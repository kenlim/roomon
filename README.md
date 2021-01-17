# Roomon
This is a super simple room temperature monitor built on a Raspberry PI and some Pimoroni accessories. 

# Hardware
* Raspberry Pi v3 running Raspberry Pi OS
* [Pimoroni BME680](https://shop.pimoroni.com/products/bme680-breakout)
* [Pimoroni 1.3" LCD SPI display](https://shop.pimoroni.com/products/1-3-spi-colour-lcd-240x240-breakout)
* [Pimoroni Breakout Garden HAT](https://shop.pimoroni.com/products/breakout-garden-hat-i2c-spi)

# Installation 
## Hardware
* By default, the LCD screen should be installed in the *front* SPI slot
* The BME680 sensor goes in any I2C slot
  
## Setting up the Raspberry Pi 
OS setup is accomplished via 
```
> sudo-raspi-config
```

### Login immediately
```System option > Boot / Auto Login > Console Autologin```

This will allow the Pi to run in headless mode. 

### Configure hardware
Under *Interface options* enable:
* SSH
* SPI
* I2C

## Software setup
Install dependencies by executing
```
> sudo apt-get install pimoroni
```

## Project setup
This is a Python project since all the Pimoroni examples are in Python. I am copying and pasting code from these example projects:

* [Pimoroni BME680](https://github.com/pimoroni/bme680-python)
* [Pimoroni 1.3" LCD SPI display](https://github.com/pimoroni/st7789-python)

### The Hitchhiker's Guide to Python
I don't do much Python, so I am referring heavily to [The Hitchhiker's Guide to Python](https://docs.python-guide.org).

This project uses [pipenv](https://docs.python-guide.org/dev/virtualenvs/) for dependency management and running. I've installed it with:
``` 
> pip3 install --user pipenv 
```
This might complain that the pipenv folder has to be added to your path. You should do this.

```
set -Ua fish_user_paths /Users/YOURNAME/Library/Python/3.8/bin
```

Install dependencies 
```
> pipenv install
```

Install smbus on the RaspberryPi
Couldn't do this on the Mac because there is no library. So only do this on the Raspberry Pi before running:
```
> pipenv install smbus
```


Run basic app
```
> pipenv run python read_all.py
```




