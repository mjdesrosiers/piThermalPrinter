from printer_server import send_message_to_server
from config_loader import config
from telethon.sync import TelegramClient


def get_telegram_messages():
    # modification
    api_id = config['api_id']
    api_hash = config['api_hash']
    chat_id = config['grocery_chat_id']

    client = TelegramClient('session_name', api_id, api_hash)
    client.start()

    item_set = {}
    for message in client.iter_messages(chat_id):
        items = message.text().split('\n')
        items = [item.strip() for item in items]
        item_set.update(items)

    return list(item_set)


if __name__ == "__main__":
    messages = get_telegram_messages()
    text = "\n".join(messages)
    send_message_to_server(text)
