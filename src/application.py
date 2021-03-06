import os

from flask import Flask, session, render_template, request, redirect
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = "123456789abcdefghi"

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def index():
    if "username" in session:
        return render_template("index.html")
    return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
    error = ""
    username = ""
    password = ""
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        print(f"{username} / {password}")
        if db.execute("SELECT * FROM users WHERE username=:username AND passwd=:password",
                    {"username": username, "password": password}).rowcount == 0:
            error = "Username or Password is incorrect."
            return render_template("login.html", error=error)
        else:
            session["username"] = username
            return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        error = ""
        username = request.form.get("username")
        password0 = request.form.get("password")
        password1 = request.form.get("passwordRepeat")
        if len(username) < 3 or len(password0) < 8:
            error = "Either username or password length do not suffice (username has to be greater than 2 and password has to contain a minimum of 8 letters)"
            print(error)
            print("hurz")
        if not password0 == password1:
            error = "Passwords do not match!"
            print(password0)
            print(password1)
            print(error)
        if error == "":
            db.execute("insert into users (username, passwd) values (:username, :password)",
                                        {"username": username, "password": password0})
            db.commit()
            print(f"Hallo {error}")
            return redirect("/login")
        return render_template("register.html", error=error)
