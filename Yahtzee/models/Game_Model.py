# Arlo Virtucio #

import sqlite3
import random

class Game:
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
                    name TEXT UNIQUE,
                    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    finished TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                """
        cursor.execute(f"DROP TABLE IF EXISTS {self.table_name};")
        results=cursor.execute(schema)
        db_connection.close()
    
    def exists(self, game_name=None, id=None):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()
        #######
            if (game_name):
                results = cursor.execute(f"SELECT * FROM {self.table_name} WHERE name = '{game_name}';").fetchall()
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

    def create(self, game_info):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()
            game_id = random.randint(0, self.max_safe_id)

            # TODO: check to see if id already exists!!
            
            if ((self.exists(id=game_id)["data"] == False) and (self.exists(game_info["name"])["data"] == False)):
                game_data = (game_id, game_info["name"])
                #are you sure you have all data in the correct format?
                gamename_check = True
                for character in game_data[1]:
                    if ((character.isalnum() == False) and (character != "_") and (character != "-")):
                        gamename_check = False
                        break

                if (gamename_check == True):
                    cursor.execute(f"INSERT INTO {self.table_name} (id, name) VALUES (?, ?);", game_data)
                    db_connection.commit()

                    print("aboutta check results")
                    results = cursor.execute(f"SELECT name FROM {self.table_name} WHERE name = {game_info["name"]};", game_data).fetchall()
                    print(results)


                    return {"status": "success",
                        "data": self.to_dict(results)
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
    
    def get(self, game_name=None, id=None):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()
        ####### check if exists first
            if (id):
                if (self.exists(id=id)["data"] == True):
                    results = cursor.execute(f"SELECT * FROM {self.table_name} WHERE id = '{id}';").fetchall()
                    return {"status":"success",
                    "data":self.to_dict(results[0])}
                else:
                    return {"status":"error",
                    "data":"game id doesnt exist"}
            elif (game_name):
                if (self.exists(game_name=game_name)["data"] == True):
                    results = cursor.execute(f"SELECT * FROM {self.table_name} WHERE name = '{game_name}';").fetchall()
                    return {"status":"success",
                    "data":self.to_dict(results[0])}
            else:
                return {"status":"error",
                    "data":"game name doesnt exist"}
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

            game_info_list = []
            results = cursor.execute(f"SELECT * FROM {self.table_name};").fetchall()
            for game_tuple in results:
                game_info_list.append(self.to_dict(game_tuple))
            
            return {"status":"success",
                    "data":game_info_list}
        
        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        finally:
            db_connection.close()

    def update(self, game_info): 
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

            if (self.exists(id=game_info["id"])["data"] == True):
                for element in game_info:
                    if (element != "id"):
                        cursor.execute(f"UPDATE {self.table_name} SET {element}='{game_info[element]}' WHERE id = '{game_info['id']}'")
                        db_connection.commit()

                return {"status":"success",
                        "data":self.get(id=game_info['id'])["data"]}
            else:
                return {"status":"error",
                        "data":"user doesnt exist"}

        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        finally:
            db_connection.close()

    def is_finished(self, game_name):
        try:
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

            if (self.exists(game_name=game_name)["data"] == True):
                if (self.get(game_name=game_name)["data"]["created"] == self.get(game_name=game_name)["data"]["finished"]):
                    return {"status":"success",
                    "data":True}
            else:
                return {"status":"success",
                    "data":False}
        
        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        finally:
            db_connection.close()

    def remove(self, game_name): 
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()
            
            if (self.exists(game_name=game_name)["data"] == True):
                deleted_game = self.get(game_name=game_name)["data"]
                cursor.execute(f"DELETE FROM {self.table_name} WHERE name = '{game_name}';")
                db_connection.commit()

                return {"status":"success",
                        "data":deleted_game}
            else:
                return {"status":"error",
                    "data":"user name doesnt exist"}

        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        finally:
            db_connection.close()
    
    def to_dict(self, game_tuple):
        '''Utility function which converts the tuple returned from a SQLlite3 database
           into a Python dictionary
        '''
        game_dict={}
        print("to_dict:", game_tuple)
        #print("usertuple",user_tuple, user_tuple[0], type(user_tuple[1]))
        if game_tuple:
            game_dict["id"]=game_tuple[0]
            game_dict["name"]=game_tuple[1]
            game_dict["created"]=game_tuple[2]
            game_dict["finished"]=game_tuple[3]
        return game_dict

if __name__ == '__main__':
    import os
    print("Current working directory:", os.getcwd())
    DB_location=f"{os.getcwd()}yahtzeeDB.db"
    table_name = "games"
    
    Game = Game(DB_location, table_name) 
    Game.initialize_table()

    game_details={
        "name": "aosdjkgaskdldsakjg"
    }
    results = Game.create(game_details)
    # id = results["data"]["id"]
    print(results)

    # new_user_details={
    #     "id": id,
    #     "email":"justin.gohde@trinityschoolnyc.org",
    #     "username":"justingohdeeeeeee",
    #     "password":"123TriniT"
    # }
    
    