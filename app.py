from flask import Flask, render_template, request, redirect, make_response, send_from_directory
import json

from model import Game

app = Flask(__name__)
game = Game()

# @app.route('/static/images/<path:filename>')
# def static(filename):
#     resp = make_response(send_from_directory('static/', filename))
#     resp.headers['Cache-Control'] = 'max-age'
#     return resp

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
        return render_template('index.html', cards=game.table.cards, rows=game.table.get_rows(), columns=game.table.get_columns(), score=game.score, deck=len(game.deck.cards)+len(game.table.cards))

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("password")
        if name and password:
            print(f"{name} tried to sign in!")
            return redirect("/")
        else:
            return redirect("/login")
    else:
        return render_template('login.html')
    
@app.route('/account', methods=["GET", "POST"])
def account():
    if request.method == "POST":
        return redirect("/account")
    else:
        test_data = {"name": "enarve", "games": 3, "sets": 24, "rank": 1}
        return render_template('account.html', data=test_data)

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
    return render_template('leaderboard.html')

@app.route('/rules')
def rules():
    return render_template('rules.html')