# Arlo Virtucio #

import sqlite3
import random

class User:
    def __init__(self, db_name, table_name):
        self.db_name =  db_name
        self.max_safe_id = 9007199254740991 #maximun safe Javascript integer
        self.table_name = table_name
    
    def initialize_table(self):
        print(self.db_name)
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
            if (username):
                results = cursor.execute(f"SELECT * FROM {self.table_name} WHERE username = '{username}';").fetchall()
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

            # TODO: check to see if id already exists!!
            # print("user_info", user_info)
            # print(user_info["username"])
            # print(self.exists(username=user_info["username"])["data"])

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

                email_list = cursor.execute(f"SELECT email FROM {self.table_name};").fetchall()
                if user_data[1] in email_list:
                    email_check = False

                if ((username_check == True) and (password_check == True) and (email_check == True)):
                    cursor.execute(f"INSERT INTO {self.table_name} VALUES (?, ?, ?, ?);", user_data)
                    db_connection.commit()
                    
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
                print('username', username)
                if (self.exists(username=username) == True):
                    results = cursor.execute(f"SELECT * FROM {self.table_name} WHERE username = '{username}';").fetchall()
                    print("usernamE:", results, type(results))
                    print(self.to_dict(results[0]))
                    return {"status":"success",
                    "data":self.to_dict(results[0])}
                else:
                    print("userexists failing")
            elif (id):
                if (self.exists(id=id) == True):
                    results = cursor.execute(f"SELECT * FROM {self.table_name} WHERE id = '{id}';").fetchall()
                    #print(results[0])
                    return {"status":"success",
                    "data":self.to_dict(results[0])}
            else:
                return {"status":"success",
                    "data":"user doesnt exist"}
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

            results = cursor.execute(f"SELECT * FROM {self.table_name};").fetchall()
            print(results)
            return {"status":"success",
                    "data":results}
        
        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        finally:
            db_connection.close()

    def update(self, user_info): 
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()
            '''
                Insert your code here
            '''
            for element in user_info:
                if (element != "id"):
                    cursor.execute(f"UPDATE {self.table_name} SET {element}='{user_info[element]}' WHERE id = '{user_info['id']}'")
                    db_connection.commit()
            
            return {"status":"success",
                    "data":self.to_dict(self.get(id=user_info['id'])['data'])}

        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        finally:
            db_connection.close()

    def remove(self, username): 
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()
            '''
                Insert your code here
            '''
            cursor.execute(f"DELETE FROM {self.table_name} WHERE username = '{username}';")
            db_connection.commit()

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

    # user_details={
    #     "email":"justin.gohde@trinityschoolnyc.org",
    #     "username":"justingohde",
    #     "password":"123TriniT"
    # }
    # results = Users.create(user_details)

    user_details={"email": "hey_hey@haveaniceday.com", 
                    "username":"something_different",  # bad username
                    "password":"123456789"}
    results = Users.create(user_details)

    print(results, type(results))

    user_details2 = {"email": "hey_hey@haveaniceday.com", 
                    "username":"sasdfasdfnt",  # bad username
                    "password":"1alsdkfjlaskdjf9"}
    results = Users.create(user_details2)

    print(results, type(results))

    # print(Users.exists(username='justingohde'))
    # print(Users.exists(id=8237105982883065))
    # print(Users.get('justingohde'))
    
