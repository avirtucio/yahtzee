from flask import jsonify
from flask import request, render_template

from models import User_Model, Scorecard_Model
yahtzeeDB = './Models/yahtzeeDB.db'
User = User_Model.User(yahtzeeDB, "users")
Scorecard = Scorecard_Model.Scorecard(yahtzeeDB, "scorecards", "users", "games")

def login():
    # curl "http://127.0.0.1:5000"   
    print(f"request.url={request.url}")
    print("username and password", request.args.get('username'), request.args.get('password'))

    username = request.args.get('username')
    password = request.args.get('password')

    if (username):
        get_user_data_packet = User.get(username=username)
        print("get user packet", get_user_data_packet)
        if (get_user_data_packet["status"] == "success"):
            if (get_user_data_packet["data"]["password"] == password):
                all_users_games = Scorecard.get_all_user_game_names(username)["data"]
                
                all_game_scores = {}
                for game_name in all_users_games:
                    game_score = Scorecard.tally_score(Scorecard.get(f"{game_name}|{username}")["data"]["categories"])
                    all_game_scores[game_name]=game_score

                    all_game_scores = {game_name: score for game_name, score in sorted(all_game_scores.items(), key=lambda item: item[1], reverse=True)}
                return render_template('user_games.html', username=username, all_users_games=all_users_games, all_game_scores=all_game_scores)
            else:
                return render_template('login.html', error = "incorrect password")
        else:
            return render_template('login.html', error = "user name doesnt exist")
    else:
        return render_template('login.html')

    