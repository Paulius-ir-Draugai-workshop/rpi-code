import syslog
from time import sleep

import serial
from serial.tools import list_ports


def connect_antenna():
    while True:
        try:
            ports = list_ports.comports()
            usb_tty_ports = [port.device for port in ports if "ttyUSB" in port.device]
            if len(usb_tty_ports) >= 1:
                antenna = serial.Serial(usb_tty_ports[0], 115200)
                syslog.syslog("Antenna connected using USB")
                print("Antenna connected using USB")
                return antenna

            antenna = serial.Serial("/dev/serial0", 115200)
            print("Antenna connected using GPIO pins")
            syslog.syslog("Antenna connected using GPIO pins")
            return antenna
        except serial.SerialException:
            print("Antenna is not plugged in")
            syslog.syslog("Antenna is not plugged in")
            sleep(1)


def write(msg, antenna):
    try:
        antenna.write(msg)
        return True
    except serial.SerialException:
        print("Write failed")
        syslog.syslog("Write failed")
        return False
