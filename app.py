from flask import Flask, render_template, request, redirect, session, make_response, send_from_directory
from flask_session import Session
import json

from helpers import login_required
from model import Game

app = Flask(__name__)
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
            print("update")
            result = game.move_set_to_pile()
            return json.dumps(result)

    else:
        print("logged in?", logged_in())
        return render_template('index.html', cards=game.table.cards, rows=game.table.get_rows(), columns=game.table.get_columns(), score=game.score, deck=len(game.deck.cards)+len(game.table.cards), login=logged_in())

@app.route('/login', methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    if request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("password")
        print(name, password)
        if name and password:
            # Query database for username
            rows = [{"id": 0}]
            # Ensure username exists and password is correct
            #
            session["user_id"] = rows[0]["id"]
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
    if request.method == "POST":
        return redirect("/account")
    else:
        test_data = {"name": "enarve", "games": 3, "sets": 24, "rank": 1}
        return render_template('account.html', data=test_data, login=logged_in())

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
            selected_cards.append(card)
        result = game.compare(selected_cards)
        if result:
            game.take_set_and_replace(selected_cards)
    return json.dumps(result)

@app.route('/data/check_state', methods=["POST"])
def check_state():
    if len(game.deck.cards) > 0:
        return json.dumps(False)
    else:
        game_end = not game.check_sets()
        if game_end:
            game.restart()
        return json.dumps(game_end)

@app.route('/leaderboard')
def leaderboard():
    return render_template('leaderboard.html', login=logged_in())

@app.route('/rules')
def rules():
    return render_template('rules.html', login=logged_in())