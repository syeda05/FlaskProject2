import firebase_admin
from firebase_admin import credentials, firestore

def db_connection():
    cred = credentials.Certificate("key.json")
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    collection = db.collection("recipes").get()
    recipes_list=[]
    for r in collection:
        recipes_list.append(r.to_dict())
    return recipes_list