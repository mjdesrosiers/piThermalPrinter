import printer_server
from config_loader import config
from telethon.sync import TelegramClient


def get_telegram_messages():
    api_id = config['api_id']
    api_hash = config['api_hash']
    main_chat_id = config['main_chat_id']

    client = TelegramClient('session_name', api_id, api_hash)
    client.start()

    # gets most recent message
    message = client.get_messages(main_chat_id)
    return [message]


if __name__ == "__main__":
    messages = get_telegram_messages()
    text = "\n".join(messages)
    printer_server.send_message_to_server(text)
