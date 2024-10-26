from pymongo import MongoClient

db_name = "Triage-o-matic"
collection_name = "users"

def get_db_client(uri="mongodb+srv://vermatanmay661:5j3NcFusxyDfHYYU@cluster0.3ny45.mongodb.net/Triage-o-matic?retryWrites=true&w=majority&ssl=true"):
    return MongoClient(uri)

def find_user(username):
    client = get_db_client()
    try:
        database = client.get_database(db_name)
        collection = database.get_collection(collection_name)
        query = {"username": username}
        user = collection.find_one(query)
        return user
    except Exception as e:
        raise Exception("Unable to connect to the database or find the document due to the following error:", e)
    finally:
        client.close()

def insert_user(user_data):
    client = get_db_client()
    try:
        database = client.get_database(db_name)
        collection = database.get_collection(collection_name)
        result = collection.insert_one(user_data)
        return result.inserted_id
    except Exception as e:
        raise Exception("Unable to insert the document due to the following error:", e)
    finally:
        client.close()
