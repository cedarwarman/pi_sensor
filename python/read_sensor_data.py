#!/usr/bin/env python3

# Data reading adapted from https://pimylifeup.com/raspberry-pi-humidity-sensor-dht22/

import os
import time
import glob
import Adafruit_DHT
import gspread
import argparse

### Setting up arguments
parser = argparse.ArgumentParser(description='Read Raspberry Pi DHT22 sensor data')
parser.add_argument('-p',
                    '--path',
                    type=str,
                    help='Path to Google Sheet URL code file')
args = parser.parse_args()

### Open Google Sheet URLs file
# The url file is a tsv file with key value pairs as follows:
# all   Google_spreadsheet_ID
# week  Google_spreadsheet_ID
# month Google_spreadsheet_ID
def open_url_files(dir_path, sensor_list):
    url_dict = {}
    for file_path in glob.glob(dir_path + '*'):
        print("working on " + file_path)
        # Getting the file name
        file_string = os.path.basename(file_path)
        file_string = os.path.splitext(file_string)[0]
        # Checking to see if it's on the sensor_list
        print("file_string: " + file_string)
        #print("sensor_list: " + sensor_list)
        if any(sensor_string in file_string for sensor_string in sensor_list):
            print("Matched string")
            with open(file_path, 'r') as url_file:
                nest_dict = {}
                for line in url_file:
                    # Adding values to the nested dictionary
                    (key, value) = line.split()
                    nest_dict[key] = value
                # Adding the nested dictionary to the main dictionary
                url_dict[file_string] = nest_dict
        else:
            print("no match")
    return(url_dict)

### Open the file to write out
def open_output_file():
    if not os.path.exists('/home/pi/Documents/pi_sensor/output/'):
        os.makedirs('/home/pi/Documents/pi_sensor/output/')

    try:
        f = open('/home/pi/Documents/pi_sensor/output/sensor_output.csv', 'a+')
        if os.stat('/home/pi/Documents/pi_sensor/output/sensor_output.csv').st_size == 0:
                f.write('date\ttime\ttemp_c\ttemp_f\thumidity\tpin\r\n')
        return(f)
    except:
        pass


### Read the sensor 
def read_sensor(dht_sensor, dht_pin, input_time):
    humidity, temp_c = Adafruit_DHT.read_retry(dht_sensor, dht_pin)

    if humidity is not None and temp_c is not None:
        # C to F conversion
        temp_f = (temp_c * 9/5) + 32

        # Test print
        # print("Temp={0:0.1f} C ({1:0.1f} F) Humidity={2:0.1f}%".format(temp_c, temp_f, humidity))

        sensor_list = [time.strftime('%H:%M:%S', input_time), temp_c, temp_f, humidity]
        return(sensor_list)

    else:
        print("Failed to retrieve data from humidity sensor")


### Append to file
def append_file(input_file_handle, input_list, input_time, dht_pin):
    try:
        input_file_handle.write('{0}\t{1}\t{2:0.1f}\t{3:0.1f}\t{4:0.1f}\t{5}\r\n'.format(time.strftime('%Y-%m-%d',
        input_time),
        input_list[0], input_list[1], input_list[2], input_list[3], dht_pin))
        input_file_handle.flush()
    except:
        print("Fail to write to file")


### Append to Google sheet
def append_google_sheet(input_list, sheet_key, input_time):
    try:
        # Setting up the service account info
        # (/home/pi/.config/gspread/service_account.json)
        gc = gspread.service_account()

        # Reading the sheet
        sheet = gc.open_by_key(sheet_key).sheet1    

        # Writing the data
        append_list = [time.strftime('%Y-%m-%d', input_time), 
        input_list[0], 
        round(input_list[1], 1), 
        round(input_list[2], 1), 
        round(input_list[3], 1)]
        sheet.append_row(append_list)
    except:
        print("Failed to upload to Google Sheets")


def main():
    print("started program")
    # Defining some constants
    dht_sensor = Adafruit_DHT.DHT22
    #dht_pin = 4
    start_time = time.time() # Initial time for fancy sleep
    # Opening the file with the Google sheet IDs
    ######              FIX THIS IN SYSTEMCTL            ######
    ###### CURRENTLY: ADD SENSORS TO MEASURE TO LIST ARG ######
    sheet_ids = open_url_files('/home/pi/Documents/pi_sensor/url/', 
        ["home_1", "home_2"]) ###### CHANGE SENSORS HERE
    print("this is the library:")
    print(sheet_ids)

    f = open_output_file()

    while True:
        # Gives everything the same time to fix a bug that came from calling 
        # time() a bunch of times
        read_time = time.localtime()
        
        for sensor_location, sensor_dict in sheet_ids.items():
            print("In for loop")
            print(sensor_location)
            print(sensor_dict)

            dht_pin = sensor_dict.get('pin')
            sensor_output = read_sensor(dht_sensor, dht_pin, read_time)
            print(sensor_output)
            append_file(f, sensor_output, read_time, dht_pin)
            # Appends to sheet that has all the data
            append_google_sheet(sensor_output, sensor_dict.get('all'), read_time)
            # Appends to sheet that just has the past 7 days (pruned by another
            # script on a different raspberry pi)
            append_google_sheet(sensor_output, sensor_dict.get('week'), read_time)
            # Appends to sheet that has the past 30 days
            append_google_sheet(sensor_output, sensor_dict.get('month'), read_time)
            time.sleep(60.0 - ((time.time() - start_time) % 60.0))


if __name__ == "__main__":
    main()
