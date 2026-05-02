import asyncio
import motor.motor_asyncio
import certifi
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = "mongodb+srv://haymanotgula24_db_user:zMgbNMibquwrgCNB@cluster0.ohqivqp.mongodb.net/?appName=Cluster0"

async def test_mongo():
    print(f"Testing MongoDB connection to: {MONGO_URI}")
    try:
        client = motor.motor_asyncio.AsyncIOMotorClient(
            MONGO_URI,
            tlsCAFile=certifi.where(),
            tlsAllowInvalidCertificates=True,
            serverSelectionTimeoutMS=10000
        )
        # Ping
        await client.admin.command('ping')
        print("DONE: MongoDB Connection Successful!")
    except Exception as e:
        print(f"ERROR: MongoDB Connection Failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_mongo())
