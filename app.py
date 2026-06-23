from flask import Flask, render_template, request, redirect, session, flash
import sqlite3
import re
from werkzeug.security import (generate_password_hash,check_password_hash)


app = Flask(__name__)

app.secret_key = "super_secret_key"

def is_strong_password(password):

    if len(password) < 8:
        return False

    if not re.search(r"[A-Z]", password):
        return False

    if not re.search(r"[a-z]", password):
        return False

    if not re.search(r"\d", password):
        return False

    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False

    return True

  

def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()



@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if not is_strong_password(password):

            flash(
                "Password must contain 8+ characters, a capital letter, a small letter, a number and a special character."
            )

            return redirect("/signup")

        hashed_password = generate_password_hash(password)

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        try:

            cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, hashed_password)
            )

            conn.commit()

            user_id = cursor.lastrowid

            session["user_id"] = user_id

            flash("🎉 Account created successfully!")

            return redirect("/dashboard")

        except sqlite3.IntegrityError:

            flash("Username already exists!")

            return redirect("/signup")

        finally:

            conn.close()

    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        )

        user = cursor.fetchone()

        conn.close()

        if user and check_password_hash(user[2], password):

            session["user_id"] = user[0]

            return redirect("/dashboard")

        flash("Invalid username or password") 
        return redirect("/login")
    
    return render_template("login.html")



@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect("/login")

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT username FROM users WHERE id = ?",
        (session["user_id"],)
    )

    user = cursor.fetchone()

    conn.close()

    return render_template(
    "dashboard.html",
    username=user[0],
    user_id=session["user_id"]
)

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")


@app.route("/")
def home():
    return redirect("/login")



init_db()

if __name__ == "__main__":
    app.run(debug=True)



