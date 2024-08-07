import imaplib
import email
from email.header import decode_header, make_header

# 사용 전 구글 앱 비밀번호 설정해야 함.

def getAuthNumber(mail, appPw, from_email):
    server = imaplib.IMAP4_SSL("imap.gmail.com", 993)  
    server.login(mail, appPw)
    server.select("inbox")

    status, messages = server.search(None, f'(FROM "{from_email}")')

    mail_ids = messages[0].split()  

    if not mail_ids:  
        print('error')

    latest_email_id = mail_ids[-1]

    status, msg_data = server.fetch(latest_email_id, "(RFC822)")

    message = email.message_from_bytes(msg_data[0][1])
    fr = make_header(decode_header(message.get('From')))
    subject = make_header(decode_header(message.get('Subject')))


    print(f"제목:{subject}")


    server.close()
    server.logout()
    return str(subject).split('[')[1].split(']')[0]
