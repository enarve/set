from flask import Flask, render_template, request, redirect
import json

from model import Game

app = Flask(__name__)
game = Game()

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
            if result:
                game.deal(3)
            return json.dumps(result)

    else:
        return render_template('index.html', cards=game.table.cards, rows=game.table.get_rows(), columns=game.table.get_columns())

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
            game.take_set(selected_cards)
    return json.dumps(result)

@app.route('/leaderboard')
def leaderboard():
    return render_template('leaderboard.html')

@app.route('/rules')
def rules():
    return render_template('rules.html')