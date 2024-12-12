from flask import jsonify
from flask import request, render_template

from Models import User_Model
yahtzeeDB = './yahtzeeDB.db'
User = User_Model.User(yahtzeeDB, "users")

def user():
    print(f"request.method= {request.method} request.url={request.url}")
    print(f"request.url={request.query_string}")
    print("request.form:", request.form)
    if (request.method == "POST"):
        print("post request inititated")
        user_info = {"email": request.form["email"],
                     "username": request.form["username"], 
                     "password": request.form["password"]
                     }
        print("user_info:", user_info)
        
        create_user_data_packet = User.create(user_info)
        
        if (create_user_data_packet["status"] == "success"):
            return render_template('user_games.html', username = request.form["username"])
        else:
            return render_template('user_details.html')
    else:
        return render_template('user_details.html')