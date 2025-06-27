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

    else:
        return render_template('index.html', cards=game.table.cards, rows=game.table.get_rows(), columns=game.table.get_columns())

@app.route('/data/compare', methods=["POST"])
def compare():
    data = request.json
    # TODO: check if received cards are on the table
    
    print(data)
    return json.dumps(True)

@app.route('/leaderboard')
def leaderboard():
    return render_template('leaderboard.html')

@app.route('/rules')
def rules():
    return render_template('rules.html')