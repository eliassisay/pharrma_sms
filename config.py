import os
from dotenv import load_dotenv

# Load .env file for local development
load_dotenv()

# Telegram API Credentials
# Get these from https://my.telegram.org
API_ID = int(os.getenv('API_ID', '30227459'))
API_HASH = os.getenv('API_HASH', '1aba59c22dc72c7f9a671e13d6981b05')
PHONE_NUMBER = os.getenv('PHONE_NUMBER', '+251980027967')

# MongoDB Configuration
MONGO_URI = os.getenv('MONGO_URI', 'mongodb+srv://haymanotgula24_db_user:zMgbNMibquwrgCNB@cluster0.ohqivqp.mongodb.net/?appName=Cluster0')
DB_NAME = os.getenv('DB_NAME', 'all_in_one')

# Telegram Session Management (Used for cloud deployment)
STRING_SESSION = os.getenv('STRING_SESSION', '1BJWap1wBu1h4l-4_PmW1gXzE6749bSQ_xgtLm6mEeD8awQUcYWu7F_O7oNHX7VmdTkTOG23f7r2cyISUw8H-XD8StuDQEDe42P2IlIBMyH5VX_wbBDHcUuNctHvIKFdGOP48lQ-gXDb8nI_iMAoEJRm9qf_TK1BlHrkY0MqlJfSrrOMc54EHs_TIqm_2-_KC2BAR2c2pFQMnrp5-es5qvhAd6Cxy2KCe9H0LTOFTrgSgJbCuXc_g_-wdmUUeT19jnpBSW8X9lGEtywCl6RGouls8IrSSJeC5gtKEvdVwG85xrLc-VhC3WF9q6KaDllte-Qn0SNILLBZ0sJyIQeX7rzOht7-hkqo=')
BOT_TOKEN = os.getenv('BOT_TOKEN', '8724770472:AAEzwjh5s5tbhP9ptZykmxk4NHnpkfdTXds')
OWNER_ID = int(os.getenv('OWNER_ID', '0')) # Set this to your Telegram ID to use the bot mode

