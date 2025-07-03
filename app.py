from flask import Flask, render_template, request, redirect, session, make_response, send_from_directory
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import json
import sqlite3

from helpers import login_required
from model import Game

DATABASE = 'database.db'

def init_db():
    try:
        con = sqlite3.connect(DATABASE)
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, name TEXT NOT NULL, hash TEXT NOT NULL, games INTEGER NOT NULL DEFAULT 0, sets INTEGER NOT NULL DEFAULT 0);")
        con.commit()
        con.close()
        print("Database created.")
    except:
        print("Error while creating database.")

app = Flask(__name__)
with app.app_context():
    init_db()
game = Game()

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# @app.after_request
# def after_request(response):
#     """Ensure responses aren't cached"""
#     response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
#     response.headers["Expires"] = 0
#     response.headers["Pragma"] = "no-cache"
#     return response

# @app.route('/static/images/<path:filename>')
# def static(filename):
#     resp = make_response(send_from_directory('static/', filename))
#     resp.headers['Cache-Control'] = 'max-age'
#     return resp

def logged_in():
    if session.get("user_id") != None:
        return True
    else:
        return False

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if request.form.get("restart"):
            game.restart()
            return redirect("/")
        elif request.form.get("deal_more"):
            game.deal(3)
            return redirect("/")
        elif request.json.get("update"):
            result = game.move_set_to_pile()
            return json.dumps(result)

    else:
        return render_template('index.html', cards=game.table.cards, rows=game.table.get_rows(), columns=game.table.get_columns(), score=game.score, deck=len(game.deck.cards)+len(game.table.cards), login=logged_in())

@app.route('/login', methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    if request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("password")
        if name and password:
            # Query database for username
            con = sqlite3.connect(DATABASE)
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            res = cur.execute("SELECT * FROM users WHERE name = ?;", (name,))
            users = res.fetchall()
            
            if users:
                # try to login or return
                hash = users[0]["hash"]
                if check_password_hash(hash, password):
                    session["user_id"] = users[0]["id"]
                else:
                    return redirect("/login")
            else:
                # register new user
                hash = generate_password_hash(password)
                cur.execute("INSERT INTO users (name, hash) VALUES (?, ?);", (name, hash, ))
                con.commit()
                res = cur.execute("SELECT * FROM users WHERE name = ?;", (name, ))
                user = res.fetchone()
                print(user)
                if user:
                    session["user_id"] = user["id"]

            con.close()
            return redirect("/")
        else:
            return redirect("/login")
    else:
        return render_template('login.html', login=logged_in())
    
@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")
    
@app.route('/account', methods=["GET", "POST"])
@login_required
def account():
    user_id = session.get("user_id")
    if request.method == "POST":
        if user_id:
            name = request.form.get("name")
            password = request.form.get("password")

            # check something
            
            con = sqlite3.connect(DATABASE)
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            res = cur.execute("SELECT name, hash FROM users WHERE id = ?;", (user_id, ))
            user = dict(res.fetchone())

            if name:
                if user.get("name") != name:
                    cur.execute("UPDATE users SET name = ? WHERE id = ?;", (name, user_id, ))
                    con.commit()
            
            if password:
                if not check_password_hash(user.get("hash"), password):
                    new_hash = generate_password_hash(password)
                    cur.execute("UPDATE users SET hash = ? WHERE id = ?;", (new_hash, user_id, ))
                    con.commit()

            con.close()
            return redirect("/account")
        else:
            return redirect("/account")
    else:
        con = sqlite3.connect(DATABASE)
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        if user_id:
            res = cur.execute("SELECT * FROM users WHERE id = ?", (user_id, ))
            user = res.fetchone()
            if user:
                data = dict(user)
                rank_res = cur.execute("SELECT rank FROM (SELECT *, ROW_NUMBER() OVER (ORDER BY games DESC, sets DESC) as rank FROM users ORDER BY games DESC, sets DESC) WHERE id = ?;", (user_id,))
                rank_data = rank_res.fetchone()
                data["rank"] = rank_data["rank"]
                con.close()
                return render_template('account.html', data=data, login=logged_in())
            else:
                con.close()
                return redirect("/logout")
        else:
            return redirect("/")

@app.route('/data/compare', methods=["POST"])
def compare():
    result = False
    data = request.json
    # TODO: check if received cards are on the table
    selection = data.get("selection")
    print(selection)
    if selection:
        selected_cards = []
        for id in selection:
            card = game.table.get_card(id)
            if card:
                selected_cards.append(card)
        result = game.compare(selected_cards)
        if result:
            game.take_set_and_replace(selected_cards)

            # Update user stats if logged in
            user_id = session.get("user_id")
            if user_id:
                con = sqlite3.connect(DATABASE)
                con.row_factory = sqlite3.Row
                cur = con.cursor()
                res = cur.execute("SELECT * FROM users WHERE id = ?;", (user_id, ))
                user = res.fetchone()
                sets = dict(user)["sets"]
                sets+=1
                cur.execute("UPDATE users SET sets = ? WHERE id = ?;", (sets, user_id, ))
                con.commit()
                con.close()

    return json.dumps(result)

@app.route('/data/check_state', methods=["POST"])
def check_state():
    if len(game.deck.cards) > 0:
        return json.dumps(False)
    else:
        game_end = not game.check_sets()
        if game_end:

            # Update user stats if logged in
            user_id = session.get("user_id")
            if user_id:
                con = sqlite3.connect(DATABASE)
                con.row_factory = sqlite3.Row
                cur = con.cursor()
                res = cur.execute("SELECT * FROM users WHERE id = ?;", (user_id, ))
                user = res.fetchone()
                games = dict(user)["games"]
                games+=1
                cur.execute("UPDATE users SET games = ? WHERE id = ?;", (games, user_id, ))
                con.commit()
                con.close()

            game.restart()
        return json.dumps(game_end)

@app.route('/leaderboard')
def leaderboard():
    con = sqlite3.connect(DATABASE)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    res = cur.execute("SELECT *, ROW_NUMBER() OVER (ORDER BY games DESC, sets DESC) as rank FROM users ORDER BY games DESC, sets DESC;")
    users = res.fetchall()
    userdicts = []
    for user in users:
        userdicts.append(dict(user))
    con.close()
    return render_template('leaderboard.html', users=userdicts, login=logged_in())

@app.route('/rules')
def rules():
    return render_template('rules.html', login=logged_in())