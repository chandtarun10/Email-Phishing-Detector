from flask import Flask, render_template, request, redirect, session, jsonify
from email_handler import connect_to_email, fetch_emails
from phishing_detection import (
    keyword_phishing_check,
    contains_url,
    check_url_virustotal
)
from quarantine import quarantine_email
from logger import log_flagged_email

app = Flask(__name__)
app.secret_key = "email-phishing-secret-key"


# ---------------- LOGIN ----------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session["email"] = request.form["email"]
        session["password"] = request.form["password"]
        session["scan_results"] = []   # clear old scan
        return redirect("/dashboard")
    return render_template("login.html")


# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    if "email" not in session:
        return redirect("/")

    # ✅ Only show stored scan results (FAST)
    results = session.get("scan_results", [])

    return render_template("dashboard.html", results=results)


# ---------------- SCAN EMAILS ----------------
@app.route("/scan", methods=["POST"])
def scan():
    if "email" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    email_address = session["email"]
    email_password = session["password"]

    results = []

    try:
        mail = connect_to_email(email_address, email_password)
        emails = fetch_emails(mail)

        for e in emails:
            phishing = False

            # ✅ FAST priority order
            if keyword_phishing_check(e["body"]):
                phishing = True
            elif contains_url(e["body"]):
                phishing = check_url_virustotal(e["body"])

            if phishing:
                quarantine_email(mail, e["id"])
                log_flagged_email(e)

            results.append({
                "id": e["id"].decode(),
                "from": e["from"],          # ✅ sender email
                "body": e["body"],
                "status": "⚠️ Phishing" if phishing else "✅ Safe"
            })

        # ✅ STORE RESULTS FOR DASHBOARD
        session["scan_results"] = results

        return jsonify({"status": "Scan complete"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ---------------- DELETE MAIL ----------------
@app.route("/delete/<email_id>", methods=["POST"])
def delete_mail(email_id):
    if "email" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    mail = connect_to_email(session["email"], session["password"])

    try:
        # 1️⃣ Select ALL mailboxes (important for Gmail)
        mail.select("INBOX", readonly=False)

        # 2️⃣ Remove Quarantine label if present
        mail.store(email_id.encode(), "-X-GM-LABELS", "Quarantine")

        # 3️⃣ Mark as deleted
        mail.store(email_id.encode(), "+FLAGS", "\\Deleted")

        # 4️⃣ Permanently delete
        mail.expunge()

        return jsonify({"status": "deleted"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500



# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
