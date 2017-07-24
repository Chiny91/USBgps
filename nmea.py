#!/usr/bin/python

# Import some modules, use pip install
import serial   # pyserial
import pynmea2  # https://github.com/Knio/pynmea2

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

    # Print info
    msg = pynmea2.parse(response)
    try:
        if msg.sentence_type == "GGA":
            print response
            print msg.timestamp
            print msg.lat, msg.lat_dir
            print msg.lon, msg.lon_dir
            print "Number of satellites", msg.num_sats
            print msg.altitude, msg.altitude_units
            stuff = window.refresh()
        elif msg.sentence_type == "TXT":
            print msg.text
        else:
            pass
    except:
        pass

# Python appears to need a line with same indent as the program start
raise SystemExit
