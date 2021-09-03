#!/usr/bin/env python3

# Data reading adapted from:
# https://learn.adafruit.com/adafruit-max31856-thermocouple-amplifier/python-circuitpython

import time
import board
import digitalio
import adafruit_max31856

# Import LED libraries
import re
import time

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT

def create_sensor():
    # Create sensor object
    spi = board.SPI()
    
    # Allocate CS pin and set direction
    cs = digitalio.DigitalInOut(board.D5)
    cs.direction = digitalio.Direction.OUTPUT

    # Make it work with type T thermocouple
    tc_type = adafruit_max31856.ThermocoupleType.T
    
    # Create thermocouple object
    thermocouple = adafruit_max31856.MAX31856(spi,cs,tc_type)

    return(thermocouple)
    
    # Print temperature
    #while True:
    #	print(thermocouple.temperature)
    #    time.sleep(1.0)

def create_led_device():
    # create matrix device
    serial = spi(port=0, device=1, gpio=noop())
    device = max7219(serial, cascaded=4, block_orientation=-90,
                     rotate=0, blocks_arranged_in_reverse_order=False)
    return(device)

if __name__ == "__main__":
    # Setting up the thermocouple
    thermocouple = create_sensor()

    # Setting up the display
    device = create_led_device()

    # Showing the temp on the display
    #show_message(device, msg, fill="white", font=proportional(CP437_FONT))

    # Opening message
    msg = "Thermocouple active"
    show_message(device, msg, fill="white", font=proportional(LCD_FONT), scroll_delay=0.05)

    # Temperature loop
    while True:
        # Getting the temp
        temp_string = str(format(thermocouple.temperature, '.4f'))

        with canvas(device) as draw:
            text(draw, (0,0), temp_string, fill="white", font=proportional(LCD_FONT))

        time.sleep(1)
