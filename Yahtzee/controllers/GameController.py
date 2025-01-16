from flask import jsonify
from flask import request, render_template

from models import Game_Model, Scorecard_Model, User_Model
yahtzeeDB = './Models/yahtzeeDB.db'
Game = Game_Model.Game(yahtzeeDB, "games")
User = User_Model.User(yahtzeeDB, "users")
Scorecard = Scorecard_Model.Scorecard(yahtzeeDB, "scorecards", "users", "games")

def users_games(username):
    all_users_games = Scorecard.get_all_user_game_names(username)["data"]
    return render_template("user_games.html", username=username, all_users_games=all_users_games)

def create_game():
    username = request.form.get("username")
    game_name = Game.create({"name":request.form.get("create_game_name")})["data"]["name"]
    all_users_games = Scorecard.get_all_user_game_names(username)["data"]
    return render_template("user_games.html", username=username, game_name=game_name, all_users_games=all_users_games)
    
def join_game():
    username = request.form.get("username")
    game_name = request.form.get("join_game_name")
    #check if usernames and gamenames actually exist
    print('alsdjnglkadsjnglkdjasglkadsjgkldasjgkladsjgdalksjh')
    print(type(username))
    print(User.get(username=username))
    user_id = str(User.get(username=username)["data"]["id"])
    game_id = str(Game.get(game_name=game_name)["data"]["id"])
    print("about to make new scorecard in join game")
    new_scorecard = Scorecard.create(game_id, user_id, f"{game_name}|{username}")
    print("join game, new scorecard:", new_scorecard)
    all_users_games = Scorecard.get_all_user_game_names(username)["data"]
    return render_template("user_games.html", username=username, game_name=game_name, all_users_games=all_users_games)

def delete_game(game_name, username):
    scorecard_name=f"{game_name}|{username}"
    scorecard_id=Scorecard.get(name=scorecard_name)["data"]["id"]
    deleted_game=Scorecard.remove(scorecard_id)["data"]

    all_users_games = Scorecard.get_all_user_game_names(username)["data"]
    return render_template("user_games.html", username=username, all_users_games=all_users_games)