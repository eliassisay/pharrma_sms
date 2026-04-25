import asyncio
import logging
import threading
import os
import sys
from flask import Flask
from telethon import TelegramClient, events, errors, types, functions
from telethon.sessions import StringSession
from config import API_ID, API_HASH, PHONE_NUMBER, STRING_SESSION
import database

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Globals
client = None
session = StringSession(STRING_SESSION) if STRING_SESSION else 'multi_sender_session'

HELP_TEXT = """
**Multi-Sender Userbot Commands:**
/add @user1 @user2 12345 - Add users by username or ID
/remove @user1 12345 - Remove users
/list - List selected users
/clear - Clear the selection list
/load_contacts - Add all your personal contacts to the list
/load_group @group_username - Add members from a group
/broadcast message - Send message to all. (TIP: Reply to any message with /broadcast to send that specific message/media)
/help - Show this help
"""

async def get_user_details(client, entity):
    try:
        user = await client.get_entity(entity)
        if isinstance(user, types.User):
            first_name = user.first_name or ""
            last_name = user.last_name or ""
            return user.id, user.username, f"{first_name} {last_name}".strip()
    except Exception as e:
        logger.error(f"Error getting entity {entity}: {e}")
    return None, None, None

def is_allowed_chat(event):
    return event.is_private

async def start_handler(event):
    if not is_allowed_chat(event): return
    await event.respond("✅ Multi-Sender Userbot is active. Type /help to see commands.")

async def help_handler(event):
    if not is_allowed_chat(event): return
    await event.respond(HELP_TEXT)

async def add_handler(event):
    if not is_allowed_chat(event): return
    args = event.message.text.split()[1:]
    if not args:
        return await event.respond("Usage: /add @user1 @user2 12345")
    
    added = []
    failed = []
    for arg in args:
        uid, username, name = await get_user_details(event.client, arg)
        if uid:
            await database.add_user(uid, username, name)
            added.append(f"{name or username or uid}")
        else:
            failed.append(arg)
    
    response = ""
    if added:
        response += f"✅ Added: {', '.join(added)}\n"
    if failed:
        response += f"❌ Failed to find: {', '.join(failed)}"
    await event.respond(response or "No users found.")

async def remove_handler(event):
    if not is_allowed_chat(event): return
    args = event.message.text.split()[1:]
    if not args:
        return await event.respond("Usage: /remove @user1 12345")
    
    removed = []
    for arg in args:
        try:
            if arg.startswith('@'):
                if await database.remove_user_by_username(arg):
                    removed.append(arg)
            else:
                if await database.remove_user(int(arg)):
                    removed.append(arg)
        except ValueError:
             if await database.remove_user_by_username(arg):
                    removed.append(arg)
    
    await event.respond(f"✅ Removed: {', '.join(removed)}" if removed else "None removed.")

async def list_handler(event):
    if not is_allowed_chat(event): return
    users = await database.get_all_users()
    if not users:
        return await event.respond("The selection list is empty.")
    
    msg = "**Selected Users:**\n"
    for u in users:
        username = f"(@{u['username']})" if u.get('username') else ""
        msg += f"- {u.get('name', 'Unknown')} {username} [ID: {u['_id']}]\n"
    
    if len(msg) > 4000:
        for i in range(0, len(msg), 4000):
            await event.respond(msg[i:i+4000])
    else:
        await event.respond(msg)

async def clear_handler(event):
    if not is_allowed_chat(event): return
    await database.clear_users()
    await event.respond("✅ Selection list cleared.")

async def contacts_handler(event):
    if not is_allowed_chat(event): return
    status = await event.respond("Loading contacts...")
    try:
        contacts = await event.client.get_contacts()
        count = 0
        for c in contacts:
            if not c.bot:
                await database.add_user(c.id, c.username, f"{c.first_name or ''} {c.last_name or ''}".strip())
                count += 1
        await status.edit(f"✅ Loaded {count} contacts into the list.")
    except Exception as e:
        await status.edit(f"❌ Error: {str(e)}")

async def group_handler(event):
    if not is_allowed_chat(event): return
    args = event.message.text.split()
    if len(args) < 2:
        return await event.respond("Usage: /load_group @group_username OR https://t.me/link")
    
    group_input = args[1]
    status = await event.respond(f"🔍 Accessing group: {group_input}...")
    try:
        if 't.me/+' in group_input or 't.me/joinchat/' in group_input:
            hash = group_input.split('/')[-1].replace('+', '')
            try:
                await event.client(functions.messages.ImportChatInviteRequest(hash))
                group_entity = await event.client.get_entity(group_input)
            except errors.UserAlreadyParticipantError:
                group_entity = await event.client.get_entity(group_input)
        else:
            group_entity = await event.client.get_entity(group_input)

        count = 0
        async for user in event.client.iter_participants(group_entity):
            if not user.bot:
                await database.add_user(user.id, user.username, f"{user.first_name or ''} {user.last_name or ''}".strip())
                count += 1
        await status.edit(f"✅ Loaded {count} members from {group_entity.title if hasattr(group_entity, 'title') else group_input}.")
    except Exception as e:
        logger.error(f"Error loading group: {e}")
        await status.edit(f"❌ Error: {str(e)}")

