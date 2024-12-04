from flask import Flask
from flask import render_template
from flask import request
import json
import math
import os

app = Flask(__name__, static_url_path='', static_folder='static')

@app.route('/')
def login():

    return render_template('login.html')

@app.route('/game')
def game():
    username = request.args.get('username')

    return render_template('game.html', username=username)

@app.route('/user_details')
def user_details():

    return render_template('user_details.html')

if __name__ == "__main__":
    port = int(os.environ.get("GET", 8080))
    app.run(debug=True, port=port)
