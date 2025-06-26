from flask import Flask, render_template

from model import Game

app = Flask(__name__)
game = Game()

@app.route('/')
def index():
    return render_template('index.html', cards=game.deck.cards, rows=4, columns=3)

@app.route('/leaderboard')
def leaderboard():
    return render_template('leaderboard.html')

@app.route('/rules')
def rules():
    return render_template('rules.html')