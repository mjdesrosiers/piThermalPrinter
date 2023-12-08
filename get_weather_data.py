from PIL import ImageFont, ImageDraw
from pyowm import OWM
from pyowm.utils import config
from pyowm.utils import timestamps
from datetime import datetime

from PIL import Image, ImageOps
import urllib.request

from config_loader import config

def make_weather_image():

    owm = OWM(config["OWM_key"])
    mgr = owm.weather_manager()

    observation = mgr.weather_at_coords(config["lat"], config["lon"])
    w = observation.weather

    weather_status = w.detailed_status
    weather_status = weather_status[0].upper() + weather_status[1:]
    weather_icon = w.weather_icon_name
    # 100 x 100 image
    weather_icon_url = f"https://openweathermap.org/img/wn/{weather_icon}@2x.png"


    temp = 'temp.png'
    urllib.request.urlretrieve(weather_icon_url, temp)


    t_max = round(w.temperature('fahrenheit')['temp_max'])
    t_min = round(w.temperature('fahrenheit')['temp_min'])
    t_cur = round(w.temperature('fahrenheit')['temp'])
    temp_message = f"Now: {t_cur} H:{t_max} L:{t_min}"
    icon = Image.open(temp)

    now = datetime.now()
    now = now.strftime("%Y-%m-%d - %A")

    image = Image.new('RGB', (400, 100))


    font = ImageFont.truetype("DejaVuSans.ttf", 20)
    draw = ImageDraw.Draw(image)
    draw.rectangle([0, 0, 400, 100], fill="#ffffff")
    draw.rectangle([1, 1, 399, 99], fill="#000000")

    draw.text((100, 10), f"{now}\n{temp_message}\n{weather_status}", (255, 255, 255), font=font)
    image = ImageOps.invert(image)
    #image = ImageOps.posterize(image, 1)
    image.paste(icon)
    image.show()


    image.save(temp)

    #forecast = mgr.three_hour_forecast(config["location"])



