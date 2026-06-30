from pymongo import MongoClient
from app.config import get_settings

# Load settings from .env
settings = get_settings()

# Create MongoDB client
client = MongoClient(settings.mongo_uri)

# Select database
db = client[settings.mongo_db_name]


def test_connection():
    try:
        client.admin.command("ping")
        print("✅ MongoDB Atlas Connected Successfully!")
    except Exception as e:
        print("❌ MongoDB Connection Failed:", e)


# Optional: expose collections (you can use later)
clients_collection = db["clients"]
documents_collection = db["documents"]
traces_collection = db["traces"]


if __name__ == "__main__":
    test_connection()