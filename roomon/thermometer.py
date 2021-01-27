#!/usr/bin/env python
import mcp9600
import time
from prometheus_client import start_http_server, Gauge

m = mcp9600.MCP9600()
m.set_thermocouple_type('K')

# Apparently the default i2c baudrate is too high you need to lower it: 
# set the followig line in the Pi's /boot/config.txt file
# dtparam=i2c_arm=on,i2c_arm_baudrate=40000

# Source:
# https://forums.pimoroni.com/t/mcp9600-breakout-pim437/13129/3
# https://www.raspberrypi-spy.co.uk/2018/02/change-raspberry-pi-i2c-bus-speed/

start_http_server(8002)

hotGauge = Gauge('roomon_mcp9600_hot_temp', 'Temperature at hot junction of thermocouple in C')
coldGauge = Gauge('roomon_mcp9600_cold_temp', 'Temperature at cold junction of thermocouple in C')
while True:
    t = m.get_hot_junction_temperature()
    c = m.get_cold_junction_temperature()
    d = m.get_temperature_delta()

    hotGauge.set(t)
    coldGauge.set(c)

    print(t, c, d)

    time.sleep(10)