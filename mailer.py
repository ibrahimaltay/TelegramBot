import smtplib
import ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_file(filename, username, password, subject):

    EMAIL_ADDRESS =  username
    EMAIL_PASSWORD = password

    smtp_server = "smtp.gmail.com"
    port = 587  # For starttls
    sender_email = EMAIL_ADDRESS
    password = EMAIL_PASSWORD

    subject = subject
    body = "Sent to you by Raspberry Pi"
    receiver_email = "ibrahimaltay152@hotmail.com"

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message["Bcc"] = receiver_email

    message.attach(MIMEText(body, "plain"))
    filename = filename

    with open(filename, 'rb') as f:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(f.read())
    encoders.encode_base64(part)

    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )

    message.attach(part)
    text = message.as_string()
    # Create a secure SSL context

    # Try to log in to server and send email
    context = ssl.create_default_context()
    try:
        server = smtplib.SMTP(smtp_server,port)
        server.ehlo() # Can be omitted
        server.starttls(context=context) # Secure the connection
        server.ehlo() # Can be omitted
        server.login(sender_email, password)
        # TODO: Send email here
        server.sendmail(sender_email, receiver_email, text)
    except Exception as e:
        # Print any error messages to stdout
        print(e)
    finally:
        server.quit() 