from telethon.sync import TelegramClient, events

from constance import *

# Configure your API credentials
api_id = telegram_api_id_str
api_hash = telegram_api_hash_str
session_name = 'session_name'

# Create a Telegram client
client = TelegramClient(session_name, api_id, api_hash)
client.start()


# Define an event handler for new messages
@client.on(events.NewMessage(chats=telegram_channel_str))
async def handle_new_message(event):
    message = event.message
    signed_name = get_signed_name(message)
    print(f"Signed name: {signed_name}")

# Helper function to get the signature name from the message
def get_signed_name(message):
    if message.post_author:
        return message.post_author
    else:
        return "Unknown"

# Run the client
client.run_until_disconnected()