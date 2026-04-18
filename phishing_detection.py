import requests
import base64
import re

VT_API_KEY = "your_api_key"

PHISHING_KEYWORDS = [
    "lottery", "won", "winner", "urgent",
    "verify", "click", "free money",
    "confirm your details", "clicking", "claim", "claiming"
]

def keyword_phishing_check(body):
    body = body.lower()
    return any(word in body for word in PHISHING_KEYWORDS)

def contains_url(body):
    return bool(re.findall(r'https?://', body))

def check_url_virustotal(body):
    urls = re.findall(r'https?://[^\s]+', body)
    for url in urls:
        url_id = base64.urlsafe_b64encode(url.encode()).decode().strip("=")
        headers = {"x-apikey": VT_API_KEY}

        response = requests.get(
            f"https://www.virustotal.com/api/v3/urls/{url_id}",
            headers=headers,
            timeout=6
        )

        if response.status_code == 200:
            stats = response.json()["data"]["attributes"]["last_analysis_stats"]
            if stats["malicious"] > 0:
                return True

    return False