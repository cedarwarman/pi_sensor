#!/usr/bin/env python3

# Data reading adapted from https://pimylifeup.com/raspberry-pi-humidity-sensor-dht22/

import os
import time
import Adafruit_DHT
import gspread


### Open the file to write out
def open_output_file():
    if not os.path.exists('/home/pi/Documents/pi_sensor/output/'):
        os.makedirs('/home/pi/Documents/pi_sensor/output/')

    try:
        f = open('/home/pi/Documents/pi_sensor/output/sensor_output.csv', 'a+')
        if os.stat('/home/pi/Documents/pi_sensor/output/sensor_output.csv').st_size == 0:
                f.write('date\ttime\ttemp_c\ttemp_f\thumidity\r\n')
        return(f)
    except:
        pass

### Read the sensor 
def read_sensor(dht_sensor, dht_pin):
    humidity, temp_c = Adafruit_DHT.read_retry(dht_sensor, dht_pin)

    if humidity is not None and temp_c is not None:
        # C to F conversion
        temp_f = (temp_c * 9/5) + 32

        # Test print
        # print("Temp={0:0.1f} C ({1:0.1f} F) Humidity={2:0.1f}%".format(temp_c, temp_f, humidity))

        sensor_list = [time.strftime('%H:%M:%S'), temp_c, temp_f, humidity]
        return(sensor_list)

    else:
        print("Failed to retrieve data from humidity sensor")

### Append to file
def append_file(input_file_handle, input_list):
    try:
        input_file_handle.write('{0}\t{1}\t{2:0.1f}\t{3:0.1f}\t{4:0.1f}\r\n'.format(time.strftime('%Y-%m-%d'),
        input_list[0], input_list[1], input_list[2], input_list[3]))
        input_file_handle.flush()
    except:
        print("Fail to write to file")

### Append to Google sheet
def append_google_sheet(input_list, sheet_key):
    try:
        # Setting up the service account info
        # (/home/pi/.config/gspread/service_account.json)
        gc = gspread.service_account()

        # Reading the sheet
        sheet = gc.open_by_key(sheet_key).sheet1    

        # Writing the data
        append_list = [time.strftime('%Y-%m-%d'), 
        input_list[0], 
        round(input_list[1], 1), 
        round(input_list[2], 1), 
        round(input_list[3], 1)]
        sheet.append_row(append_list)
    except:
        print("Failed to upload to Google Sheets")


def main():
    # Defining some constants
    dht_sensor = Adafruit_DHT.DHT22
    dht_pin = 4
    start_time = time.time() # Initial time for fancy sleep

    while True:
        f = open_output_file()
        sensor_output = read_sensor(dht_sensor, dht_pin)
        # print(sensor_output)
        append_file(f, sensor_output)
        # Appends to sheet that has all the data
        append_google_sheet(sensor_output, '1v0W5jSeF_wNWV9JCeZlG_zNOOsADDlPmwQSymcgLEJQ')
        # Appends to sheet that just has the past 7 days (pruned by another
        # script on a different raspberry pi)
        append_google_sheet(sensor_output, '1pb0uU-8VST4gp8zkbDiO0YNfAKdsnvoKgLZ63juG27I')
        time.sleep(60.0 - ((time.time() - start_time) % 60.0))


if __name__ == "__main__":
    main()