async def broadcast_handler(event):
    if not is_allowed_chat(event): return
    
    selected_users = await database.get_all_users()
    if not selected_users:
        return await event.respond("Selection list is empty. Add users first!")
    
    reply = await event.get_reply_message()
    broadcast_msg = reply if reply else event.message
    
    if not reply and event.message.text.startswith('/broadcast'):
        text = event.message.text[len('/broadcast'):].strip()
        if not text:
            return await event.respond("Usage: /broadcast <message> OR reply to a message with /broadcast")
        broadcast_msg = text

    confirm = await event.respond(f"🚀 Starting broadcast to {len(selected_users)} users...")
    
    success = 0
    failed = 0
    err_logs = []
    
    for u in selected_users:
        try:
            await event.client.send_message(u['_id'], broadcast_msg)
            success += 1
            await asyncio.sleep(1.5) 
        except errors.FloodWaitError as e:
            logger.warning(f"FloodWait: sleeping for {e.seconds} seconds")
            await asyncio.sleep(e.seconds)
            try:
                await event.client.send_message(u['_id'], broadcast_msg)
                success += 1
            except Exception as e2:
                failed += 1
                err_logs.append(f"User {u['_id']}: {str(e2)}")
        except Exception as e:
            failed += 1
            err_logs.append(f"User {u['_id']}: {str(e)}")
            logger.error(f"Failed to send to {u['_id']}: {e}")
            
    preview = "Media/Reply"
    if isinstance(broadcast_msg, str): preview = broadcast_msg
    elif hasattr(broadcast_msg, 'text') and broadcast_msg.text: preview = broadcast_msg.text

    await database.log_broadcast(preview, success, failed, err_logs[:10])
    
    final_report = f"✨ Broadcast Finished!\n✅ Success: {success}\n❌ Failed: {failed}"
    if failed > 0:
        final_report += "\nCheck MongoDB logs for details."
    await confirm.edit(final_report)

# --- Minimal Web Server for Health Checks ---
app = Flask(__name__)

@app.route('/')
def health_check():
    return "Bot is running!", 200

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

async def main():
    global client
    logger.info("Starting Health Check server...")
    try:
        threading.Thread(target=run_flask, daemon=True).start()
    except Exception as e:
        logger.error(f"Failed to start Flask thread: {e}")

    logger.info("Checking MongoDB connection...")
    if not await database.check_connection():
        logger.critical("Could not connect to MongoDB. Please check your MONGO_URI and IP whitelist.")
        sys.exit(1)

    logger.info("Initializing Telegram Client...")
    try:
        client = TelegramClient(session, API_ID, API_HASH)
        
        # Register Handlers
        client.add_event_handler(start_handler, events.NewMessage(pattern='/start', from_users='me'))
        client.add_event_handler(help_handler, events.NewMessage(pattern='/help', from_users='me'))
        client.add_event_handler(add_handler, events.NewMessage(pattern='/add', from_users='me'))
        client.add_event_handler(remove_handler, events.NewMessage(pattern='/remove', from_users='me'))
        client.add_event_handler(list_handler, events.NewMessage(pattern='/list', from_users='me'))
        client.add_event_handler(clear_handler, events.NewMessage(pattern='/clear', from_users='me'))
        client.add_event_handler(contacts_handler, events.NewMessage(pattern='/load_contacts', from_users='me'))
        client.add_event_handler(group_handler, events.NewMessage(pattern='/load_group', from_users='me'))
        client.add_event_handler(broadcast_handler, events.NewMessage(pattern='/broadcast', from_users='me'))

        if STRING_SESSION:
            await client.start()
        else:
            logger.error("STRING_SESSION is missing! Cloud deployment requires a string session.")
            logger.info("Please run 'python generate_session.py' locally to get one.")
            sys.exit(1)
            
        logger.info("Client connected successfully!")
        print("\nUserbot is running! Send commands in Saved Messages or your Bot chat.\n")
        await client.run_until_disconnected()
    except Exception as e:
        logger.error(f"A critical error occurred during bot startup: {e}")
        sys.exit(1)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped.")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
