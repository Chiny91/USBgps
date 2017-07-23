#!/usr/bin/python

# Import some modules
import os       # Used for filer operations
import rrdtool
import serial   # pip install pyserial
import re       # Used for string searching
import pynmea2

# Each NMEA line begins with a '$' and ends with a carriage return/line feed sequence
# and can be no longer than 80 characters of visible text (plus the line terminators)

# Clobber the port (as root)
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
            
    # Remove first and last characters which may be junk,
    # using Python's slice notation
    response = response[1:-1]
    
    # Break up data into individual parameters
    parameters = re.findall('\d+', response)
    
    # Do the sums

    
    # Test everything
    print response
    
    # Flush serial buffer
    # port.flushInput()

# Python appears to need a line with same indent as the program start
raise SystemExit
