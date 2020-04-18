

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///users.db")

@app.route("/")
def index():
    '''Show MainPage'''
    return render_template("index.html")

@app.route("/login", methods=["GET","POST"])
def login():
    '''log-in page'''
    #forget any user id
    session.clear()
    return apology("Doesn't exist yet")


@app.route("/register", methods=["GET","POST"])
def register():
    ''' register page '''
    return apology("Sign-Up not functional")

@app.route("/PomoDoro", methods=["GET","POST"])
@login_required
def taskpage():
    return apology("Not Found")
















