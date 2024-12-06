from time import sleep

import serial
from serial.tools import list_ports


def connect_antenna():
    while True:
        try:
            ports = serial.tools.list_ports.comports()
            usb_tty_ports = [port.device for port in ports if "USB" in port.description or "tty" in port.device]
            print(usb_tty_ports)
            
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
