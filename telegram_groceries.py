import requests
from config_loader import config

def trigger_print_messages():
    url = f"http://127.0.0.1:{config['port']}/{config['groceries']}"
    requests.get(url)


if __name__ == "__main__":
    trigger_print_messages()
