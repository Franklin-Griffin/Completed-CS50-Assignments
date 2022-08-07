import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    purchases = db.execute("SELECT symbol, SUM(shares) FROM purchases WHERE id = ? GROUP BY symbol HAVING SUM(shares) > 0", session["user_id"])
    subtotal = 0
    body = []
    for row in purchases:
        symbol = row["symbol"]
        response = lookup(symbol)
        name = response["name"]
        shares = int(row["SUM(shares)"])
        price = float(response["price"])
        total = price * shares
        body.append({"symbol": symbol, "name": name, "shares": shares, "price": usd(price), "total": usd(total)})
        subtotal += total
    cash = float(db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"])
    total = cash + subtotal
    return render_template("index.html", body=body, cash=usd(cash), total=usd(total))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "GET":
        return render_template("buy.html")

    # POST
    symbol = request.form.get("symbol")
    shares = request.form.get("shares")
    if symbol == "":
        return apology("Please enter a symbol")
    if not shares.isnumeric():
        return apology("Please enter a number for shares")
    if int(shares) != float(shares):
        return apology("Number of shares must be an integer")
    shares = int(shares)
    if shares <= 0:
        return apology("Number of shares must be positive")
    response = lookup(symbol)
    if response == None:
        return apology("Symbol does not exist")
    price = response["price"] * shares
    cash = int(db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"])
    if price > cash:
        return apology("You do not have enough money to make this purchase")
    db.execute("UPDATE users SET cash = ? WHERE id = ?", cash-price, session["user_id"])
    db.execute("INSERT INTO purchases (symbol, shares, id, transacted) VALUES (?, ?, ?, CURRENT_TIMESTAMP)",
               symbol, shares, session["user_id"])
    return redirect("/")


@app.route("/history")
@login_required
def history():
    purchases = db.execute("SELECT symbol, shares, transacted FROM purchases WHERE id = ?", session["user_id"])
    body = []
    for row in purchases:
        symbol = row["symbol"]
        response = lookup(symbol)
        shares = int(row["shares"])
        price = float(response["price"])
        transacted = row["transacted"]
        body.append({"symbol": symbol, "shares": shares, "price": usd(price), "transacted": transacted})
    return render_template("history.html", body=body)


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
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

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
    if request.method == "GET":
        return render_template("quote.html")

    # POST
    symbol = request.form.get("symbol")
    response = lookup(symbol)
    if response == None:
        return apology("This symbol does not exist")
    return render_template("quoted.html", name=response["name"], price=usd(response["price"]), symbol=response["symbol"])


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    name = request.form.get("username")
    password = request.form.get("password")
    confirm = request.form.get("confirmation")
    if name == "":
        return apology("Please enter a name")
    elif len(db.execute("SELECT * FROM users WHERE username = ?", name)) != 0:
        return apology("Username already exists")
    elif password == "":
        return apology("Please enter a password")
    elif confirm == "":
        return apology("Please enter a confirmation password")
    elif not password == confirm:
        return apology("Passwords do not match")
    # Personal touch: passwords must have 8 characters, a number, a letter, and a special character
    if len(password) < 8:
        return apology("Your password is not long enough")
    number = False
    letter = False
    special = False
    for i in password:
        if i.isnumeric():
            number = True
        elif i.isalpha():
            letter = True
        else:
            # Special character
            special = True
    if not number:
        return apology("Your password must contain a number")
    if not letter:
        return apology("Your password must contain a letter")
    if not special:
        return apology("Your password must contain a special character")
    # Register user and log in
    db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", name, generate_password_hash(password))
    session["user_id"] = db.execute("SELECT * FROM users WHERE username = ?", name)[0]["id"]
    return redirect("/")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    if request.method == "GET":
        symbols = db.execute("SELECT symbol FROM purchases WHERE id = ? GROUP BY symbol HAVING SUM(shares) > 0", session["user_id"])
        return render_template("sell.html", symbols=symbols)

    # POST
    symbol = request.form.get("symbol")
    shares = request.form.get("shares")
    if symbol == "":
        return apology("Please enter a symbol")
    if not shares.isnumeric():
        return apology("Please enter a number for shares")
    if int(shares) != float(shares):
        return apology("Number of shares must be an integer")
    shares = int(shares)
    if shares <= 0:
        return apology("Number of shares must be positive")
    response = lookup(symbol)
    if response == None:
        return apology("Symbol does not exist")
    userShares = db.execute("SELECT SUM(shares) FROM purchases WHERE id = ? AND symbol = ? GROUP BY symbol",
                            session["user_id"], symbol)[0]["SUM(shares)"]
    if shares > userShares:
        return apology("You do not have enough shares to sell")
    earnings = response["price"] * shares
    cash = int(db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"])
    db.execute("UPDATE users SET cash = ? WHERE id = ?", cash+earnings, session["user_id"])
    db.execute("INSERT INTO purchases (symbol, shares, id, transacted) VALUES (?, ?, ?, CURRENT_TIMESTAMP)",
               symbol, -shares, session["user_id"])

    return redirect("/")
