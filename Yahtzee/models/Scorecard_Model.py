# Arlo Virtucio #

import sqlite3
import random
import json
from User_Model import User
from Game_Model import Game

class Scorecard:
    def __init__(self, db_name, scorecard_table_name, user_table_name, game_table_name):
        self.db_name =  db_name
        self.max_safe_id = 9007199254740991 #maximun safe Javascript integer
        self.table_name = scorecard_table_name 
        self.user_table_name = user_table_name
        self.game_table_name = game_table_name
    
    def initialize_table(self):
        db_connection = sqlite3.connect(self.db_name, )
        cursor = db_connection.cursor()
        schema=f"""
                CREATE TABLE {self.table_name} (
                    id INTEGER PRIMARY KEY UNIQUE,
                    game_id INTEGER,
                    user_id INTEGER,
                    categories TEXT,
                    turn_order INTEGER,
                    name TEXT,
                    FOREIGN KEY(game_id) REFERENCES {self.game_table_name}(id) ON DELETE CASCADE,
                    FOREIGN KEY(user_id) REFERENCES {self.user_table_name}(id) ON DELETE CASCADE
                )
                """
        cursor.execute(f"DROP TABLE IF EXISTS {self.table_name};")
        results=cursor.execute(schema)
        db_connection.close()
    
    def create(self, game_id, user_id, name):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()
            card_id = random.randint(0, self.max_safe_id)
            categories_dict = {
                "dice_rolls":0,
                "upper":{
                    "ones":-1,
                    "twos":-1,
                    "threes":-1,
                    "fours":-1,
                    "fives":-1,
                    "sixes":-1
                },
                "lower":{
                "three_of_a_kind":-1,
                    "four_of_a_kind":-1,
                    "full_house":-1,
                    "small_straight":-1,
                    "large_straight":-1,
                    "yahtzee":-1,
                    "chance":-1
                }
            }
            categories_string = json.dumps(categories_dict)

            results = cursor.execute(f"SELECT * FROM {self.table_name} WHERE game_id = {game_id};").fetchall()
            current_players_count = len(results)
            turn_order = current_players_count + 1

            if (turn_order > 4):
                return {"status":"error",
                    "data":"maximum players in game"}
            
            player_exist_test = cursor.execute(f"SELECT * FROM {self.table_name} WHERE user_id = {user_id};").fetchall()
            if (player_exist_test):
                return {"status":"error",
                    "data":"player already in game"}

            scorecard_data = [card_id, game_id, user_id, categories_string, turn_order, name]
            cursor.execute(f"INSERT INTO {self.table_name} VALUES (?, ?, ?, ?, ?, ?);", scorecard_data)
            db_connection.commit()

            return {"status":"success",
                    "data":self.get(id=card_id)["data"]}

        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        finally:
            db_connection.close()

    def get(self, name = None, id=None):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

            if (name):
                results = cursor.execute(f"SELECT * FROM {self.table_name} WHERE name = '{name}';").fetchall()
                if (results):
                    return {"status":"success",
                        "data":self.to_dict(results[0])}
                else:
                    return {"status":"error",
                        "data":"scorecard does not exist"}
            elif (id):
                results = cursor.execute(f"SELECT * FROM {self.table_name} WHERE id = {id};").fetchall()
                if (results):
                    return {"status":"success",
                        "data":self.to_dict(results[0])}
                else:
                    return {"status":"error",
                        "data":"scorecard does not exist"}

        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        finally:
            db_connection.close()
    
    def get_all(self): 
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

            card_array = []
            results = cursor.execute(f"SELECT * FROM {self.table_name};").fetchall()
            for card_tuple in results:
                card_array.append(self.to_dict(card_tuple))
            return {"status":"success",
                    "data":card_array}

        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        finally:
            db_connection.close()
    
    def get_all_game_scorecards(self, game_name:str): 
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

            scorecard_list = []
            all_cards = self.get_all()["data"]
            for card in all_cards:
                card_game_name = card["name"].split("|")[0]
                if (card_game_name == game_name):
                    scorecard_list.append(card)
            
            return {"status":"success", "data":scorecard_list}
                
        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        finally:
            db_connection.close()

    def get_all_game_usernames(self, game_name:str): 
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

            username_list = []
            all_cards = self.get_all()["data"]
            for card in all_cards:
                card_game_name = card["name"].split("|")[0]
                card_user_name = card["name"].split("|")[1]
                if (card_game_name == game_name):
                    username_list.append(card_user_name)
            
            return {"status":"success", "data":username_list}

        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        finally:
            db_connection.close()

    def get_all_user_game_names(self, username:str): 
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()
            
            print("looking for", username, "games")
            game_list = []
            all_cards = self.get_all()["data"]
            for card in all_cards:
                print(card["name"])
                card_user_name = card["name"].split("|")[1]
                print(card_user_name)
                if (card_user_name == username):
                    print("user has this game", card["name"].split("|")[0])
                    game_list.append(card["name"].split("|")[0])
            
            print(username, "games:", game_list)
            
            return {"status":"success", "data":game_list}

        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        finally:
            db_connection.close()

    def update(self, id, name=None, categories=None): 
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

            results = cursor.execute(f"SELECT * FROM {self.table_name} WHERE id = {id};").fetchall()
            if (results):
                if (name):
                    cursor.execute(f"UPDATE {self.table_name} SET name ='{name}' WHERE id = {id};")
                    db_connection.commit()
                if (categories):
                    cursor.execute(f"UPDATE {self.table_name} SET categories ='{json.dumps(categories)}' WHERE id = {id};")
                    db_connection.commit()

                return {"status":"success",
                        "data":self.get(id=id)["data"]}
            else:
                return {"status":"error", 
                 "data":"score card doesnt exist"}

        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        finally:
            db_connection.close()

    def remove(self, id): 
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

            print("all scorecards", len(self.get_all()["data"]))

            results = cursor.execute(f"SELECT * FROM {self.table_name} WHERE id = {id};").fetchall()
            print("game exists", results)

            if (results):
                deleted_game = self.get(id=id)["data"]
                cursor.execute(f"DELETE FROM {self.table_name} WHERE id = {id};")
                db_connection.commit()

                print("after game deletion", cursor.execute(f"SELECT * FROM {self.table_name} WHERE id = {id};").fetchall())

                print("all scorecards after deletion", len(self.get_all()["data"]))
                

                return {"status":"success", 
                        "data":deleted_game}
            else:
                return {"status":"error", 
                        "data":"score card doesnt exist"}

        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        finally:
            db_connection.close()
    
    def to_dict(self, card_tuple):
        game_dict={}
        if card_tuple:
            game_dict["id"]=card_tuple[0]
            game_dict["game_id"]=card_tuple[1]
            game_dict["user_id"]=card_tuple[2]
            game_dict["categories"]=json.loads(card_tuple[3])
            game_dict["turn_order"]=card_tuple[4]
            game_dict["name"]=card_tuple[5]
        return game_dict
    
    def create_blank_score_info(self):
        return {
            "dice_rolls":0,
            "upper":{
                "ones":-1,
                "twos":-1,
                "threes":-1,
                "fours":-1,
                "fives":-1,
                "sixes":-1
            },
            "lower":{
                "three_of_a_kind":-1,
                "four_of_a_kind":-1,
                "full_house":-1,
                "small_straight":-1,
                "large_straight":-1,
                "yahtzee":-1,
                "chance":-1
            }
        }

    def tally_score(self, score_info):
        total_score = 0
        scores_dict = score_info  
        upper_sum = 0
        lower_sum = 0

        for category in scores_dict["upper"]:
            if (scores_dict["upper"][category] > -1):
                upper_sum += scores_dict["upper"][category]
        if (upper_sum >= 63):
            upper_sum += 35

        for category in scores_dict["lower"]:
            if (scores_dict["lower"][category] > -1):
                upper_sum += scores_dict["lower"][category]
        if (lower_sum >= 63):
            lower_sum += 35

        total_score = upper_sum + lower_sum
        return total_score

if __name__ == '__main__':
    import os
    #print("Current working directory:", os.getcwd())
    DB_location=f"{os.getcwd()}/yahtzeeDB.db"
    #print("location", DB_location)
    Users = User(DB_location, "users")
    Users.initialize_table()
    Games = Game(DB_location, "games")
    Games.initialize_table()
    Scorecards = Scorecard(DB_location, "scorecards", "users", "games")
    Scorecards.initialize_table()

    Scorecards.update()