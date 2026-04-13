import os

# Telegram API Credentials
# Get these from https://my.telegram.org
API_ID = 36530300
API_HASH = '4515566e294d0313e501cf5a08dd1a79'
PHONE_NUMBER = '+251980027967'

# MongoDB Configuration
# Default to localhost if MONGO_URI is not set in environment
# MONGO_URI = os.getenv('MONGO_URI', 'mongodb+srv://eliassisaynega_db_user:x9aUrWYrO6ehIBDQ@pharma.xbx5axb.mongodb.net/?appName=pharma')
DB_NAME = 'telegram_multi_sender'
MONGO_URI = os.getenv('MONGO_URI', 'mongodb+srv://eliassisaydev_db_user:MZYldEzKCWGutjZq@pharma.ofeigvv.mongodb.net/?appName=pharma')
