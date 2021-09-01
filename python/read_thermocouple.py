#!/usr/bin/env python3

# Data reading adapted from:
# https://learn.adafruit.com/adafruit-max31856-thermocouple-amplifier/python-circuitpython

import time
import board
import digitalio
import adafruit_max31856

# Create sensor object
spi = board.SPI()

# Allocate CS pin and set direction
cs = digitalio.DigitalInOut(board.D5)
cs.direction = digitalio.Direction.OUTPUT

# Create thermocouple object
thermocouple = adafruit_max31856.MAX31856(spi,cs)

# Print temperature
while True:
	print(thermocouple.temperature)
	time.sleep(1.0)
