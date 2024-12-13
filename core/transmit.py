import syslog
from time import sleep

import serial


def connect_antenna():
    while True:
        try:
            antenna = serial.Serial("/dev/serial0", 115200)
            print("Antenna connected ;)")
            syslog.syslog("Antenna connected ;)")
            return antenna
        except serial.SerialException:
            print("Antenna not pluged in ;(")
            syslog.syslog("Antenna not pluged in ;(")
            sleep(1)


def write(msg, antenna):
    try:
        antenna.write(msg)
        return True
    except serial.SerialException:
        print("Write failed")
        syslog.syslog("Write failed")
        return False
