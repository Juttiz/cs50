import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    # portfolio = db.execute("SELECT * FROM users WHERE id = user_id")
    user_id = session["user_id"]
    holds = []

    mn = db.execute(f"SELECT cash FROM users WHERE id = '{user_id}'")
    tl = mn[0]["cash"]
    properties = db.execute(f"SELECT symbol, SUM(share) FROM share_hold WHERE id = '{user_id}' GROUP BY symbol")
    for property in properties:
        holds.append(lookup(property["symbol"]))
    for i in range(len(properties)):
        tl += properties[i]["SUM(share)"]*holds[i]["price"]

    return render_template("index.html",mn =mn,properties = properties ,holds = holds,tl = tl)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        stock = lookup(request.form.get("symbol"))
        user_id = session["user_id"]
        new = db.execute(f"SELECT cash FROM users WHERE id = '{user_id}'")
        if new[0]["cash"] - stock["price"]*int(request.form.get("shares")) < 0 :
            return render_template("buy.html",message = "No cash")
        else:
            new = new[0]["cash"] - stock["price"]*int(request.form.get("shares"))
            db.execute("INSERT INTO share_hold(id,symbol,share,price) VALUES(:uid,:symbol,:share,:price)",uid = session["user_id"],symbol = stock["symbol"],
            share = request.form.get("shares"),price = stock["price"])

            db.execute(f"UPDATE users SET cash = {new} WHERE id = '{user_id}'")
            return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""
    return jsonify("TODO")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    user_id = session["user_id"]
    histories = db.execute(f"SELECT * FROM share_hold WHERE id = '{user_id}'")
    return render_template("history.html",histories = histories)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    # todo error check
    if request.method == "POST":
        stock = lookup(request.form.get("symbol"))
        return render_template("quoted.html",stock = stock)

    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        # TODO user name check
        if request.form.get("password") == request.form.get("password(again)"):
            db.execute("INSERT INTO users(username,hash) VALUES(:username,:hash)",username = request.form.get("username"),
            hash = generate_password_hash(request.form.get("password")))
            session["user_id"] = db.execute("SELECT id FROM users WHERE username = :username",username = request.form.get("username"))
            return redirect("/")
        else:
            return render_template("register.html")
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    user_id = session["user_id"]
    stocks = db.execute(f"SELECT * FROM share_hold WHERE id = '{user_id}' GROUP BY symbol")
    if request.method == "POST":
        stock = lookup(request.form.get("symbol"))
        properties = db.execute(f"SELECT SUM(share) ,symbol FROM share_hold WHERE id = '{user_id}' GROUP BY symbol HAVING symbol = :sb",
        sb = request.form.get("symbol"))

        new = db.execute(f"SELECT cash FROM users WHERE id = '{user_id}'")

        if properties[0]["SUM(share)"] < int(request.form.get("shares")) :
            return render_template("sell.html",message = "Too many shares",stocks = stocks)
        else:

            new = new[0]["cash"] + stock["price"]*int(request.form.get("shares"))
            db.execute(f"UPDATE users SET cash = {new} WHERE id = '{user_id}'")
            db.execute("INSERT INTO share_hold(id,symbol,share,price) VALUES(:uid,:symbol,:share,:price)",uid = session["user_id"],symbol = stock["symbol"],
            share = -1*int(request.form.get("shares")),price = stock["price"])

            return redirect("/")
    else:

        return render_template("sell.html",stocks = stocks)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
