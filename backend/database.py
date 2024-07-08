import firebase_admin
from firebase_admin import credentials, storage
from firebase_admin import firestore

cred = credentials.Certificate("credentials.json")
fire_app = firebase_admin.initialize_app(cred)