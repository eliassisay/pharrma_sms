import datetime
import logging
import certifi
import motor.motor_asyncio
from config import MONGO_URI, DB_NAME

logger = logging.getLogger(__name__)

# Initialize variables
client = None
db = None
users_collection = None
logs_collection = None

def get_db():
    global client, db, users_collection, logs_collection
    if client is None:
        try:
            client = motor.motor_asyncio.AsyncIOMotorClient(
                MONGO_URI, 
                tlsCAFile=certifi.where(),
                tlsAllowInvalidCertificates=True,
                serverSelectionTimeoutMS=5000 # Fail faster
            )
            db = client[DB_NAME]
            users_collection = db['selected_users']
            logs_collection = db['broadcast_logs']
        except Exception as e:
            logger.error(f"Error initializing MongoDB client: {e}")
            raise
    return db

async def check_connection():
    try:
        get_db()
        # The ping command is cheap and does not require auth.
        await client.admin.command('ping')
        logger.info("Successfully connected to MongoDB!")
        return True
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        return False

async def add_user(user_id: int, username: str = None, name: str = None):
    get_db()
    # Check if user already exists to preserve their group
    existing_user = await users_collection.find_one({'_id': user_id})
    if existing_user:
        await users_collection.update_one(
            {'_id': user_id},
            {'$set': {'username': username, 'name': name}}
        )
    else:
        # Assign new group
        user_count = await users_collection.count_documents({})
        group_id = (user_count // 50) + 1
        await users_collection.insert_one({
            '_id': user_id,
            'username': username,
            'name': name,
            'group_id': group_id,
            'added_at': datetime.datetime.utcnow()
        })

async def remove_user(user_id: int):
    get_db()
    result = await users_collection.delete_one({'_id': user_id})
    return result.deleted_count > 0

async def remove_user_by_username(username: str):
    get_db()
    # strip @ if present
    username = username.lstrip('@')
    result = await users_collection.delete_one({'username': username})
    return result.deleted_count > 0

async def get_all_users():
    get_db()
    cursor = users_collection.find({})
    return await cursor.to_list(length=None)

async def get_users_by_group(group_id: int):
    get_db()
    cursor = users_collection.find({'group_id': group_id})
    return await cursor.to_list(length=None)

async def get_group_ids():
    get_db()
    return await users_collection.distinct('group_id')

async def get_group_stats():
    get_db()
    pipeline = [
        {'$group': {'_id': '$group_id', 'count': {'$sum': 1}}},
        {'$sort': {'_id': 1}}
    ]
    cursor = users_collection.aggregate(pipeline)
    return await cursor.to_list(length=None)

async def clear_users():
    get_db()
    await users_collection.delete_many({})

async def clear_all_data():
    get_db()
    await users_collection.delete_many({})
    await logs_collection.delete_many({})

async def log_broadcast(message: str, success_count: int, failed_count: int, errors: list):
    get_db()
    await logs_collection.insert_one({
        'message_preview': str(message)[:200] if message else "[Media/Non-text]",
        'success': success_count,
        'failed': failed_count,
        'errors': errors,
        'timestamp': datetime.datetime.utcnow()
    })
