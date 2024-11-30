from time import sleep

import dll
import format
import pygame
import read
import serial

ser = serial.Serial("/dev/ttyUSB0", 115200)

# Initialize pygame
pygame.init()

# Main loop
clock = pygame.time.Clock()
running = True

throttle = None
joystick = None

while running:
    time_delta = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if read.check_connection(throttle=throttle, joystick=joystick):
        joystick, throttle = read.connect()

    values = read.read(throttle=throttle, joystick=joystick)
    if not values:
        continue

    f_axes = format.format_axes(values)
    f_hat = format.format_hat(values["hat"])
    print(f_axes, "hat:", f_hat, sep=" ")
    print(format.checksum(f_axes, f_hat))
    msg = format.format_msg1(f_axes, f_hat)
    print("Msg: ", msg)
    dll_obj = dll.Dll()
    msg_u = dll_obj.dllPack(msg)
    ser.write(msg_u)
    msg_u = [int(b) for b in msg_u]
    print("Dll: ", msg_u)

# Quit pygame
pygame.quit()
