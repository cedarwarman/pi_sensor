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
    
    # Create thermocouple object
    thermocouple = adafruit_max31856.MAX31856(spi,cs)

    return(thermocouple)
    
    # Print temperature
    #while True:
    #	print(thermocouple.temperature)
    #    time.sleep(1.0)

def create_led_device():
    # create matrix device
    serial = spi(port=0, device=0, gpio=noop())
    device = max7219(serial, cascaded=4, block_orientation=-90,
                     rotate=0, blocks_arranged_in_reverse_order=False)
    return(device)

if __name__ == "__main__":
    # Setting up the thermocouple
#    thermocouple = create_sensor()

    # Getting the temp
    #msg = str(thermocouple.temperature)
    #msg = re.sub(" +", " ", msg)
    msg = "36.6123456"
#    print(msg)

    # Setting up the display
    device = create_led_device()

    # Showing the temp on the display
    #show_message(device, msg, fill="white", font=proportional(CP437_FONT))
    while True:
        with canvas(device) as draw:
            text(draw, (0,0), msg, fill="white", font=proportional(LCD_FONT))

## create matrix device
#    serial = spi(port=0, device=0, gpio=noop())
#    device = max7219(serial, cascaded=4, block_orientation=-90,
#                     rotate=0, blocks_arranged_in_reverse_order=False)
#    print("Created device")
#
#    # start demo
##    msg = "MAX7219 LED Matrix Demo"
#    print(msg)
#    show_message(device, msg, fill="white", font=proportional(CP437_FONT))
#    time.sleep(1)
#
#    msg = "Fast scrolling: Lorem ipsum dolor sit amet, consectetur adipiscing\
#    elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut\
#    enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut\
#    aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in\
#    voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint\
#    occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit\
#    anim id est laborum."
#    msg = re.sub(" +", " ", msg)
#    print(msg)
#    show_message(device, msg, fill="white", font=proportional(LCD_FONT), scroll_delay=0)
