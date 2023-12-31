import asyncio
import datetime
import traceback

import requests
from PIL import Image
from flask import Flask, request

import GPTSorter
import get_weather_data
from config_loader import config
from telethon.sync import TelegramClient

from get_calendar_data import get_upcoming_info, format_upcoming_info
from image_utils import ImageText

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
    from escpos.printer import Usb

    printer = Usb(config['printer_vid'], config['printer_pid'],
                  in_ep=0x81, out_ep=0x03)





def get_telegram_messages():
    api_id = config['api_id']
    api_hash = config['api_hash']
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    client = TelegramClient('session_name', api_id, api_hash, loop=loop)

    with client:
        item_set = set()
        chat_id = config['grocery_chat_id']
        for message in client.iter_messages(chat_id):
            if message.text:
                items = message.text.split('\n')
                items = [item.strip() for item in items if len(item.strip())]
                item_set.update(items)
    items_set = list(item_set)
    items_set = sorted(items_set)
    return items_set


def print_text(text):
    printer.text(text)
    printer.text('\n')

def print_image(filename):
    printer.image(filename)
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



last_grocery_time = None
@app.route(config["groceries"])
def do_groceries(*args):
    global last_grocery_time
    now = datetime.datetime.now()
    delta = datetime.timedelta(seconds=30)
    if last_grocery_time and (now < (last_grocery_time + delta)):
        return
    last_grocery_time = now
    items = get_telegram_messages()
    #messages = ["* " + item for item in items]
    text = "\n".join(items)
    text = GPTSorter.do_grocery_sort(text)
    img = ImageText((400, 10000), background=(255, 255, 255, 255)) # 200 = alpha
    font = 'arial.ttf'
    color = (0, 0, 0)
    dimensions = img.write_text_box(5, 5, text, box_width=390, font_filename=config['font_name'],
                       font_size=26, color=color)
    img.save('imagetext.png')
    im = Image.open(r"imagetext.png")
    width = im.size[0]
    height = dimensions[1]
    cropped = im.crop((0, 0, width, height))
    cropped.save("imagetext.png")
    print_image("imagetext.png")
    # print_text(text)
    return "Success!"


last_calendar_time = None
@app.route(config["calendar"])
def do_calendar(*args):
    global last_calendar_time
    now = datetime.datetime.now()
    delta = datetime.timedelta(seconds=30)
    if last_calendar_time and (now < (last_calendar_time + delta)):
        return
    last_calendar_time = now
    get_weather_data.make_weather_image()
    print_image('temp.png')
    message = format_upcoming_info(get_upcoming_info())
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
                              callback=do_groceries, bouncetime=5000)

        GPIO.setup(config["button_calendar"], GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(config["button_calendar"], GPIO.FALLING,
                              callback=do_calendar, bouncetime=5000)
    except ImportError:
        print("Platform does not support RPi GPIO")


# main driver function
if __name__ == '__main__':
    # run() method of Flask class runs the application
    # on the local development server.
    init_printer()
    setup_callbacks()
    app.run(port=config['port'])
