from config_loader import config
import requests

url = f"/localhost:{config['port']}"
myobj = {'text': '\n\n\nHi Lyndsey, you are hot!\n\n'}

x = requests.post(url, json=myobj)