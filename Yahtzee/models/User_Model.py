# Arlo Virtucio #

import sqlite3
import random

class User:
    def __init__(self, db_name, table_name):
        self.db_name =  db_name
        print("user model construcotr", db_name)
        self.max_safe_id = 9007199254740991 #maximun safe Javascript integer
        self.table_name = table_name
    
    def initialize_table(self):
        print("user initialize table", self.db_name)
        db_connection = sqlite3.connect(self.db_name)
        cursor = db_connection.cursor()
        schema=f"""
                CREATE TABLE {self.table_name} (
                    id INTEGER PRIMARY KEY UNIQUE,
                    email TEXT UNIQUE,
                    username TEXT UNIQUE,
                    password TEXT
                );
                """
        cursor.execute(f"DROP TABLE IF EXISTS {self.table_name};")
        results=cursor.execute(schema)
        db_connection.close()
    
    def exists(self, username=None, id=None):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()
        #######
            #print("user model, exists, self.db_name", self.db_name)
            if (username):
                print("user model, exists, checking if user name exists", username)
                print("user model, exists, self.table_name", self.table_name)
                results = cursor.execute(f"SELECT * FROM {self.table_name} WHERE username = '{username}';").fetchall()
                print("results", results)
            elif (id):
                results = cursor.execute(f"SELECT * FROM {self.table_name} WHERE id = {id};").fetchall()
            
            if (results):
                return {"status":"success",
                    "data":True}
            else:
                return {"status":"success",
                    "data":False}
        #######
        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        finally:
            db_connection.close()

    def create(self, user_info):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()
            user_id = random.randint(0, self.max_safe_id)

            print("user_model, create function was called, db_connection was established")

            # TODO: check to see if id already exists!!
            
            if ((self.exists(id=user_id)["data"] == False) and (self.exists(username=user_info["username"])["data"] == False)):
                user_data = (user_id, user_info["email"], user_info["username"], user_info["password"])
                #are you sure you have all data in the correct format?
                username_check = True
                for character in user_data[2]:
                    if ((character.isalnum() == False) and (character != "_") and (character != "-")):
                        username_check = False
                        break
                password_check = True
                if (len(user_data[3]) < 8):
                    password_check = False
                email_check = True
                email_array = list(user_data[1])
                if ((" " in email_array) or ("@" not in email_array) or("." not in email_array)):
                    email_check = False

                email_list = []
                results = cursor.execute(f"SELECT email FROM {self.table_name};").fetchall()
                for tuple in results:
                    email_list.append(tuple[0])
                if user_data[1] in email_list:
                    email_check = False

                if ((username_check == True) and (password_check == True) and (email_check == True)):
                    cursor.execute(f"INSERT INTO {self.table_name} VALUES (?, ?, ?, ?);", user_data)
                    db_connection.commit()
                    
                    print("usermodel, create function", self.db_name)
                    return {"status": "success",
                        "data": self.to_dict(user_data)
                        }
                else:
                    return {"status": "error",
                        "data": "either bad email bad username or bad password"
                        }
            else:
                return {"status": "error",
                    "data": "something either id or username already exists"
                    }
        
        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        
        finally:
            db_connection.close()
    
    def get(self, username=None, id=None):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()
        ####### check if exists first
            if (username):
                if (self.exists(username=username)["data"] == True):
                    results = cursor.execute(f"SELECT * FROM {self.table_name} WHERE username = '{username}';").fetchall()
                    return {"status":"success",
                    "data":self.to_dict(results[0])}
                else:
                    return {"status":"error",
                    "data":"user name doesnt exist"}
            elif (id):
                if (self.exists(id=id)["data"] == True):
                    results = cursor.execute(f"SELECT * FROM {self.table_name} WHERE id = '{id}';").fetchall()
                    return {"status":"success",
                    "data":self.to_dict(results[0])}
            else:
                return {"status":"error",
                    "data":"user id doesnt exist"}
        #######
        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        finally:
            db_connection.close()
    
    def get_all(self): 
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

            user_info_list = []
            results = cursor.execute(f"SELECT * FROM {self.table_name};").fetchall()
            for user_tuple in results:
                user_info_list.append(self.to_dict(user_tuple))
            
            return {"status":"success",
                    "data":user_info_list}
        
        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        finally:
            db_connection.close()

    def update(self, user_info): 
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

            if (self.exists(id=user_info["id"])["data"] == True):
                duplicate_username_check = cursor.execute(f"SELECT * FROM {self.table_name} WHERE username='{user_info['username']}' AND id<>'{user_info['id']}'").fetchall()
                duplicate_email_check = cursor.execute(f"SELECT * FROM {self.table_name} WHERE email='{user_info['email']}' AND id<>'{user_info['id']}'").fetchall()
                for character in user_info["username"]:
                    print("user model update, checking character in new user:", character)
                    if ((character.isalnum() == False) and (character != "_") and (character != "-")):
                        return {"status":"error",
                                "data":"invalid new username"}
                    elif (duplicate_username_check):
                        return {"status":"error",
                                "data":"username already exists"}
                    
                cursor.execute(f"UPDATE {self.table_name} SET 'username'='{user_info['username']}' WHERE id = '{user_info['id']}'")
                db_connection.commit()
                
            
                if (len(user_info["password"]) < 8):
                    print("user model, update, attempting to update password to:", user_info["password"])
                    return {"status":"error",
                            "data":"invalid new password"}
                else:
                    cursor.execute(f"UPDATE {self.table_name} SET 'password'='{user_info['password']}' WHERE id = '{user_info['id']}'")
                    db_connection.commit()
                
            
                email_array = list(user_info["email"])
                if ((" " in email_array) or ("@" not in email_array) or("." not in email_array)):
                    return {"status":"error",
                            "data":"invalid new email"}
                elif (duplicate_email_check):
                    return {"status":"error",
                            "data":"email already in use"}
                else:
                    cursor.execute(f"UPDATE {self.table_name} SET 'email'='{user_info['email']}' WHERE id = '{user_info['id']}'")
                    db_connection.commit()
            

                return {"status":"success",
                        "data":self.get(id=user_info['id'])["data"]}
            else:
                return {"status":"error",
                        "data":"user doesnt exist"}

        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        finally:
            db_connection.close()

    def remove(self, username): 
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()
            
            if (self.exists(username=username)["data"] == True):
                deleted_user = self.get(username=username)["data"]
                cursor.execute(f"DELETE FROM {self.table_name} WHERE username = '{username}';")
                db_connection.commit()

                return {"status":"success",
                        "data":deleted_user}
            else:
                return {"status":"error",
                    "data":"user name doesnt exist"}

        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        finally:
            db_connection.close()
    
    def to_dict(self, user_tuple):
        '''Utility function which converts the tuple returned from a SQLlite3 database
           into a Python dictionary
        '''
        user_dict={}
        #print("usertuple",user_tuple, user_tuple[0], type(user_tuple[1]))
        if user_tuple:
            user_dict["id"]=user_tuple[0]
            user_dict["email"]=user_tuple[1]
            user_dict["username"]=user_tuple[2]
            user_dict["password"]=user_tuple[3]
        return user_dict

if __name__ == '__main__':
    import os
    print("Current working directory:", os.getcwd())
    DB_location=f"{os.getcwd()}yahtzeeDB.db"
    table_name = "users"
    
    Users = User(DB_location, table_name) 
    Users.initialize_table()

    user_details={
        "email":"justin.gohde@trinityschoolnyc.org",
        "username":"justingohde",
        "password":"123TriniT"
    }
    results = Users.create(user_details)
    # id = results["data"]["id"]
    # print(results, id)

    # new_user_details={
    #     "id": id,
    #     "email":"justin.gohde@trinityschoolnyc.org",
    #     "username":"justingohdeeeeeee",
    #     "password":"123TriniT"
    # }
    
    print(Users.remove("justingohde"))
