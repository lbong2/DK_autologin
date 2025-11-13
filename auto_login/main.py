import configparser
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import auth

CONFIG_FILENAME = os.getenv("AUTO_LOGIN_CONFIG", "config.ini")


def _base_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    return Path(__file__).resolve().parent


def _config_path() -> Path:
    return _base_dir() / CONFIG_FILENAME


def _required(config: configparser.ConfigParser, section: str, option: str) -> str:
    try:
        value = config.get(section, option).strip()
    except (configparser.NoSectionError, configparser.NoOptionError) as exc:
        raise RuntimeError(f"[{section}] {option} 설정을 찾을 수 없습니다.") from exc
    if not value:
        raise RuntimeError(f"[{section}] {option} 값이 비어 있습니다.")
    return value


def _load_settings() -> dict:
    config_path = _config_path()
    parser = configparser.ConfigParser()
    read_files = parser.read(config_path, encoding="utf-8")
    if not read_files:
        raise FileNotFoundError(f"설정 파일을 찾을 수 없습니다: {config_path}")

    return {
        "config_path": config_path,
        "iris_id": _required(parser, "iris", "id"),
        "iris_password": _required(parser, "iris", "password"),
        "auth_email": _required(parser, "auth", "email"),
        "auth_app_password": _required(parser, "auth", "app_password"),
        "auth_from_email": parser.get("auth", "from_email", fallback="no_reply@worksmobile.com").strip()
        or "no_reply@worksmobile.com",
        "auth_initial_delay": parser.getint("auth", "initial_delay", fallback=5),
        "auth_poll_delay": parser.getint("auth", "poll_delay", fallback=5),
        "auth_poll_retries": parser.getint("auth", "poll_retries", fallback=12),
        "headless": parser.getboolean("selenium", "headless", fallback=False),
    }


def _fetch_auth_code(
    email: str,
    app_password: str,
    from_email: str,
    not_before: datetime,
    initial_delay: int,
    retries: int,
    delay: int,
) -> str:
    """Poll Gmail until a mail newer than `not_before` arrives."""
    last_error: Exception | None = None
    print(
        f"[auth] 새 인증 메일 대기 시작 "
        f"(초기 대기 {initial_delay}s, 재시도 {retries}회, 간격 {delay}s)"
    )
    time.sleep(initial_delay)
    for attempt in range(retries):
        try:
            code, received_at = auth.getAuthNumber(email, app_password, from_email)
            received_at_utc = received_at.astimezone(timezone.utc)
            if received_at_utc >= not_before:
                print(f"[auth] 새 메일 감지 ({received_at_utc.isoformat()})")
                return code
            print(
                f"[auth] 이전 코드 무시 ({received_at_utc.isoformat()} < {not_before.isoformat()}) "
                f"- 재시도 {attempt + 1}/{retries}"
            )
        except Exception as exc:  # noqa: BLE001
            last_error = exc
            print(f"[auth] 메일 확인 실패({attempt + 1}/{retries}): {exc}")
        if attempt < retries - 1:
            time.sleep(delay)
    if last_error:
        raise RuntimeError("새로운 2차 인증 메일을 확인하지 못했습니다.") from last_error
    raise RuntimeError("새로운 2차 인증 메일을 확인하지 못했습니다.")


def _input_credentials(driver: webdriver.Chrome, wait: WebDriverWait, settings: dict) -> None:
    """Handle overlay inputs (#idtemp/#passwordtemp) and type into real fields."""
    user_id_overlay = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#idtemp")))
    user_id_overlay.click()
    user_id = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#id")))
    user_id.clear()
    user_id.send_keys(settings["iris_id"])

    pw_overlay = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#passwordtemp")))
    pw_overlay.click()
    pw = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#password")))
    pw.clear()
    pw.send_keys(settings["iris_password"])


def main() -> None:
    settings = _load_settings()
    print(f"[config] 설정 파일 로드: {settings['config_path']}")

    chrome_options = Options()
    chrome_options.add_experimental_option("detach", not settings["headless"])
    if settings["headless"]:
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
    print(f"[iris] 브라우저 옵션 설정 완료 (headless={settings['headless']})")

    iris_driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(iris_driver, 15)
    print("[iris] WebDriver 초기화 완료")

    iris_driver.get("https://iris.dongkuk.com/")
    print("[iris] IRIS 로그인 페이지 접속")

    _input_credentials(iris_driver, wait, settings)
    print("[iris] 사용자 아이디/비밀번호 입력 완료")

    login_bt = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "#frm > section > section > article.loginBox > div > div:nth-child(4) > a")
        )
    )
    login_bt.click()
    print("[iris] 로그인 버튼 클릭")

    auth_bt = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#privateEmailButton")))
    auth_bt.click()
    print("[iris] 2차 인증 메일 요청 완료")

    request_timestamp = datetime.now(timezone.utc)
    auth_num = _fetch_auth_code(
        settings["auth_email"],
        settings["auth_app_password"],
        settings["auth_from_email"],
        not_before=request_timestamp,
        initial_delay=settings["auth_initial_delay"],
        retries=settings["auth_poll_retries"],
        delay=settings["auth_poll_delay"],
    )

    pw2 = WebDriverWait(iris_driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#number1")))
    pw2.clear()
    pw2.send_keys(auth_num)
    print("[iris] 2차 인증번호 입력 완료")
    print("[iris] 자동 로그인 절차 완료")


if __name__ == "__main__":
    main()
