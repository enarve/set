from flask import Flask, render_template

from model import Card

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', rows=4, columns=3)

@app.route('/leaderboard')
def leaderboard():
    return render_template('leaderboard.html')

@app.route('/rules')
def rules():
    return render_template('rules.html')