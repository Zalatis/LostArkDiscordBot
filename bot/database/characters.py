from datetime import datetime, timedelta
from pymongo import MongoClient
from pytz import timezone

class Characters:
    def __init__(self, db):
        self.db = db
        self.collection = self.db["characters"]

    def get_from_id(self, id):
        return self.collection.find_one( {"_id": id} )

    def get(self, user_id, char_name, char_level, char_class):
        
        item = self.collection.find_one(
            {
                "user_id": user_id,
                "char_name": char_name,
                "char_level": char_level,
                "char_class": char_class
            }
        )
        return item
    
    def register(self, user_id, char_name, char_level, char_class):
        
        result = self.collection.insert_one(
            {
                "user_id": user_id,
                "char_name": char_name,
                "char_level": char_level,
                "char_class": char_class,
            }
        )

        return self.get_from_id( result.inserted_id )

    def find(self, user_id, char_name):
        return self.collection.find( { "user_id": user_id, "char_name": char_name } )

    def find_all(self, user_id):
        return self.collection.find( { "user_id": user_id } )

    def edit(self, id, char_level):

        self.collection.update_one(
            {
                "_id": id,
            },
            {
                "$set": {
                    "char_level": char_level
                }
            }
        )
        

    def delete(self, id):
        self.collection.delete_one(
            {
                "_id": id,
            }
        )