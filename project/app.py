import os
import re

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

# Configure application
app = Flask(__name__)

# Ensure Templates are auto-reloaded
app.config["TEMPLATES_AUTO-RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Ensure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILEDIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure cs50 Library to use sqlite database
db = SQL("sqlite:///ratemyuni.db")

# Make sure API key is set
# if not os.environ.get("API_KEY"):
#    raise RuntimeError("API_KEY not set")

@app.route("/")
def index():
    # Shows homepage and asks user input for a university name
    return render_template("index.html")

@app.route("/login")
def login():
    # Asks for login details and checks again database
    if request.method == "GET":
        return render_template("login.html")
    
    return # TODO

@app.route("/register")
def register():
    # Registers user in database
    return # TODO

@app.route("/rating")
def rating():
    # Displays ratings for a university and asks for user input on ratings
    return # TODO

@app.route("/university")
def university():
    # Asks for university details in the case that it does not exist in database
    return # TODO