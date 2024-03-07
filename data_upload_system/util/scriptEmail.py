import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

smtp_server = "smtp.mail.rice.edu"
port = 465
sender_email = "projections@rice.edu"


def sendNotification(receivers, subject, notification, filename = None):
    """
    Sends Email notification to a list of emails
    :param notification: Message to be sent
    :param receivers: List of receiver emails
    :param subject: Subject of the notification email
    :param body: Body text of the email
    :return:
    """

    """    
    receiver = sender_email
    subject = "Incredible Email from your python server!"
    body = "This is a test email from your python seever! Hope you are happy with the output"
    """
    body = notification
    for receiver in receivers:
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        if filename is not None:
            with open(filename, "r") as f:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(f.read())
                encoders.encode_base64(part)

            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {filename}",
            )

            message.attach(part)
        text = message.as_string()

        context = ssl.create_default_context()
        server = smtplib.SMTP_SSL(smtp_server, port, context=context)

        try:
            server.sendmail(sender_email, receiver, text)
        except Exception as e:
            print(e)
        finally:
            server.quit()


