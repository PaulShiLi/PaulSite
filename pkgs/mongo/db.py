from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from pkgs import ENV
import pymongo
import os


if os.environ.get("DOCKER") == "1":
    CONTAINER_NAME = ENV.content["docker"]["mongo"]
else:
    CONTAINER_NAME = "localhost"

CONNECTION_URL = f"mongodb://{ENV.content['db']['mongo']['username']}:{ENV.content['db']['mongo']['password']}@{CONTAINER_NAME}:{ENV.content['db']['mongo']['port']}/"
mongoClient = pymongo.MongoClient(CONNECTION_URL)

class Mongo:
    def insert(db: str, collection: str, data: dict | list[dict]):
        dbObj = mongoClient[db]
        col = dbObj[collection]
        
        if isinstance(data, dict):
            col.insert_one(data)
        else:
            col.insert_many(data)
    
    def find(db: str, collection: str, query: dict = {}):
        dbObj = mongoClient[db]
        col = dbObj[collection]
        
        return list(col.find(query))
    
    def delete(db: str, collection: str, query: dict = {}):
        dbObj = mongoClient[db]
        col = dbObj[collection]
        
        col.delete_many(query)
    
    def replace(db: str, collection: str, query: dict, data: dict):
        dbObj = mongoClient[db]
        col = dbObj[collection]
        
        col.replace_one(query, data)