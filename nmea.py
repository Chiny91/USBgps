#!/usr/bin/python

# Import some modules, use pip install <module> if missing
import curses
import serial   # pyserial
import pynmea2  # https://github.com/Knio/pynmea2
import sys
from time import gmtime, strftime

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
                stdscr.addstr(0, 0, "iMac time:", curses.color_pair(1))
                stdscr.addstr(0, 11, str(strftime("%H:%M:%S", gmtime())), curses.color_pair(1))
                stdscr.addstr(1, 0, "GPS time:", curses.color_pair(2))
                stdscr.addstr(1, 11, str(msg.timestamp), curses.color_pair(2))
                stdscr.addstr(2, 3, str(msg.latitude), curses.color_pair(2))
                stdscr.addstr(2, 0, msg.lat_dir, curses.color_pair(2))
                stdscr.addstr(3, 3, str(msg.longitude), curses.color_pair(2))
                stdscr.addstr(3, 0, msg.lon_dir, curses.color_pair(2))
                stdscr.addstr(4, 0, "Altitude", curses.color_pair(2))
                stdscr.addstr(4, 9, str(msg.altitude), curses.color_pair(2))
                stdscr.addstr(4, 14, msg.altitude_units, curses.color_pair(2))
                stdscr.addstr(5, 0, "Number of satellites in use:", curses.color_pair(2))
                stdscr.addstr(5, 30, msg.num_sats, curses.color_pair(2))
                stdscr.refresh()
            if msg.sentence_type == "GSV":
                stdscr.addstr(6, 0, "Number of satellites in view:", curses.color_pair(2))
                stdscr.addstr(6, 30, str(msg.num_sv_in_view), curses.color_pair(2))
                stdscr.addstr(9, 0, "Message Number:", curses.color_pair(1))
                stdscr.addstr(9, 16, str(msg.msg_num), curses.color_pair(1))
                stdscr.addstr(10, 0, "Number of messages in GSV cycle:", curses.color_pair(1))
                stdscr.addstr(10, 33, str(msg.num_messages), curses.color_pair(1))
                stdscr.addstr(11, 0, "", curses.color_pair(1))
                stdscr.refresh()
            # Ignore RMC, VTG, GLL messages as no additional information
            # Ignore TXT message as never changes
        except pynmea2.ParseError:
            pass
        except:
            print "Nobody expects an inquistion about this error:", sys.exc_info()[0]
            raise

# Initialize curses and call another function,
# which is the rest of curses-using application,
# then gracefully exit curses and tidy up terminal
curses.wrapper(main)

# Exit Python
raise SystemExit
