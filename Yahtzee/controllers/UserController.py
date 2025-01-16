from flask import jsonify
from flask import request, render_template
import os

from models import User_Model
yahtzeeDB = './Models/yahtzeeDB.db'
User = User_Model.User(yahtzeeDB, "users")

def user():
    print(f"request.method= {request.method} request.url={request.url}")
    print(f"request.url={request.query_string}")
    if (request.method == "POST"):
        user_info = {"email": request.form.get("email"),
                     "username": request.form.get("username"), 
                     "password": request.form.get("password")
                     }
        print("user_info:", user_info)
        
        create_user_data_packet = User.create(user_info)
        
        if (create_user_data_packet["status"] == "success"):
            return render_template('user_games.html', username = request.form["username"], context='create user')
        else:
            return render_template('user_details.html', feedback = create_user_data_packet["data"], context='create user')
   
    elif (request.method == "GET"):
        print("request method was get")
        
        return render_template('user_details.html', context='create user')
    # print(f"request.method= {request.method} request.url={request.url}")
    # print(f"request.url={request.query_string}")
    # print("request.form:", request.form)
    # if (request.method == "POST"):
    #     print("post request inititated")
    #     user_info = {"email": request.form.get("email"),
    #                  "username": request.form.get("username"), 
    #                  "password": request.form.get("password")
    #                  }
    #     print("user_info:", user_info)
        
    #     create_user_data_packet = User.create(user_info)
        
    #     if (create_user_data_packet["status"] == "success"):
    #         return render_template('user_games.html', username = request.form["username"])
    #     else:
    #         return render_template('user_details.html')
    # else:
    #     return render_template('user_details.html')

def single_user(username):

    if (request.method == "GET"):
        print("request method was get")
        get_user_data_packet = User.get(username=username)
        if (get_user_data_packet["status"] == "success"):
            user_name = get_user_data_packet["data"]['username']
            user_password = get_user_data_packet["data"]['password']
            user_email = get_user_data_packet["data"]['email']
            user_id = get_user_data_packet["data"]['id']

            return render_template('user_details.html', context='get user', feedback=get_user_data_packet["data"], 
                                   user_name=user_name, user_password=user_password, user_email=user_email,
                                   user_id=user_id, username=username)

        elif (get_user_data_packet["status"] == "error"):
            return render_template('user_details.html', context='get user', feedback=get_user_data_packet["data"])

    elif (request.method == "POST"):
        print("request method was post")
        print(f"{username} in submit request")
        user_id = User.get(username=username)["data"]["id"]
        print(user_id)
        user_info = {"id": user_id,
                     "email": request.form.get("email"),
                     "username": request.form.get("username"), 
                     "password": request.form.get("password")
                     }
        update_user_data_packet = User.update(user_info)
        print(update_user_data_packet)
        if (update_user_data_packet["status"] == "success"):
            get_user_data_packet = User.get(id=user_id)
            user_name = get_user_data_packet["data"]['username']
            user_password = get_user_data_packet["data"]['password']
            user_email = get_user_data_packet["data"]['email']
            user_id = get_user_data_packet["data"]['id']

            return render_template('user_details.html', context='get user', feedback=get_user_data_packet["data"], 
                                   user_name=user_name, user_password=user_password, user_email=user_email,
                                   user_id=user_id, username=username)
        else:
            return render_template('user_details.html', context='get user', username=username,
                                   feedback=update_user_data_packet["data"])

def delete_user(username):
    if (User.exists(username=username)["data"]==True):
        User.remove(username)
        return render_template('login.html', username=username)
    else:
        return render_template('user_details.html', feedback="user does not exist")