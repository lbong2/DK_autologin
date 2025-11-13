## 사용 방법

준비물: 구글 메일

1. https://support.bespinglobal.com/ko/support/solutions/articles/73000545275--gmail-%EC%95%B1-%EB%B9%84%EB%B0%80%EB%B2%88%ED%98%B8-%EC%83%9D%EC%84%B1%EB%B0%A9%EB%B2%95

- app 비밀번호 설정 후 config.ini 파일 app_password 항목에 저장

2. https://support.bespinglobal.com/ko/support/solutions/articles/73000545270--gmail-pop-%EB%B0%8F-imap-%ED%99%9C%EC%84%B1%ED%99%94-%ED%95%98%EA%B8%B0

- 구글 gmail imap 활성화

3. config.ini 파일 생성 후 내용 저장 config.ini.example 참고

4. config.ini 파일과 exe 파일 동일한 경로에 넣고 exe파일 실행

```
[iris]
id = your_iris_id
password = your_iris_password

[auth]
email = your_gmail_address
app_password = your_gmail_app_password
from_email = no_reply@worksmobile.com (고정)
initial_delay = 5
poll_delay = 5
poll_retries = 12

[selenium]
headless = false
```
