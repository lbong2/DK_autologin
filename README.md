## 환경 변수 설정

1. `.env.example`을 복사해 `.env` 파일을 만듭니다.
2. 다음 값을 채웁니다.
   - `IRIS_ID`, `IRIS_PASSWORD`: IRIS 포털 로그인 정보
   - `AUTH_EMAIL`, `AUTH_APP_PASSWORD`: 2차 인증 메일을 수신하는 Gmail 계정과 앱 비밀번호
   - `AUTH_FROM_EMAIL`(선택): 인증 메일 발신자. 기본값은 `no_reply@worksmobile.com`
3. `poetry run python auto_login/main.py`로 실행하면 `.env` 값을 사용해 로그인합니다.
