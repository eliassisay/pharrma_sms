# Telegram Multi-Sender Userbot

A powerful Telegram userbot that allows you to broadcast messages to multiple users from your personal account.

## Features
- **Send from YOU**: Messages appear as normal private chats from your account.
- **MongoDB Backend**: Selected users and broadcast logs are persisted in MongoDB.
- **Command Based**: Control everything from your "Saved Messages" chat.
- **Media Support**: Broadcast text, photos, videos, or documents by replying to them.
- **Group/Contact Importer**: Quickly add users from your contacts or any public group.
- **Flood Handling**: Built-in delays and automatic handling of `FloodWait`.

## Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **MongoDB**:
   Ensure MongoDB is running. If using a custom URI, set it in your environment:
   ```bash
   export MONGO_URI="mongodb://localhost:27017/"
   ```

3. **Run the Userbot**:
   ```bash
   python multi_sender.py
   ```
   *Note: On first run, it will ask for your phone number and the OTP code sent to your Telegram.*

## How to Use
Send these commands in your **Saved Messages**:

| Command | Description |
| :--- | :--- |
| `/add @user1 @user2` | Add users by username or ID |
| `/remove @user1` | Remove users from the list |
| `/list` | Show current selection |
| `/clear` | Remove all users from selection |
| `/load_contacts` | Add all your personal contacts to the list |
| `/load_group @group` | Add all members from a group |
| `/broadcast <text>` | Send message to selection |
| `/broadcast` (as reply) | Broadcast the message you replied to (works for media) |

---
**Warning**: Use responsibly. Sending too many messages to non-contacts too quickly can result in your account being restricted by Telegram.
