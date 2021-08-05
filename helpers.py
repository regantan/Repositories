import os
import requests

from flask import render_template, session, redirect
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function
    
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