from prometheus_client import start_http_server, Gauge

class Prometheus_Logger:
    def __init__(self):
        start_http_server(8000)
        self.temp_g = Gauge('roomon_bme680_temperature', 'Measured temperature in C')
        self.pressure_g = Gauge('roomon_bme680_pressure', 'Measured pressure in hPa')
        self.humidity_g = Gauge('roomon_bme680_humidity', 'Measured humidity in %Rh')
        self.gas_g = Gauge('roomon_bme680_gas_resistance', 'Measured gas resistance in Ohms')

    def log(self, temperature, pressure, humidity, gas_resistance = None):
        self.temp_g.set(temperature)
        self.humidity_g.set(humidity)
        self.pressure_g.set(pressure)
        if gas_resistance is not None:
            self.gas_g.set(gas_resistance)    