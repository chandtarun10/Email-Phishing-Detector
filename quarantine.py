def quarantine_email(mail, email_id):
    mail.create("Quarantine")
    mail.store(email_id, "+X-GM-LABELS", "Quarantine")
