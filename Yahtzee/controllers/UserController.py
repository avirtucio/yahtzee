from flask import jsonify
from flask import request, render_template

from Models import User_Model
yahtzeeDB = './yahtzeeDB.db'
User = User_Model.User(yahtzeeDB, "users")

def user():
    if (request.method == "POST"):
        user_info = {"email": request.form,
                     "username": , 
                     "password":
                     }

    return render_template('user_details.html')