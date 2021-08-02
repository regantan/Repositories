import os
import re

from cs50 import SQL
from datetime import date
from flask import Flask, flash, redirect, render_template, request, session, jsonify
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

@app.route("/")
def index():
    # Shows homepage and asks user input for a university name
    return render_template("index.html")

@app.route("/search")
def search():
    # Queries database on name of universities
    q = request.args.get("q")
    if not q:
        universities = []
    else:
        universities = db.execute("SELECT * FROM universities WHERE name LIKE ? ORDER BY name", "%" + q + "%")
    return jsonify(universities)

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
        return render_template("register.html")
        
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
        print(check["check"])
        if not check or check["check"] != "safe":
            return apology("Invalid Email", 400)
        rows = db.execute("SELECT username FROM users WHERE username = ?", email)
        print(rows)
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
    if request.method == "GET":
        universities = db.execute("SELECT * FROM universities")
        q = request.args.get("q")
        if not q:
            flash("Please type in university name on the home page")
            return redirect("/")
        ratings = db.execute("SELECT * FROM ratings JOIN universities ON ratings.university_id = universities.id JOIN courses ON ratings.course_id = courses.id WHERE universities.id = ? ORDER BY date DESC", q)
        if len(ratings) == 0:
            flash("This university has no review yet!")
            return redirect("/rate")
        grade = 0; counter = 0
        for rating in ratings:
            grade += rating["overall"]
            counter += 1
        grade = float(grade) / counter
        grade = round(grade, 2)
        name = db.execute("SELECT * FROM universities WHERE id = ?", q)
        return render_template("ratings.html", ratings=ratings, universities=universities, grade=grade, name=name[0]["name"])
            
    else:
        name = request.form.get("name")
        year = request.form.get("year")
        comment = request.form.get("comment")
        course = request.form.get("course")
        status = request.form.get("status")
        if not name or not year or not comment or not course or not status:
            return apology("Missing information", 400)
        if int(year) > date.today().year or int(year) < 2015:
            return apology(f"Year entered must be between 2015 and {date.today().year}", 400)
        university = db.execute("SELECT * FROM universities WHERE name LIKE ?", name)
        if len(university) != 1:
            return apology("Invalid university name", 400)
        if re.search("[^a-zA-Z\s]", course) != None:
            return apology("Course names should only contain letters", 400)
        courses = db.execute("SELECT * FROM courses WHERE name LIKE ?", course)
        if len(courses) == 0:
            db.execute("INSERT INTO courses (name) VALUES (UPPER(?))", course)
        elif len(courses) != 1:
            message = "Did you mean: "
            for row in courses:
                message += row.name
            return apology(message, 400)
        courses = db.execute("SELECT * FROM courses WHERE name LIKE ?", course)
        if status != "Completed" and status != "Ongoing" and status != "Dropped Out":
            return apology("Status should only be 'Completed', 'Ongoing' or 'Dropped out'", 400)
                
        sliders = {}
        sliders["facilities"] = request.form.get("facilities")
        sliders["location"] = request.form.get("location")
        sliders["safety"] = request.form.get("safety")
        sliders["workload"] = request.form.get("workload")
        sliders["food"] = request.form.get("food")
        sliders["clubs"] = request.form.get("clubs")
        sliders["happiness"] = request.form.get("happiness")
        overall = 0; counter = 0
        for row in sliders:
            if re.search("/D", sliders[row]) != None or int(sliders[row]) < 1 or int(sliders[row]) > 5:
                return apology("Slider ranges are only integers between 1 and 5", 400)
            sliders[row] = int(sliders[row])
            overall += sliders[row]
            counter += 1
        overall = float(overall) / counter
        sliders["overall"] = round(overall, 2)
        
        id = db.execute('INSERT INTO ratings (date, university_id, course_id, facilities, location, safety, workload, food, clubs, happiness, status, year, comment, overall) VALUES (DATE("now"), (SELECT id FROM universities WHERE name LIKE ?), (SELECT id FROM courses WHERE name LIKE UPPER(?)) , ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) ', university[0]["name"], courses[0]["name"], sliders["facilities"], sliders["location"], sliders["safety"], sliders["workload"], sliders["food"], sliders["clubs"], sliders["happiness"], status, int(year), comment, overall)
        return redirect(f"/rating?q={university[0]['id']}")

@app.route("/rate")
def rate():
    universities = db.execute("SELECT * FROM universities")
    return render_template("rate.html", universities=universities)

@app.route("/university")
def university():
    # Asks for university details in the case that it does not exist in database
    return # TODO

@app.route("/about")
def about():
    # shows about page
    return # TODO