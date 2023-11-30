import traceback

import requests
from flask import Flask, request
from config_loader import config

app = Flask(__name__)

p = None


def init_printer():
    try:
        from escpos.printer import Usb
        p = Usb(config['printer_vid'], config['printer_pid'], 0, profile="TM-T88III")
    except Exception as e:
        print(e)
        traceback.print_exc()


def print_text(text):
    p.text(text)
    p.text('\n')


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


def send_message_to_server(message_text):
    obj = {'text': message_text}
    url = f"http://127.0.0.1:{config['port']}/{config['post_endpoint']}"
    result = requests.post(url, obj)


def do_grocery_callback():
    pass


def setup_callbacks():
    try:
        import RPi.GPIO as GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(config["button_grocery"], GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(config["button_grocery"], GPIO.FALLING,
                              callback=do_grocery_callback, bouncetime=250)
    except:
        print("Platform does not support RPi GPIO")


# main driver function
if __name__ == '__main__':
    # run() method of Flask class runs the application
    # on the local development server.
    init_printer()
    setup_callbacks()
    app.run(port=config['port'])
