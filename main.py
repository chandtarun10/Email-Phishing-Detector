from email_handler import connect_to_email, fetch_emails
from phishing_detection import check_url_virustotal, keyword_phishing_check
from quarantine import quarantine_email
from alert import send_alert_email
from logger import log_flagged_email


def run(email_address, email_password):
    # Connect to email server using login credentials
    mail = connect_to_email(email_address, email_password)

    # Fetch unread emails
    emails = fetch_emails(mail)

    if not emails:
        print("No unread emails found.")
        return

    for email in emails:
        print("--------------------------------------------------")
        print(f"From: {email['from']}")
        print(f"Subject: {email['subject']}")
        print(f"Body:\n{email['body']}\n")

        # Phishing Detection (VirusTotal + Keywords)
        vt_result = check_url_virustotal(email['body'])
        keyword_result = keyword_phishing_check(email['body'])

        if vt_result or keyword_result:
            print("⚠️ Phishing email detected!")

            quarantine_email(mail, email["id"])

            send_alert_email(
                email_address,
                email_password,
                "Phishing Alert",
                "A phishing email was detected and quarantined."
            )

            log_flagged_email(email)

        else:
            print("✅ Email is safe.")
