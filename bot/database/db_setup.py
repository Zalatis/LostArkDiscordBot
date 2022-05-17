from datetime import datetime
from pymongo import MongoClient

from .characters import Characters

class Database:
    def __init__(self, uri):
        self.cluster = MongoClient(uri)
        self.db = self.cluster["lost_ark_bot"]

        self.characters = Characters(self.db)

        