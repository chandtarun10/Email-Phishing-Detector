import imaplib
import email
from email.utils import parseaddr

IMAP_SERVER = "imap.gmail.com"


def connect_to_email(email_address, email_password):
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(email_address, email_password)
    return mail


def fetch_emails(mail):
    mail.select("inbox", readonly=False)
    _, data = mail.search(None, "ALL")

    emails = []

    for email_id in data[0].split():
        _, msg_data = mail.fetch(email_id, "(RFC822)")
        msg = email.message_from_bytes(msg_data[0][1])

        # ✅ Correct sender email
        _, sender_email = parseaddr(msg.get("From"))

        email_info = {
            "id": email_id,
            "from": sender_email,
            "body": ""
        }

        # ✅ FIXED INDENTATION HERE
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    email_info["body"] = part.get_payload(decode=True).decode(
                        errors="ignore"
                    )
                    break
        else:
            email_info["body"] = msg.get_payload(decode=True).decode(
                errors="ignore"
            )

        emails.append(email_info)

    return emails
