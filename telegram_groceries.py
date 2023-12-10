import requests
from PIL import Image

import GPTSorter
from config_loader import config
from image_utils import ImageText
from printer_server import get_telegram_messages


def trigger_print_messages():
    url = f"http://127.0.0.1:{config['port']}/{config['groceries']}"
    requests.get(url)


if __name__ == "__main__":
    messages = get_telegram_messages()
    text = "\n".join(messages)
    text = GPTSorter.do_grocery_sort(text)
    img = ImageText((400, 10000), background=(255, 255, 255, 255)) # 200 = alpha
    font = 'arial.ttf'
    color = (0, 0, 0)
    dimensions = img.write_text_box(5, 5, text, box_width=390, font_filename=config['font_name'],
                       font_size=22, color=color)
    img.save('imagetext.png')
    im = Image.open(r"imagetext.png")
    width = im.size[0]
    height = dimensions[1]
    cropped = im.crop((0, 0, width, height))
    cropped.save("imagetext.png")
