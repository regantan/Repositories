import os
from flask import render_template
import requests

def apology(error, code):
    render_template("apology.html", code=code, error=error)
    
def check_email(email):
    
    try:
        api_key = os.environ.get("API_KEY")
        url = "https://api.reacher.email/v0/check_email"
        payload = {"to_email": email}
        response = requests.post(url, json=payload)
        response.raise_for_status()
    except requests.RequestException:
        return None
    
    try:
        check = response.json()
        return {
            "email": check[0]["input"],
            "check": check[0]["is_reachable"]
        }
    except (KeyError, TypeError, ValueError):
        return None