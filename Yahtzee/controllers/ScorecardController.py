from flask import jsonify
from flask import request

from models import Game_Model, Scorecard_Model, User_Model
yahtzeeDB = './Models/yahtzeeDB.db'
Game = Game_Model.Game(yahtzeeDB, "games")
User = User_Model.User(yahtzeeDB, "users")
Scorecard = Scorecard_Model.Scorecard(yahtzeeDB, "scorecards", "users", "games")

def update_scorecard(scorecard_name):
    categories = request.json.get("categories") #probably json to object it or smtg
    scorecard_id = Scorecard.get(name=scorecard_name)["data"]["id"]
    new_scorecard = Scorecard.update(scorecard_id, categories=categories)

    return new_scorecard