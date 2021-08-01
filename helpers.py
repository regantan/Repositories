import os
from flask import render_template
import requests

def apology(error, code):
    return render_template("apology.html", code=code, error=error)
    
def check_email(email):
    
    try:
        api_key = os.environ.get("API_KEY")
        url = "https://api.reacher.email/v0/check_email"
        header = {"authorization": api_key}
        payload = {"to_email": email}
        response = requests.post(url, json=payload, headers=header)
        response.raise_for_status()
    except requests.RequestException:
        return None
    
    try:
        check = response.json()
        return {
            "email": check["input"],
            "check": check["is_reachable"]
        }
    except (KeyError, TypeError, ValueError):
        return None