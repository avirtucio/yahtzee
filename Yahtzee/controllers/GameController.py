from flask import jsonify
from flask import request, render_template

from models import Game_Model, Scorecard_Model, User_Model
yahtzeeDB = './Models/yahtzeeDB.db'
Game = Game_Model.Game(yahtzeeDB, "games")
User = User_Model.User(yahtzeeDB, "users")
Scorecard = Scorecard_Model.Scorecard(yahtzeeDB, "scorecards", "users", "games")

def users_games(username):
    if (User.exists(username=username)["data"]==False):
        return render_template("login.html", error="user does not exist")
    else:
        all_users_games = Scorecard.get_all_user_game_names(username)["data"]
        
        all_game_scores = {}
        for game_name in all_users_games:
            game_score = Scorecard.tally_score(Scorecard.get(f"{game_name}|{username}")["data"]["categories"])
            all_game_scores[game_name]=game_score

            all_game_scores = {game_name: score for game_name, score in sorted(all_game_scores.items(), key=lambda item: item[1], reverse=True)}

        return render_template("user_games.html", username=username, all_users_games=all_users_games,
                               all_game_scores=all_game_scores)

def create_game():
    username = request.form.get("username")
    gamename = request.form.get("create_game_name")

    if (User.exists(username=username)["data"] == False):
        return render_template("user_games.html", feedback="user does not exist")
    elif (Game.exists(game_name=gamename)["data"] == True):
        all_users_games = Scorecard.get_all_user_game_names(username)["data"]
        return render_template("user_games.html", feedback="game already exists", username=username, all_users_games=all_users_games)
    else:
        game_name = Game.create({"name":gamename})["data"]["name"]
        user_id = str(User.get(username=username)["data"]["id"])
        game_id = str(Game.get(game_name=game_name)["data"]["id"])
        
        new_scorecard = Scorecard.create(game_id, user_id, f"{game_name}|{username}")
        
        all_users_games = Scorecard.get_all_user_game_names(username)["data"]
       
        all_game_scores = {}
        for game_name in all_users_games:
            game_score = Scorecard.tally_score(Scorecard.get(f"{game_name}|{username}")["data"]["categories"])
            all_game_scores[game_name]=game_score

            all_game_scores = {game_name: score for game_name, score in sorted(all_game_scores.items(), key=lambda item: item[1], reverse=True)}
        return render_template("user_games.html", username=username, game_name=game_name, all_users_games=all_users_games,
                               all_game_scores=all_game_scores)
    
def join_game():
    username = request.json.get("username")
    game_name = request.json.get("game_name")
    print("game_controller, join_game, username and game_name:", username, game_name)
    all_users_games_old = Scorecard.get_all_user_game_names(username)["data"]

    print("game controller, join game, check if game exists", Game.exists(game_name=game_name))
    
    if (User.exists(username=username)["data"] == False):
        print("game controller, join game, username does not exist")
        return jsonify({'status': 'error', 'message': 'username does not exist'})
        # return render_template("user_games.html", feedback="user does not exist")
    elif (Game.exists(game_name=game_name)["data"] == False):
        print("game controller, join game, game does not exist")
        return jsonify({'status': 'error', 'message': 'game does not exist'})
        # return render_template("user_games.html", feedback="game does not exist")
    else:
        user_id = str(User.get(username=username)["data"]["id"])
        game_id = str(Game.get(game_name=game_name)["data"]["id"])
        new_scorecard = Scorecard.create(game_id, user_id, f"{game_name}|{username}")
        all_users_games = Scorecard.get_all_user_game_names(username)["data"]
        all_new_games = set(all_users_games).symmetric_difference(set(all_users_games_old))
        # print("game controller, join game, all users games old", all_users_games_old)
        # print("game controller, join game, all users games", all_users_games)
        # print("game controller, join game, all new games", all_new_games)
        return jsonify(list(all_new_games))
        # return render_template("user_games.html", username=username, game_name=game_name, all_users_games=all_users_games)

def delete_game(game_name, username):
    scorecard_name=f"{game_name}|{username}"
    scorecard_id=Scorecard.get(name=scorecard_name)["data"]["id"]
    deleted_scorecard=Scorecard.remove(scorecard_id)["data"]
    deleted_game=Game.remove(game_name)

    all_users_games = Scorecard.get_all_user_game_names(username)["data"]
    
    all_game_scores = {}
    for game_name in all_users_games:
        game_score = Scorecard.tally_score(Scorecard.get(f"{game_name}|{username}")["data"]["categories"])
        all_game_scores[game_name]=game_score

        all_game_scores = {game_name: score for game_name, score in sorted(all_game_scores.items(), key=lambda item: item[1], reverse=True)}
    
    return render_template("user_games.html", username=username, all_users_games=all_users_games, all_game_scores=all_game_scores)