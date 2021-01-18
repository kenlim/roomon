#!/usr/bin/env python
# Originally from here: https://github.com/pimoroni/bme680-python/blob/master/examples/read-all.py
from prometheus_client import start_http_server, Gauge
import bme680
import time
from datetime import datetime

print("""read-all.py - Displays temperature, pressure, humidity, and gas.

Press Ctrl+C to exit!

""")

try:
    sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
except IOError:
    sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)

# These calibration data can safely be commented
# out, if desired.

print('Calibration data:')
for name in dir(sensor.calibration_data):

    if not name.startswith('_'):
        value = getattr(sensor.calibration_data, name)

        if isinstance(value, int):
            print('{}: {}'.format(name, value))

# These oversampling settings can be tweaked to
# change the balance between accuracy and noise in
# the data.

sensor.set_humidity_oversample(bme680.OS_2X)
sensor.set_pressure_oversample(bme680.OS_4X)
sensor.set_temperature_oversample(bme680.OS_8X)
sensor.set_filter(bme680.FILTER_SIZE_3)
sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)

print('\n\nInitial reading:')
for name in dir(sensor.data):
    value = getattr(sensor.data, name)

    if not name.startswith('_'):
        print('{}: {}'.format(name, value))

sensor.set_gas_heater_temperature(320)
sensor.set_gas_heater_duration(150)
sensor.select_gas_heater_profile(0)

# Up to 10 heater profiles can be configured, each
# with their own temperature and duration.
# sensor.set_gas_heater_profile(200, 150, nb_profile=1)
# sensor.select_gas_heater_profile(1)

TEMPERATURE = Gauge('temperature', 'Measured temperature in C')
PRESSURE = Gauge('pressure', 'Measured pressure in hPa')
HUMIDITY = Gauge('humidity', 'Measured humidity in %RH')
GAS = Gauge('gas_resistance', 'Measured gas resistance in Ohms')

try:
    start_http_server(8000)
    while True:
        if sensor.get_sensor_data():
            temp = sensor.data.temperature
            pres = sensor.data.pressure
            humid = sensor.data.humidity

            TEMPERATURE.set(temp)
            PRESSURE.set(pres)
            HUMIDITY.set(humid)
            output = '{0}, {1:.2f} C, {2:.2f} hPa, {3:.2f} %RH'.format(
                datetime.now().isoformat(),
                temp,
                pres,
                humid)

            if sensor.data.heat_stable:
                g = sensor.data.gas_resistance
                
                GAS.set(g)

                output = ('{0}, {1} Ohms'.format(
                    output, g))
                print(output)
            else:
                print(output)
        time.sleep(1)

except KeyboardInterrupt:
    pass
