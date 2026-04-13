import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession
import os
from dotenv import load_dotenv

load_dotenv()

async def generate_string_session():
    print("--- Telegram String Session Generator ---")
    
    api_id = input("Enter API_ID (or press Enter to use .env value): ") or os.getenv('API_ID')
    api_hash = input("Enter API_HASH (or press Enter to use .env value): ") or os.getenv('API_HASH')
    
    if not api_id or not api_hash:
        print("Error: API_ID and API_HASH are required.")
        return

    async with TelegramClient(StringSession(), int(api_id), api_hash) as client:
        session_str = client.session.save()
        print("\n" + "="*50)
        print("YOUR STRING SESSION (Keep this secret!):")
        print("="*50)
        print(f"\n{session_str}\n")
        print("="*50)
        print("Copy the string above and add it as 'STRING_SESSION' in your Render Environment Variables.")

if __name__ == "__main__":
    asyncio.run(generate_string_session())
