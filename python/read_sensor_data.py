#!/usr/bin/env python3

# Data reading adapted from https://pimylifeup.com/raspberry-pi-humidity-sensor-dht22/

import os
import time
import Adafruit_DHT

# Defining some constants
dht_sensor = Adafruit_DHT.DHT22
dht_pin = 4


# Opening the file to write out
if not os.path.exists('/home/pi/Documents/pi_sensor/output/'):
    os.makedirs('/home/pi/Documents/pi_sensor/output/')

try:
    f = open('/home/pi/Documents/pi_sensor/output/sensor_output.csv', 'a+')
    if os.stat('/home/pi/Documents/pi_sensor/output/sensor_output.csv').st_size == 0:
            f.write('date\ttime\ttemp_c\ttemp_f\thumidity\r\n')
except:
    pass

# Reading the sensor and printing results
while True:
    humidity, temp_c = Adafruit_DHT.read_retry(dht_sensor, dht_pin)

    if humidity is not None and temp_c is not None:
        # Adding C to F conversion
        temp_f = (temp_c * 9/5) + 32

        print("Temp={0:0.1f} C ({1:0.1f} F) Humidity={2:0.1f}%".format(temp_c, temp_f, humidity))

        # Writing to the file
        f.write('{0}\t{1}\t{2:0.1f}\t{3:0.1f}\t{4:0.1f}\r\n'.format(time.strftime('%m/%d/%y'),
        time.strftime('%H:%M'), temp_c, temp_f, humidity))

    else:
        print("Failed to retrieve data from humidity sensor")

    time.sleep(120)

