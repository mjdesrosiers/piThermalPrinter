import asyncio
import traceback

import requests
from flask import Flask, request
from config_loader import config
from escpos.printer import Usb
from telethon.sync import TelegramClient


app = Flask(__name__)

printer = None
client = None
loop = None

def start_background_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

def init_printer():
    global printer
    global loop

    printer = Usb(config['printer_vid'], config['printer_pid'],
                  in_ep=0x81, out_ep=0x03)





def get_telegram_messages():
    api_id = config['api_id']
    api_hash = config['api_hash']
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    client = TelegramClient('session_name', api_id, api_hash, loop=loop)
    client.start()
    item_set = {}
    chat_id = config['grocery_chat_id']
    for message in client.iter_messages(chat_id):
        items = message.text().split('\n')
        items = [item.strip() for item in items]
        item_set.update(items)
    items_set = list(item_set)

    return items_set


def print_text(text):
    printer.text(text)
    printer.text('\n')


@app.route("/")
def hello_world():
    search = request.args.get("search")
    page = request.args.get("page")
    return f"<p>Hello, World!<br><br>{search} --> {page}</p>"


@app.route(config["post_endpoint"], methods=['POST'])
def receive_new_request():
    if request.method == "POST":
        text = request.form.get('text')
        print_text(text)


@app.route(config["groceries"])
def do_groceries():
    items = get_telegram_messages()
    messages = ["* " + item for item in items]
    message = "\n".join(messages)
    print_text(message)
    return "Success!"


def send_message_to_server(message_text):
    obj = {'text': message_text}
    url = f"http://127.0.0.1:{config['port']}/{config['post_endpoint']}"
    result = requests.post(url, obj)


def setup_callbacks():
    try:
        import RPi.GPIO as GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(config["button_grocery"], GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(config["button_grocery"], GPIO.FALLING,
                              callback=do_groceries, bouncetime=250)
    except:
        print("Platform does not support RPi GPIO")


# main driver function
if __name__ == '__main__':
    # run() method of Flask class runs the application
    # on the local development server.
    init_printer()
    setup_callbacks()
    app.run(port=config['port'])
