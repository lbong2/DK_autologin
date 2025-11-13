## 설정 방법

1. `config.ini.example`을 복사해 실행 파일과 같은 위치에 `config.ini`를 만듭니다.
2. `[iris]`, `[auth]`, `[selenium]` 섹션의 값을 실제 계정 정보와 환경에 맞게 채웁니다.
   - `headless = true`로 두면 브라우저 창 없이 실행됩니다.
   - 인증 메일이 늦게 온다면 `initial_delay`, `poll_delay`, `poll_retries`를 늘리세요.
3. `poetry run python auto_login/main.py`(또는 PyInstaller로 만든 exe)를 실행합니다. `AUTO_LOGIN_CONFIG` 환경 변수를 설정하면 다른 경로의 설정 파일을 지정할 수 있습니다.

## PyInstaller로 배포하기

```
poetry run pyinstaller --onefile --name iris-auto-login auto_login/main.py
```

- 빌드가 끝나면 `dist/iris-auto-login.exe`와 동일한 폴더에 `config.ini`를 복사해 줍니다.
- Chrome 및 ChromeDriver가 설치되어 있어야 하며, 헤드리스 모드에서는 별도 창이 뜨지 않습니다.
