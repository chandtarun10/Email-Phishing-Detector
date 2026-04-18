import sqlite3

def log_flagged_email(email):
    conn = sqlite3.connect("phishing_alerts.db")
    cur = conn.cursor()

    # Ensure table structure matches existing DB
    cur.execute("""
        CREATE TABLE IF NOT EXISTS flagged_emails (
            sender TEXT,
            subject TEXT,
            body TEXT
        )
    """)

    # Insert all 3 required values
    cur.execute(
        "INSERT INTO flagged_emails (sender, subject, body) VALUES (?, ?, ?)",
        (
            email.get("from"),
            email.get("subject", "No Subject"),
            email.get("body")
        )
    )

    conn.commit()
    conn.close()

    print("📌 Phishing email logged successfully.")
