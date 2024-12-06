from time import sleep

import serial
from serial.tools import list_ports


def connect_antenna():
    while True:
        try:
            print(list_ports.comports())
            antenna = serial.Serial("/dev/ttyUSB0", 115200)
            print("Antenna connected ;)")
            return antenna
        except serial.SerialException:
            print("Antenna not pluged in ;(")
            sleep(1)


def write(msg, antenna):
    try:
        antenna.write(msg)
        return True
    except serial.SerialException:
        print("Write failed")
        return False
