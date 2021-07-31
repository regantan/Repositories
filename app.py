import os
import re

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import check_email, apology

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
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")

@app.route("/", methods=["GET", "POST"])
def index():
    # Shows homepage and asks user input for a university name
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    # Clears cookies
    session.clear()
    
    if request.method == "GET":
        return render_template("login.html")
    
    else:
        email = request.form.get("email")
        password = request.form.get("password")

        if not email or not password:
            return apology("Missing Email/Password", 400)
        rows = db.execute("SELECT * FROM users WHERE username = ?", email)
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            return apology("Invalid Email/Password", 400)
        
        session["user_id"] = rows[0]["id"]
        flash("Successfully Logged In")
        return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    # Allows user to register (method GET)
    if request.method == "GET":
        render_template("register.html")
        
    # Process user input (method POST)
    else:
        email = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirm_password")
        
        # Ensure email and passwords are typed in
        if not email or not password or not confirmation:
            return apology("Missing Email/Password", 400)
        
        # Ensures email is valid
        check = check_email(email)
        if check["check"] != "safe":
            return apology("Invalid Email", 400)
        rows = db.execute("SELECT username FROM users WHERE username = ?", email)
        
        # Ensures email is unique
        if len(rows) != 0:
            return apology("Email Already Exists", 400)
        
        # Ensures passwords are identical
        if password != confirmation:
            return apology("Passwords do not match", 400)
        
        # Insert info into database
        password_hash = generate_password_hash(password)
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", email, password_hash)
        return redirect("/login")

@app.route("/rating", methods=["GET", "POST"])
def rating():
    # Displays ratings for a university and asks for user input on ratings
    return # TODO

@app.route("/university")
def university():
    # Asks for university details in the case that it does not exist in database
    return # TODO