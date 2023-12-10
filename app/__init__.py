import os

from pymongo.mongo_client import MongoClient
from pymongo.collection import Collection
from dotenv import load_dotenv

def create_mongo_client(uri):
    client = MongoClient(uri)
    try:
        client.admin.command("ping")
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)
    return client

load_dotenv()
_uri = os.getenv("mongo_uri")
_admin_id = os.getenv("admin_id")
CLIENT = create_mongo_client(_uri)
DB = CLIENT.data
DB_GROUPS_QUEUES: Collection = DB.groups_queues
DB_GROUPS_ADMINS: Collection = DB.groups_admins
DB_GROUPS_SKIPS: Collection = DB.groups_skips
PEER_ID_OFFSET = 2000000000

#TODO: FIX IT
def add_default_admin(group_id, admin_id=_admin_id):
    try:
        DB_GROUPS_ADMINS.insert_one({"_id": group_id, "admins": [admin_id]})
    except:
        pass

for i in range(1, 10):
    #Добавление в первые 10 бесед админа по умолчанию
    add_default_admin(i)