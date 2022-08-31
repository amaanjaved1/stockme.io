import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
import datetime
from helpers import apology, login_required, lookup, usd

def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

def transact_portfolio(transaction_type, user_id, symbol, value, shares, name, final_shares):
    response = db.execute("SELECT * FROM portfolio WHERE user_id = ? AND symbol = ?", user_id, symbol)
    if transaction_type == "purchase":
        if len(response) == 0:
            db.execute("INSERT INTO portfolio (user_id, symbol, value, shares, name) VALUES (?,?,?,?,?)", user_id, symbol, value, shares, name)
        else:
            stock = response[0]
            updated_value = stock["value"] + value
            updated_shares = stock["shares"] + shares
            db.execute("UPDATE portfolio SET value = ?, shares = ? WHERE user_id = ? AND symbol = ? AND name = ?", updated_value, updated_shares, user_id, symbol, name)
    elif transaction_type == "sell":
        if final_shares > 0:
            stock = response[0]
            updated_value = stock["value"] - value
            updated_shares = stock["shares"] - shares
            db.execute("UPDATE portfolio SET value = ?, shares = ? WHERE user_id = ? AND symbol = ? AND name = ?", updated_value, updated_shares, user_id, symbol, name)
        else:
            db.execute("DELETE FROM portfolio WHERE user_id = ? AND symbol = ? AND name = ?", user_id, symbol, name)



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

@app.context_processor
def example():
    return dict(myexample='This is an example')

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response




@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "POST":
        symbol = request.form.get("symbol") #collect stock symbol
        sharesc = request.form.get("shares") #collect number of stocks being purchased
        stock = lookup(symbol)
        #define possible errors
        if sharesc.isnumeric(): #check if purchase quantity is an integer
            sharesc = int(sharesc)
        elif isfloat(sharesc): #check if purchase quantity is a float
            sharesc = float(sharesc)
        else:
           return apology("enter a valid input for share count", 400)
        if not symbol:
            return apology("must provide ticker symbol", 400)
        if not sharesc:
            return apology("must provide number of shares", 400) #if share count is not provided
        if sharesc <= 0:
            return apology("purchase quantity must be greater than 0", 400)
        if not stock:
           return apology("stock not found", 400)
        #collect variables
        user_id = session["user_id"]
        cmd = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
        balance = cmd[0]["cash"]
        purchase_value = round(sharesc * stock["price"], 2)
        name = stock["name"]
        final_balance = balance - purchase_value
        transtype = "purchase"
        if balance > purchase_value:
            db.execute("UPDATE users SET cash = ? WHERE id = ?", final_balance, user_id)
            date = datetime.datetime.now()
            db.execute("INSERT INTO transactions (user_id, symbol, shares, price, date, type) VALUES (?,?,?,?,?,?)", user_id, symbol, sharesc, purchase_value, date, transtype)
            transact_portfolio(transtype, user_id, symbol, purchase_value, sharesc, name, None)
            flash("Your order has been succesfully fulfilled! Navigate to 'portfolio' to view this transaction")
            return redirect("/")
        else:
            return apology("insufficient funds", 400)
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    user_id = session["user_id"]
    history = db.execute("SELECT * FROM transactions WHERE user_id = ?", user_id)
    return render_template("history.html", history=history)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 400)

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


@app.route("/", methods=["GET", "POST"])
@login_required
def quote():
    if request.method == "POST":
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("must provide ticker symbol", 400)
        stock = lookup(symbol)
        if stock:
            return render_template("quoted.html", stock=stock)
        else:
           return apology("stock not found", 400)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username") #use the name property within the HTML input tag
        password = request.form.get("password")
        cpassword = request.form.get("confirmation")
        if not username:
            return apology("must provide username", 400)
        elif not password:
            return apology("must provide password", 400)
        elif not cpassword:
            return apology("must confirm password", 400)
        elif password != cpassword:
            return apology("passwords do not match", 400)
        hpassword = generate_password_hash(cpassword)
        try:
            new = db.execute("INSERT INTO users (username, hash) VALUES (?,?)", username, hpassword)
        except:
            return apology("username already exists", 400)
        session["user_id"] = new
        return redirect("/")
    else:
        return render_template("register.html")



