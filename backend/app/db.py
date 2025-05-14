import gridfs
from pymongo import MongoClient

# Hardcoded MongoDB Credentials
MONGO_USER = "mongoapp"
MONGO_PASS = "huMONGOu5"
MONGO_DB = "MongoProject"
MONGO_HOST = "localhost"
MONGO_PORT = "27017"
MONGO_AUTH = True

# MongoDB Connection URI with Authentication
MONGO_URI = f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}?authSource={MONGO_DB}"


if MONGO_AUTH:
    # Initialize MongoDB connection
    client = MongoClient(MONGO_URI)
else:
    # For local debugging not bothering with authentication
    client = MongoClient("mongodb://localhost:27017/")

db = client[MONGO_DB]

# Initialize GridFS
fs = gridfs.GridFS(db)

# Define the GeoUFOSightings collection
ufoSightings = db.GeoUFOSightings  # Collection for UFO reports
