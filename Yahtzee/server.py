from flask import Flask
from flask import render_template
from flask import request
import json
import math
import os
import sys

from Controllers import GameController, ScorecardController, SessionController, UserController

#Connect Controller definitions
fpath = os.path.join(os.path.dirname(__file__), 'Controllers')
sys.path.append(fpath)
fpath = os.path.join(os.path.dirname(__file__), 'Models')
sys.path.append(fpath)
app = Flask(__name__, static_url_path='', static_folder='static')

#session router
app.add_url_rule('/', view_func=SessionController.login, methods = ['GET'])
app.add_url_rule('/login', view_func=SessionController.login, methods = ['GET'])

#game router
app.add_url_rule('/games/<username>', view_func=GameController.users_games, methods = ['GET'])
app.add_url_rule('/games', view_func=GameController.games, methods = ['GET', 'POST'])

# #scorecard router
# app.add_url_rule('/', view_func=SessionController.login, methods = ['GET'])
# app.add_url_rule('/login', view_func=SessionController.login, methods = ['GET'])

#user router
app.add_url_rule('/users', view_func=UserController.user, methods = ['GET', 'POST'])
app.add_url_rule('/users/<username>', view_func=UserController.single_user, methods = ['GET', 'POST'])
app.add_url_rule('/users/delete/<username>', view_func=UserController.delete_user, methods = ['GET'])


# @app.route('/')
# def login():

#     return render_template('login.html')

# @app.route('/games:<username>')
# def game():
#     username = request.form.get('username')

#     return render_template('game.html', username=username)

@app.route('/user_details')
def user_details():

    return render_template('user_details.html')

if __name__ == "__main__":
    port = int(os.environ.get("GET", 8080))
    app.run(debug=True, port=port)
