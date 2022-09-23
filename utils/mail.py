import smtplib
import ssl

# DEPRECIADO


class SendMail:

    def __init__(self, user_mail: str, auth_token: str):
        port = 465  # For SSL
        smtp_server = "smtp.gmail.com"
        sender_email = "email@gmail.com"  # Enter your address
        receiver_email = user_mail  # Enter receiver address
        password = ''
        message = f"""\
        Subject: Hi there

        Envie o comando: /token {auth_token}
        E pronto, você ja pode utilizar o BOT!"""

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)
