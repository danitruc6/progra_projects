from pymongo import MongoClient

# This is a MongoDB client for the local database.
# It connects to the local MongoDB instance and accesses the 'local' database.
# db_client = MongoClient().local

# This is a MongoDB client for the remote database.
db_client = MongoClient("mongodb+srv://test:test@cluster0.obskpq8.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0").test