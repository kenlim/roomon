import json
import requests
from configparser import ConfigParser
import time
from prometheus_client import start_http_server, Gauge

config = ConfigParser()
config.read("settings.ini")

pollFrequency = int(config["DEFAULT"]["pollFrequency"])
apiSettings = config["openweathermap"]

r = requests.get("http://api.openweathermap.org/data/2.5/weather", 
    {"id" : apiSettings["cityId"], 
    "units" : apiSettings["units"],
    "appid" : apiSettings["apiKey"]
    })

tempGauge = Gauge('openweathermap_temp', 'Temperature outside in C')

print(r.url)
while True:
    temp = r.json()["main"]["temp"]

    print(temp)

    tempGauge.set(temp)

    time.sleep(pollFrequency)

