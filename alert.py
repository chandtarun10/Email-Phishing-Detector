import smtplib
from email.mime.text import MIMEText

def send_alert_email(sender_email, sender_password, subject, message):
    """
    Sends phishing alert email using the same Gmail
    credentials used during web login.
    """

    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    receiver_email = sender_email  # alert goes to same project mail

    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())

        print("Alert email sent successfully.")

    except Exception as e:
        print("Failed to send alert email:", e)
