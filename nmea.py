#!/usr/bin/python

# Import some modules, use pip install <module> if missing
import curses
import serial   # pyserial
import pynmea2  # https://github.com/Knio/pynmea2
import sys

def main(stdscr):
    curses.start_color()
    curses.use_default_colors()
    for i in range(0, curses.COLORS):
        curses.init_pair(i + 1, i, -1)
    # Set up the USB (serial) port
    port = serial.Serial("/dev/tty.usbmodem1431", 4800, timeout = None)
    while True:
        try:
            response = port.readline()   # read a '\n' terminated line
            msg = pynmea2.parse(response)
            if msg.sentence_type == "GGA":
                stdscr.addstr(0, 0, str(msg.timestamp), curses.color_pair(2))
                stdscr.addstr(1, 3, msg.lat, curses.color_pair(1))
                stdscr.addstr(1, 0, msg.lat_dir, curses.color_pair(1))
                stdscr.addstr(2, 3, msg.lon, curses.color_pair(1))
                stdscr.addstr(2, 0, msg.lon_dir, curses.color_pair(1))
                stdscr.addstr(3, 0, "Altitude", curses.color_pair(1))
                stdscr.addstr(3, 9, str(msg.altitude), curses.color_pair(1))
                stdscr.addstr(3, 14, msg.altitude_units, curses.color_pair(1))
                stdscr.addstr(4, 0, "Number of satellites", curses.color_pair(2))
                stdscr.addstr(4, 21, msg.num_sats, curses.color_pair(2))
                stdscr.addstr(5, 0, "", curses.color_pair(1))
                stdscr.refresh()
        except ParseError:    # Ignore any errors from pynmea2
            pass
        except:
            print "Unexpected error:", sys.exc_info()[0]
            raise

# Initialize curses and call another function,
# which is the rest of curses-using application,
# then gracefully exit curses and tidy up terminal
curses.wrapper(main)

# Exit Python
raise SystemExit
