import os
from dotenv import load_dotenv

# Load .env file for local development
load_dotenv()

# Telegram API Credentials
# Get these from https://my.telegram.org
API_ID = int(os.getenv('API_ID', '36530300'))
API_HASH = os.getenv('API_HASH', '4515566e294d0313e501cf5a08dd1a79')
PHONE_NUMBER = os.getenv('PHONE_NUMBER', '+251980027967')

# MongoDB Configuration
MONGO_URI = os.getenv('MONGO_URI', 'mongodb+srv://haymanotgula24_db_user:B4qP0H6VOU4AAnRB@smspharma.wnhrqeh.mongodb.net/?appName=smspharma')
DB_NAME = os.getenv('DB_NAME', 'telegram_multi_sender')

# Telegram Session Management (Used for cloud deployment)
STRING_SESSION = os.getenv('STRING_SESSION')
