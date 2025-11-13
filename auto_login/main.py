import os
import time

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

import pyautogui
import pyperclip

import auth


def _required_env(key: str) -> str:
    """Return required env var or raise for quicker failure."""
    value = os.getenv(key)
    if not value:
        raise RuntimeError(f"{key} is not set in the environment.")
    return value


load_dotenv()

IRIS_ID = _required_env("IRIS_ID")
IRIS_PASSWORD = _required_env("IRIS_PASSWORD")
AUTH_EMAIL = _required_env("AUTH_EMAIL")
AUTH_APP_PASSWORD = _required_env("AUTH_APP_PASSWORD")
AUTH_FROM_EMAIL = os.getenv("AUTH_FROM_EMAIL", "no_reply@worksmobile.com")

# 브라우저 꺼짐 방지 옵션
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

iris_driver = webdriver.Chrome(options=chrome_options)
iris_driver.get("https://iris.dongkuk.com/")
iris_driver.implicitly_wait(10)

user_id = iris_driver.find_element(By.CSS_SELECTOR, "#idtemp")
user_id.click()
pyperclip.copy(IRIS_ID)
pyautogui.hotkey("ctrl", "v")
iris_driver.implicitly_wait(10)

pw = iris_driver.find_element(By.CSS_SELECTOR, "#passwordtemp")
pw.click()
pyperclip.copy(IRIS_PASSWORD)
pyautogui.hotkey("ctrl", "v")
iris_driver.implicitly_wait(10)

login_bt = iris_driver.find_element(By.CSS_SELECTOR, "#frm > section > section > article.loginBox > div > div:nth-child(4) > a")
login_bt.click()
iris_driver.implicitly_wait(10)

# 2차인증
auth_bt = iris_driver.find_element(By.CSS_SELECTOR, "#privateEmailButton")
auth_bt.click()

time.sleep(5)
# 이메일 내용 호출
auth_num = auth.getAuthNumber(AUTH_EMAIL, AUTH_APP_PASSWORD, AUTH_FROM_EMAIL)

# 인증번호 입력
pw2 = iris_driver.find_element(By.CSS_SELECTOR, "#number1")
pw2.click()
pyperclip.copy(auth_num)
pyautogui.hotkey("ctrl", "v")