@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    if request.method == "POST":
        user_id = session["user_id"]
        symbol = request.form.get("symbol")
        sellsharesinput = request.form.get("shares")
        sharesinput = db.execute("SELECT shares FROM portfolio WHERE user_id = ? AND symbol = ?", user_id, symbol)
        if sellsharesinput.isnumeric(): #check if purchase quantity is an integer
            sellshares = int(sellsharesinput)
        elif isfloat(sellsharesinput): #check if purchase quantity is a float
            sellshares = float(sellsharesinput)
        else:
           return apology("enter a valid input for share count", 400)
        if not symbol:
            return apology("must provide stock symbol", 400)
        elif not sellsharesinput:
            return apology("must provide share count", 400)
        shares = float(sharesinput[0]["shares"])
        if sellshares > shares:
           return apology("not enough shares", 400)
        stock = lookup(symbol)
        cmd = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
        balance = cmd[0]["cash"]
        sell_value = round(sellshares * stock["price"], 2)
        name = stock["name"]
        final_balance = balance + sell_value
        final_shares = shares - sellshares
        transtype = "sell"
        db.execute("UPDATE users SET cash = ? WHERE id = ?", final_balance, user_id)
        date = datetime.datetime.now()
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price, date, type) VALUES (?,?,?,?,?,?)", user_id, symbol, sellshares, sell_value, date, transtype)
        transact_portfolio(transtype, user_id, symbol, sell_value, sellshares, name, final_shares)
        flash("Your have succesfully sold your shares! Navigate to 'portfolio' to view this transaction")
        return redirect("/")
    else:
        user_id = session["user_id"]
        symbols = db.execute("SELECT symbol FROM portfolio WHERE user_id = ?", user_id)
        return render_template("sell.html", symbols=symbols)

@app.route("/friend", methods=["GET","POST"])
@login_required
def friend():
    if request.method == "POST":
        user_id = session["user_id"]
        my_name = db.execute("SELECT username FROM users WHERE id=?", user_id)[0]["username"]
        friend_username = request.form.get("username")
        if not friend_username:
            return apology("must provide username", 400)
        friend_name = db.execute("SELECT username FROM users WHERE username = ?", friend_username)
        if len(friend_name) == 0:
            return apology("friend not found", 400)
        if my_name == friend_name[0]["username"]:
            return apology("cannot add yourself", 400)
        previous_friends = db.execute("SELECT friends FROM users WHERE id=?", user_id)[0]["friends"]
        if previous_friends == None:
            db.execute("UPDATE users SET friends = ? WHERE id = ?", friend_name[0]["username"], user_id)
        elif friend_name[0]["username"] in previous_friends:
            return apology("already friended user", 400)
        else:
            friend_name = friend_name[0]["username"]
            updated_friends = previous_friends + f",{friend_name}"
            db.execute("UPDATE users SET friends = ? WHERE id=?", updated_friends, user_id)
        friend_list = db.execute("SELECT friends FROM users WHERE id=?", user_id)[0]["friends"].split(",")
        friend_list_status = []
        for each in friend_list:
            dicts = {}
            friend_user_id = db.execute("SELECT id FROM users WHERE username = ?", each)[0]["id"]
            port = db.execute("SELECT * FROM portfolio WHERE user_id = ?", friend_user_id)
            cash = db.execute("SELECT cash FROM users WHERE id = ?", friend_user_id)[0]
            invested = db.execute("SELECT SUM(value) FROM portfolio WHERE user_id = ?", friend_user_id)[0]
            name = db.execute("SELECT username FROM users WHERE id = ?", friend_user_id)[0]
            keys = range(4)
            values = [port, cash, invested, name]
            for i in keys:
                dicts[i] = values[i]
            friend_list_status.append(dicts)
        return render_template("friend.html", friends=friend_list_status)
    else:
        user_id = session["user_id"]
        friend_list = db.execute("SELECT friends FROM users WHERE id=?", user_id)[0]["friends"].split(",")
        friend_list_status = []
        for each in friend_list:
            dicts = {}
            friend_user_id = db.execute("SELECT id FROM users WHERE username = ?", each)[0]["id"]
            port = db.execute("SELECT * FROM portfolio WHERE user_id = ?", friend_user_id)
            cash = db.execute("SELECT cash FROM users WHERE id = ?", friend_user_id)[0]
            invested = db.execute("SELECT SUM(value) FROM portfolio WHERE user_id = ?", friend_user_id)[0]
            name = db.execute("SELECT username FROM users WHERE id = ?", friend_user_id)[0]
            keys = range(4)
            values = [port, cash, invested, name]
            for i in keys:
                dicts[i] = values[i]
            friend_list_status.append(dicts)
        return render_template("friend.html", friends=friend_list_status)

@app.route("/portfolio")
@login_required
def portfolio():
    user_id = session["user_id"]
    port = db.execute("SELECT * FROM portfolio WHERE user_id = ?", user_id)
    cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]
    invested = db.execute("SELECT SUM(value) FROM portfolio WHERE user_id = ?", user_id)[0]
    return render_template("portfolio.html", port=port, cash=cash, invested=invested, leninvested=len(invested))

if __name__ == "__main__":
    app.run(debug=True)