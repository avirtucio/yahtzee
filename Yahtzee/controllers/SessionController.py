from flask import jsonify
from flask import request, render_template

from Models import User_Model
yahtzeeDB = './yahtzeeDB.db'
User = User_Model.User(yahtzeeDB, "users")

def login():
    # curl "http://127.0.0.1:5000"   
    print(f"request.url={request.url}")
    print("username and password", request.args.get('username'), request.args.get('password'))

    username = request.args.get('username')
    password = request.args.get('password')

    if (username):
        get_user_data_packet = User.get(username=username)
        
        if (get_user_data_packet["status"] == "success"):
            if (get_user_data_packet["data"]["password"] == password):
                return render_template('user_games.html')
            else:
                return render_template('login.html', error = "incorrect password")
        else:
            return render_template('login.html', error = "user name doesnt exist")
    else:
        return render_template('login.html')

    