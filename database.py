import datetime
import logging
import certifi
import motor.motor_asyncio
from config import MONGO_URI, DB_NAME

logger = logging.getLogger(__name__)

# DIAGNOSTIC MODE: Testing if SSL error is CA-related or Protocol-related
client = motor.motor_asyncio.AsyncIOMotorClient(
    MONGO_URI, 
    tlsCAFile=certifi.where(),
    tlsAllowInvalidCertificates=True 
)
db = client[DB_NAME]
users_collection = db['selected_users']
logs_collection = db['broadcast_logs']

async def check_connection():
    try:
        # The ping command is cheap and does not require auth.
        await client.admin.command('ping')
        logger.info("Successfully connected to MongoDB!")
        return True
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        return False

async def add_user(user_id: int, username: str = None, name: str = None):
    await users_collection.update_one(
        {'_id': user_id},
        {'$set': {'username': username, 'name': name}},
        upsert=True
    )

async def remove_user(user_id: int):
    result = await users_collection.delete_one({'_id': user_id})
    return result.deleted_count > 0

async def remove_user_by_username(username: str):
    # strip @ if present
    username = username.lstrip('@')
    result = await users_collection.delete_one({'username': username})
    return result.deleted_count > 0

async def get_all_users():
    cursor = users_collection.find({})
    return await cursor.to_list(length=None)

async def clear_users():
    await users_collection.delete_many({})

async def log_broadcast(message: str, success_count: int, failed_count: int, errors: list):
    await logs_collection.insert_one({
        'message_preview': str(message)[:200] if message else "[Media/Non-text]",
        'success': success_count,
        'failed': failed_count,
        'errors': errors,
        'timestamp': datetime.datetime.utcnow()
    })

