import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime
import sys

class SendEmail():
    mailserver = None
    sender = "servicedeskjira@inatel.br"
    password = ""
    #to = "paulosergio@inatel.br,paulosergio.natercia@gmail.com"
    #cc = "paulosergio.natercia@gmail.com"#tadeuribeiro@inatel.br,andersonarruda@inatel.br"

    def __init__(self):
        pass

    def send(self, to, cc, subject, messageText, messageHtml):
        msg = MIMEMultipart('alternative')
        msg.attach(MIMEText(messageText, 'text'))
        msg.attach(MIMEText(messageHtml, 'html'))
        msg['From'] = self.sender
        msg['to'] = to
        msg['cc'] = cc
        msg["Subject"] = subject
        allToAdddr = cc.split(",") + to.split(",")
        self.mailserver = smtplib.SMTP('smtp-mail.outlook.com', '587')
        self.mailserver.ehlo()
        self.mailserver.starttls()
        self.mailserver.login(self.sender, self.password)
        self.mailserver.sendmail(self.sender, allToAdddr, msg.as_string())
        self.mailserver.quit()
        self.mailserver.close()
        print("Email '{}' enviado de {} para {} às {}".format(subject, self.sender, to,  datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')))

if __name__ == "__main__":
    try:
        message = "POC-500: Bug de formatacao decimal invalida"
        sendEmail = SendEmail()
        sendEmail.send("paulosergio@inatel.br", "paulosergio.natercia@gmail.com", 'Teste de envio de email pelo Python', message, message)
        sendEmail.send("paulosergio@inatel.br", "paulosergio.natercia@gmail.com", 'Teste de envio de email pelo Python', message, message)
        sendEmail.send("paulosergio@inatel.br", "paulosergio.natercia@gmail.com", 'Teste de envio de email pelo Python', message, message)
        print("Email enviado")
    except Exception as ex:
        print(str(ex))
    sys.exit(0)
