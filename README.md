# 🛡️ Email Phishing Detector

> **A smart, real-time phishing email detection system built with Python & Flask.**  
> Automatically scans your Gmail inbox, flags suspicious emails, quarantines threats, and keeps you safe — all from a sleek web dashboard.

## 📖 Table of Contents

- [What Is This Project?](#-what-is-this-project)
- [How It Works (Simple Explanation)](#-how-it-works-simple-explanation)
- [Project Structure](#-project-structure)
- [File-by-File Breakdown](#-file-by-file-breakdown)
- [Tech Stack](#-tech-stack)
- [Setup & Installation](#-setup--installation)
- [How to Run](#-how-to-run)
- [Using the App](#-using-the-app)
- [Security Issues to Fix](#-security-issues-to-fix)
- [Future Improvements](#-future-improvements)
- [Author](#-author)

---

## 🤔 What Is This Project?

Phishing emails are **fake emails** designed to trick you into giving away your passwords, credit card details, or personal information. They often look like they're from real companies (banks, Google, etc.) but they're not.

This project is a **web application** that:
- Connects to your Gmail account securely
- Reads your emails automatically
- Uses two techniques to detect if an email is a phishing attempt
- Moves dangerous emails to a "Quarantine" folder
- Shows you everything on a clean dashboard

Think of it like a **security guard** for your inbox 📬🔒

---

## ⚙️ How It Works (Simple Explanation)

```
You Log In → App Connects to Gmail → Fetches Emails → Scans Each Email
                                                              ↓
                              ┌───────────────────────────────────────┐
                              │        Two-Layer Detection System      │
                              │                                        │
                              │  1️⃣ Keyword Check                    │
                              │     Looks for words like:             │
                              │     "lottery", "urgent", "winner",    │
                              │     "verify", "free money", etc.      │
                              │                                        │
                              │  2️⃣ URL Check (VirusTotal API)        │
                              │     If email has a link, checks it    │
                              │     against VirusTotal's database of  │
                              │     60+ antivirus engines             │
                              └───────────────────────────────────────┘
                                              ↓
                    ┌─────────────────────────────────────────────┐
                    │                                             │
               ⚠️ PHISHING?                                  ✅ SAFE?
                    │                                             │
         Move to Quarantine folder                   Show as "Safe" on dashboard
         Send alert email to you
         Log it in the database
```

---

## 📁 Project Structure

```
Email-phishing-detector-main/
│
├── 📄 app.py                  ← Main web application (Flask routes)
├── 📄 main.py                 ← Standalone runner (without web UI)
├── 📄 email_handler.py        ← Connects to Gmail, fetches emails
├── 📄 phishing_detection.py   ← Brain: keyword + VirusTotal checks
├── 📄 alert.py                ← Sends alert email if phishing found
├── 📄 logger.py               ← Saves phishing emails to database
├── 📄 quarantine.py           ← Moves bad emails to Quarantine folder
├── 🗄️ phishing_alerts.db      ← SQLite database of caught phishing emails
│
├── 📁 templates/
│   ├── login.html             ← Login page (web UI)
│   └── dashboard.html         ← Main dashboard (web UI)
│
├── 📁 static/
│   ├── style.css              ← Dashboard styling
│   ├── login.css              ← Login page styling
│   ├── script.js              ← Frontend JavaScript (scan, delete, view)
│   └── bp.jpg                 ← Background image
│
└── 📁 __pycache__/            ← Python auto-generated cache (ignore this)
```

---

## 🔍 File-by-File Breakdown

### 🔷 `app.py` — The Heart of the Web App

This is the **main Flask application**. Flask is a Python framework that lets you build websites. This file defines what happens when you visit different pages:

| Route | What It Does |
|-------|-------------|
| `/` (GET) | Shows the login page |
| `/` (POST) | Accepts your login and redirects to dashboard |
| `/dashboard` | Shows your email scan results |
| `/scan` | Triggers email scanning (called by the Scan button) |
| `/delete/<id>` | Deletes a specific email permanently |
| `/logout` | Logs you out and clears the session |

> 💡 **For beginners:** A "route" is like a URL path. When you go to `http://localhost:5000/dashboard`, Flask runs the `dashboard()` function.

---

### 🔷 `email_handler.py` — Connecting to Gmail

This file handles the actual connection to Gmail using **IMAP** (a standard protocol for reading emails).

**Key functions:**
- `connect_to_email(email, password)` — Logs in to Gmail securely using SSL encryption
- `fetch_emails(mail)` — Gets ALL emails from your inbox and extracts sender + body text

> 💡 **For beginners:** IMAP is like a postal worker that fetches your mail from the post office (Gmail's servers) and brings it to your house (this app).

---

### 🔷 `phishing_detection.py` — The Detection Engine

This is the **brain** of the project. It has three functions:

**1. `keyword_phishing_check(body)`**  
Scans the email text for suspicious words:
```
"lottery", "won", "winner", "urgent", "verify", "click",
"free money", "confirm your details", "clicking", "claim", "claiming"
```
If any of these appear → flagged as phishing ⚠️

**2. `contains_url(body)`**  
Checks if the email contains any links (http:// or https://)

**3. `check_url_virustotal(body)`**  
If a URL is found, it sends it to **VirusTotal** — a free service that checks URLs against 60+ antivirus databases. If any engine reports it as malicious → flagged as phishing ⚠️

> 💡 **For beginners:** Think of VirusTotal as a crowd of 60 security experts — if even one of them says a link is dangerous, the email gets flagged.

> ⚠️ **Note:** You need to replace `"your_api_key"` in this file with a real VirusTotal API key (free at [virustotal.com](https://www.virustotal.com))

---

### 🔷 `alert.py` — Email Alert System

When a phishing email is detected, this file **sends you an alert email** using SMTP (Gmail's email sending protocol). The alert goes to the same Gmail account you're scanning.

---

### 🔷 `logger.py` — Database Logging

Uses **SQLite** (a simple built-in database) to save every caught phishing email with:
- Sender's address
- Email subject
- Email body

This creates a permanent record in `phishing_alerts.db` that you can review later.

---

### 🔷 `quarantine.py` — Email Quarantine

Moves flagged emails to a **"Quarantine"** label/folder in Gmail so they're separated from your real inbox but not deleted (in case of false positives).

---

### 🔷 `templates/login.html` — Login Page

The login page where you enter:
- Your Gmail address
- Your **Gmail App Password** (NOT your regular Gmail password — see setup below)

> ⚠️ **PRIVACY ISSUE:** Lines 51-52 show your phone number and email in the footer. Remove these before submitting or deploying!

---

### 🔷 `templates/dashboard.html` — The Control Panel

Shows a table of all scanned emails with:
- Sender email
- View button (opens email content in a popup)
- Delete button (permanently deletes the email)
- Status badge (⚠️ Phishing or ✅ Safe)

Also shows summary stats: Total / Phishing / Safe counts.

---

### 🔷 `static/script.js` — Frontend Logic

Handles:
- The "Scan Emails" button (calls `/scan` API)
- "View" popup modal to read email body
- "Delete" button with confirmation

---

### 🔷 `main.py` — Command Line Version

A standalone script to run phishing detection **without the web interface** — useful for testing or running in the background automatically.

---

## 🛠️ Tech Stack

| Technology | Purpose |
|-----------|---------|
| 🐍 Python 3 | Core programming language |
| 🌐 Flask | Web framework (runs the website) |
| 📧 imaplib | Connects to Gmail via IMAP |
| 🔍 VirusTotal API | URL malware checking |
| 🗄️ SQLite | Database for storing phishing logs |
| 🎨 HTML/CSS/JS | Frontend dashboard UI |
| 📬 smtplib | Sending alert emails |
| 🔐 IMAP SSL | Secure email connection |

---

## 🚀 Setup & Installation

### Step 1: Prerequisites

Make sure you have Python 3 installed:
```bash
python --version
```

### Step 2: Install Required Libraries

```bash
pip install flask requests
```

### Step 3: Get a Gmail App Password

> ⚠️ Gmail does NOT allow using your regular password in third-party apps. You need an **App Password**.

1. Go to your Google Account → **Security**
2. Enable **2-Step Verification** (if not already on)
3. Search for **"App Passwords"**
4. Create a new App Password → Select "Mail" → Copy the 16-character password

### Step 4: Get a VirusTotal API Key

1. Go to [virustotal.com](https://www.virustotal.com) and create a free account
2. Go to your profile → **API Key**
3. Copy your API key
4. Open `phishing_detection.py` and replace:
   ```python
   VT_API_KEY = "your_api_key"
   ```
   with your actual key.

### Step 5: Fix the Privacy Issue

Open `templates/login.html` and remove or update lines 51-52:
```html
<!-- REMOVE or UPDATE these lines: -->
📞 +91 9027239296 <br>
📧 chandtarun1234@gmail.com
```

---

## ▶️ How to Run

```bash
# Navigate to the project folder
cd Email-phishing-detector-main

# Start the Flask web app
python app.py
```

Then open your browser and go to:
```
http://localhost:5000
```

---

## 📱 Using the App

### Step 1 — Login
- Enter your **Gmail address**
- Enter your **Gmail App Password** (the 16-character one, not your real password)
- Click **Login**

### Step 2 — Scan Your Emails
- On the dashboard, click the **🔍 Scan Emails** button
- Wait while the app fetches and analyzes your inbox
- Results will appear in the table

### Step 3 — Review Results
- **⚠️ Phishing** emails are highlighted in red — these have been auto-quarantined
- **✅ Safe** emails are shown normally
- Click **👁 View** to read the email content
- Click **🗑 Delete** to permanently remove an email

### Step 4 — Logout
- Click **Logout** when done to clear your session securely

---

## 🔐 Security Issues to Fix

Before submitting this project to Google's security officer, here are the issues that should be addressed:

| # | Issue | File | Severity | Fix |
|---|-------|------|----------|-----|
| 1 | Phone number exposed publicly | `login.html:51` | 🔴 HIGH | Remove from HTML footer |
| 2 | Email exposed publicly | `login.html:52` | 🔴 HIGH | Remove from HTML footer |
| 3 | Hardcoded placeholder API key | `phishing_detection.py` | 🟡 MEDIUM | Use environment variable |
| 4 | Weak Flask secret key | `app.py` | 🟡 MEDIUM | Use a strong random key |
| 5 | Password stored in session | `app.py` | 🟡 MEDIUM | Use OAuth2 instead |
| 6 | No login authentication | `app.py` | 🟡 MEDIUM | Any email/password works |
| 7 | Debug mode enabled | `app.py` | 🟠 LOW-MED | Set `debug=False` in production |

### Quick Security Fixes:

**Fix the API key (use environment variable):**
```python
import os
VT_API_KEY = os.environ.get("VT_API_KEY", "")
```

**Fix the Flask secret key:**
```python
import secrets
app.secret_key = secrets.token_hex(32)
```

**Disable debug mode for production:**
```python
if __name__ == "__main__":
    app.run(debug=False)  # Change True → False
```

---

## 🔮 Future Improvements

- [ ] 🤖 Add machine learning model for smarter detection
- [ ] 📊 Add charts and graphs to the dashboard
- [ ] 🔑 Replace password auth with Google OAuth2 (safer)
- [ ] 📨 Support for Outlook, Yahoo Mail, etc.
- [ ] 🌐 Deploy to cloud (Heroku, AWS, etc.)
- [ ] 📱 Make the UI mobile-friendly
- [ ] 🕐 Add automatic scheduled scanning (every hour)
- [ ] 📈 Add historical statistics and trends

---

## 👨‍💻 Author

**Tarun Chand**  
📧 chandtarun1234@gmail.com

---

## 📄 License

This project was built for educational and security demonstration purposes.

---

> 🛡️ *"Security is not a product, but a process."* — Bruce Schneier

---

*Built with ❤️ using Python & Flask*
