#!/usr/bin/python

# Import some modules
import serial   # pip install pyserial
import pynmea2  # https://github.com/Knio/pynmea2
import re       # used for string searching

# To reset, clobber the port (as root)
# cu -l /dev/tty.usbmodem1431 -s 9600

# Tested with gpsmon
# /dev/tty.usbmodem1431 9600 8N1

# Set up the USB (serial) port
port = serial.Serial("/dev/tty.usbmodem1431", 9600, timeout=0.5)

# Go round loop forever
while True:

    # Get a line of NMEA data ending with "\n"
    response = ""
    eol = "\n"
    while True:
        if response.endswith(eol):
            break
        else:
            response += port.read(1)
            
    # Remove initial ($) and last (\n) characters using Python's slice notation
    response = response[1:-1]
    
    # Break up data into individual parameters
    parameters = re.findall('\d+', response)
    
    # Extract the data
    # messagetype  = parameters(1)
    
    # Test everything
    print response
    print parameters
    
    # Flush serial buffer
    # port.flushInput()

# Python appears to need a line with same indent as the program start
raise SystemExit
