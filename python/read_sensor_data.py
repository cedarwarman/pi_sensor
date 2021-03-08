#!/usr/bin/env python3

# Data reading adapted from https://pimylifeup.com/raspberry-pi-humidity-sensor-dht22/

import Adafruit_DHT

# Defining some constants
dht_sensor = Adafruit_DHT.DHT22
dht_pin = 4

# Reading the sensor and printing results
while True:
    humidity, temp_c = Adafruit_DHT.read_retry(dht_sensor, dht_pin)

    if humidity is not None and temp_c is not None:
        # Adding C to F conversion
        temp_f = (temp_c * 9/5) + 32

        print("Temp={0:0.1f} C ({1:0.1f} F) Humidity={2:0.1f}%".format(temp_c, temp_f, humidity))

    else:
        print("Failed to retrieve data from humidity sensor")

