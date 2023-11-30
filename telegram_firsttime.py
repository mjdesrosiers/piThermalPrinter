from telethon.sync import TelegramClient
import yaml

from config_loader import config

api_id = config['api_id']
api_hash = config['api_hash']
phone_number = config['phone_number']
grocery_chat_id = config['grocery_chat_id']
main_chat_id = config['main_chat_id']

client = TelegramClient('session_name', api_id, api_hash)
client.start()

# iterate through available chats:
# for dialog in client.iter_dialogs():
#     print(dialog)

# gets most recent message
message = client.get_messages(main_chat_id)
print(message)