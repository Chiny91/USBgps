#!/usr/bin/python

# Import some modules
import os       # Used for filer operations
import rrdtool
import serial
import re       # Used for string searching
import pynmea2

# Tested with gpsmon
# /dev/tty.usbmodem1431 9600 8N1

# Set up the USB (serial) port
port = serial.Serial("/dev/tty.usbmodem1431", 9600, timeout=0.5)

# Go round loop forever
while True:

    # Get a line of data where emonTH line ends with ")"
    response = ""
    eol = ")"
    while True:
        if response.endswith(eol):
            break
        else:
            response += port.read(1)
            
    # Remove first and last characters which may be junk,
    # using Python's slice notation
    response = response[1:-1]
    
    # Break up data into individual parameters
    parameters = re.findall('\d+', response)
    
    # Do the sums
    # https://community.openenergymonitor.org/t/emonth-data-output/3557/2
    temperature = (int(parameters[1])+int(parameters[2])*256)/10.0
    if temperature > 32768:
        temperature = temperature - 65536
    humidity = (int(parameters[5])+int(parameters[6])*256)/10.0
    batteryvolts = (int(parameters[7])+int(parameters[8])*256)/10.0
    rssi = -int(parameters[13])
    
    # Test everything
    import datetime
    print (datetime.datetime.now()), temperature, humidity, batteryvolts, rssi
    
    # Flush serial buffer
    # port.flushInput()

# Python appears to need a line with same indent as the program start
raise SystemExit
