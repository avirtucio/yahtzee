from flask import jsonify
from flask import request, render_template

from Models import Game_Model
yahtzeeDB = './yahtzeeDB.db'
Game = Game_Model.Game(yahtzeeDB, "games")

def users_games(username):
    return render_template("user_games.html")

def games():
    if (request.method == "POST"):
        print("request method was post")
        print(request.form)
        return render_template("user_games.html")