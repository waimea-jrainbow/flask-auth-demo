#===========================================================
# APP NAME HERE
# By YOUR NAME HERE
#===========================================================

from flask import Flask, request, session, render_template, flash, redirect, send_file, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from os import getenv
from io import BytesIO
import html
from app.helpers import *


# Create the app
app = Flask(__name__)


#===========================================================
# App Routes Handlers
#===========================================================

#-----------------------------------------------------------
# Welcome page
#-----------------------------------------------------------
@app.get("/")
def show_welcome():
    return render_template("pages/welcome.jinja")



#-----------------------------------------------------------
# Help page - Show some help
#-----------------------------------------------------------
@app.get("/help")
def show_help():

    flash("Flash test message")
    flash("Flash test message with a longer bit of text")
    flash("Success test message", "success")
    flash("Error test message", "error")

    return render_template("pages/help.jinja")


#-----------------------------------------------------------
# Signup page
#-----------------------------------------------------------
@app.get("/user/new")
def show_signup_form():
    return render_template("pages/user_form.jinja")

#-----------------------------------------------------------
# Handle user signup
#-----------------------------------------------------------
@app.post("/user")
def process_new_user():
    forename = request.form.get('forename','').strip()
    surname = request.form.get('surname','').strip()
    username = request.form.get('username','').strip()
    password = request.form.get('password','').strip()
    
    with connect_db() as db:
        sql = "SELECT id FROM users WHERE username=?"
        param = (username,)
        user = db.execute(sql,param).fetchone()

        if user:
            flash(f"Username '{username}' already exists", "error")

            return redirect("/user/new")

        pass_hash = generate_password_hash(password)

        sql = """
            INSERT INTO users (forename, surname, username, pwdHash)
            VALUES (?, ?, ?, ?)
            """

        params= (forename, surname, username, pass_hash)
        db.execute(sql, params)

        flash("Account created. Please login", "success")
        return redirect("/")



#===========================================================
# Serve login page
#===========================================================

@app.get("/user/login")
def show_signin_form():
    return render_template("pages/user_login_form.jinja")

#===========================================================
# Login route
#===========================================================
@app.post("/login")
def login_user():
    username = request.form.get('username', '').strip().lower()
    password = request.form.get('password', '').strip()

    with connect_db() as db:
        sql = """
            SELECT id, forename, surname, pwdHash
            FROM users
            WHERE username=?
        """
        params = (username,)
        user = db.execute(sql, params).fetchone()

        if not user:
            flash(f"Unknown user", "error")
            return redirect("/login")

        if not check_password_hash(user["pwdHash"], password):
            flash(f"Incorrect password", "error")
            return redirect("/login")

        session["logged_in"] = True
        session["user"] = {
            "username": username,
            "forename": user["forename"],
            "surname":  user["surname"],
        }

        flash("Login successful", "success")
        return redirect("/")

#===========================================================
# Logout
#===========================================================
@app.get("/logout")
def logout_admin():
    session.clear()
    flash(f"You have been logged out", "success")
    return redirect("/")

#-----------------------------------------------------------
# Message board page - Show all the messages
#-----------------------------------------------------------
@app.get("/messages")
def show_all_messages():
    with connect_db() as db:
        sql = """
            SELECT messages.id, user_id, title, body, users.username
            FROM messages
            JOIN users ON messages.user_id = users.id;
        """
        params = ()
        messages = db.execute(sql, params).fetchall()

        return render_template("pages/message_list.jinja", board_messages=messages)


#===========================================================
# Serve login page
#===========================================================

@app.get("/message/new_message")
@login_required
def show_message_form():
    return render_template("pages/message_form.jinja")

#===========================================================
# Post message route
#===========================================================
@app.post("/message/post_message")
@login_required
def post_message():
    title = request.form.get('title', '').strip()
    body = request.form.get('body', '').strip()
    user = session.user_id

    with connect_db() as db:
        
        if not user:
            flash(f"You need to be logged in to post.", "error")
            return redirect("/login")

        else:
        
            sql = """
            INSERT INTO messages (user_id, title, body)
            VALUES (?, ?, ?, ?)
            """

        params= (user, title, body)
        db.execute(sql, params)

        
        return redirect("/")


#===========================================================
# Configure the app
#===========================================================
load_dotenv()
app.config.from_prefixed_env()
init_logging(app)
init_text_filters(app)
init_date_filters(app)
init_error_handlers(app)
init_database()
register_commands(app)

