

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

    if request.method == "POST": # request recieved by submitting the login form

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session["username"] = rows[0]["username"]

        # Redirect user to home page
        return redirect("/taskpage")

    else: # route reached via link, address bar or redirect
        return render_template("login.html")


@app.route("/register", methods=["GET","POST"])
def register():
    ''' register page '''
    session.clear()

    if request.method == "POST":

         # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",username=request.form.get("username"))

        # Ensure username is available
        if len(rows) == 1:
            return apology("Username Already Taken, Please try again")

        # Password authentication
        if not request.form.get("password"):
            return apology("must enter password", 400)

        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("Passwords do not match.", 400)

        hsh = generate_password_hash(request.form.get("password"))

        db.execute("INSERT INTO users(username, hash) VALUES (:username, :hasher);", username=request.form.get("username"), hasher=hsh)


        # Redirect user to login page
        return redirect("/login")


    else:
        return render_template("register.html")



@app.route("/taskpage", methods=["GET","POST"])
@login_required
def taskpage():

    """define tasks as a select query from the tasks table
        containing the tasks in a list format"""
    tasks=[]
    foo = db.execute("SELECT * FROM tasks WHERE username = :username", username=session["username"])
    for i in foo:
        tasks.append(i["task"])

    session["taskcount"] = len(tasks)
    session["tasks"] = tasks

    tasks = enumerate(tasks)


    return render_template("taskpage.html", tasks=tasks, count=session["taskcount"],)

@app.route("/add", methods=["GET","POST"])
@login_required
def add():
    if request.method == "POST":
        task = request.form.get("task")
        if not task:
            return apology("Enter a Task")
        db.execute("INSERT INTO tasks(username, task) VALUES (:username, :task);", username=session["username"], task=task)
        return redirect("/taskpage")

@app.route("/remove", methods=["GET", "POST"])
@login_required
def remove():
    if request.method == "POST":

        for i in range(session["taskcount"]):

            foo = "check"+str(i)
            #bar = "removed"+str(i)
            if request.form.get(foo):

                db.execute("DELETE FROM tasks WHERE task=:task;", task=session["tasks"][i])

    return redirect("/taskpage")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()
    # Redirect user to login form
    return redirect("/")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)


if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)