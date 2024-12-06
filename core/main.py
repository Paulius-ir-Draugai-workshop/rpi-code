import dll
import format
import pygame
import read
import serial

import gui

ser = serial.Serial("/dev/ttyUSB0", 115200)

# Initialize pygame
pygame.init()

# Main loop
clock = pygame.time.Clock()
running = True

throttle = None
joystick = None

sent = False

while running:
    clock.tick(10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # checking connection, try to reconnect if disconnected
    if read.check_connection(throttle=throttle, joystick=joystick):
        print("Controls disconnected")
        joystick, throttle = read.connect()

    # read values, if no values are read, try to reconnect
    values = read.read(throttle=throttle, joystick=joystick)
    if not values:
        continue

    # formatting message to bytearray
    msg = format.format_msg1(values)

    # draw gui
    gui.parse_and_update_interface(msg)

    # run message through dll
    dll_obj = dll.Dll()
    msg_u = dll_obj.dllPack(msg)

    # send data serial
    ser.write(msg_u)

    print("Dll: ", [int(b) for b in msg_u])

# Quit pygame
pygame.quit()
