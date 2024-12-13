import serial
from serial.tools import list_ports

from core import gui

try:
    ports = list_ports.comports()
    usb_tty_ports = [port.device for port in ports if "ttyUSB" in port.device]
    if len(usb_tty_ports) >= 1:
        antenna = serial.Serial(usb_tty_ports[0], 115200)
        print("Antenna connected using USB")
except serial.SerialException:
    print("Antenna is not plugged in")
    exit(1)


while True:
    b = antenna.readline()
    print(b)
    gui.parse_and_update_interface(b[:-1])
