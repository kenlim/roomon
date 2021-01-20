import json
import requests
from configparser import ConfigParser


config = ConfigParser()
config.read("settings.ini")

apiSettings = config["openweathermap"]

r = requests.get("http://api.openweathermap.org/data/2.5/weather", 
    {"id" : apiSettings["cityId"], 
    "units" : apiSettings["units"],
    "appid" : apiSettings["apiKey"]
    })


print(r.json()["main"]["temp"])

