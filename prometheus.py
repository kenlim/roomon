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

start_time = time.time()
burn_in_time = 300
burn_in_data = []
gas_baseline = None

# Set the humidity baseline to 40%, an optimal indoor humidity.
hum_baseline = 40.0

# This sets the balance between humidity and gas reading in the
# calculation of air_quality_score (25:75, humidity:gas)
hum_weighting = 0.25

sensor.set_gas_heater_temperature(320)
sensor.set_gas_heater_duration(150)
sensor.select_gas_heater_profile(0)

# Up to 10 heater profiles can be configured, each
# with their own temperature and duration.
# sensor.set_gas_heater_profile(200, 150, nb_profile=1)
# sensor.select_gas_heater_profile(1)

temp_g = Gauge('roomon_bme680_temperature', 'Measured temperature in C')
pressure_g = Gauge('roomon_bme680_pressure', 'Measured pressure in hPa')
humidity_g = Gauge('roomon_bme680_humidity', 'Measured humidity in %RH')
gas_g = Gauge('roomon_bme680_gas_resistance', 'Measured gas resistance in Ohms')
air_g = Gauge('roomon_bme680_air_quality_score', 'Calculated air quality score')

try:
    start_http_server(8000)
    while True:
        if sensor.get_sensor_data():
            temp = sensor.data.temperature
            pres = sensor.data.pressure
            humid = sensor.data.humidity

            temp_g.set(temp)
            pressure_g.set(pres)
            humidity_g.set(humid)
            output = '{0}, {1:.2f} C, {2:.2f} hPa, {3:.2f} %RH'.format(
                datetime.now().isoformat(),
                temp,
                pres,
                humid)
            print(output)
            
            now = time.time()
            if (now - start_time < burn_in_time) and sensor.data.heat_stable:
                gas = sensor.data.gas_resistance
                burn_in_data.append(gas)
            elif (now - start_time > burn_in_time) and sensor.data.heat_stable:
                if gas_baseline is None:
                    gas_baseline = sum(burn_in_data[-50:]) / 50.0

                gas = sensor.data.gas_resistance
                gas_offset = gas_baseline - gas

                hum = sensor.data.humidity
                hum_offset = hum - hum_baseline

                # Calculate hum_score as the distance from the hum_baseline.
                if hum_offset > 0:
                    hum_score = (100 - hum_baseline - hum_offset)
                    hum_score /= (100 - hum_baseline)
                    hum_score *= (hum_weighting * 100)

                else:
                    hum_score = (hum_baseline + hum_offset)
                    hum_score /= hum_baseline
                    hum_score *= (hum_weighting * 100)

                # Calculate gas_score as the distance from the gas_baseline.
                if gas_offset > 0:
                    gas_score = (gas / gas_baseline)
                    gas_score *= (100 - (hum_weighting * 100))

                else:
                    gas_score = 100 - (hum_weighting * 100)

                # Calculate air_quality_score.
                air_quality_score = hum_score + gas_score

                output = ('{0}, {1} Ohms, {2}'.format(output, gas, air_quality_score))
                
                air_g.set(air_quality_score)
                gas_g.set(gas)
                print(output)
            else:
                print(output)
        time.sleep(10)

except KeyboardInterrupt:
    pass
