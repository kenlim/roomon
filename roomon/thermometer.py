#!/usr/bin/env python
import mcp9600
import time

m = mcp9600.MCP9600()
m.set_thermocouple_type('k')

# Apparently the default i2c baudrate is too high you need to lower it: 
# https://forums.pimoroni.com/t/mcp9600-breakout-pim437/13129/3
# https://www.raspberrypi-spy.co.uk/2018/02/change-raspberry-pi-i2c-bus-speed/

while True:
    t = m.get_hot_junction_temperature()
    c = m.get_cold_junction_temperature()
    d = m.get_temperature_delta()

    print(t, c, d)

    time.sleep(1.0)