#!/usr/bin/env python3

import Adafruit_DHT

# Defining some constants
dht_sensor = Adafruit_DHT.DHT22
dht_pin = 4

# Reading the sensor and printing results
while True:
    humidity, temperature = Adafruit_DHT.read_retry(dht_sensor, dht_pin)

    if humidity is not None and temperature is not None:
        print("Temp={0:0.1f} C  Humidity={1:0.1f}%".format(temperature, humidity))
    else:
        print("Failed to retrieve data from humidity sensor")

