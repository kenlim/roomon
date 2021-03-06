import json
import requests
from configparser import ConfigParser
import time
from prometheus_client import start_http_server, Gauge

config = ConfigParser()
config.read("settings.ini")

apiSettings = config["openweathermap"]


tempGauge = Gauge('openweathermap_temp', 'Temperature outside in C')

start_http_server(8001)

while True:
    r = requests.get("http://api.openweathermap.org/data/2.5/weather", 
        {"id" : apiSettings["cityId"], 
        "units" : apiSettings["units"],
        "appid" : apiSettings["apiKey"]
        })

    json = r.json()    
    temp = json["main"]["temp"]
    humidity = json["main"]["humidity"]
    pressure = json["main"]["pressure"]
    timestamp = r.headers["Date"]
    print("{0}, {1}, {2}, {3}".format(timestamp, temp, pressure, humidity))

    tempGauge.set(temp)

    time.sleep(int(apiSettings["pollInterval"]))

