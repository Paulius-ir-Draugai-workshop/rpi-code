from time import sleep

import dll
import format
import pygame
import read
import serial

ser = serial.Serial("/dev/ttyUSB0", 115200)

# Initialize pygame
pygame.init()

# Arrays to store inputs
throttle_inputs = []
joystick_inputs = []

# Main loop
clock = pygame.time.Clock()
running = True

# Initialize throttle and joystick

THROTTLE_NAME = ["TWCS Throttle", "Thrustmaster TWCS Throttle"]
JOYSTICK_NAME = ["T.16000M", "Thrustmaster T.16000M"]


# Function to check and connect joystick and throttle
def connect_controls():
    global throttle, joystick
    throttle = None
    joystick = None
    while throttle is None or joystick is None:
        pygame.joystick.quit()
        pygame.joystick.init()
        if pygame.joystick.get_count() >= 2:
            if (
                pygame.joystick.Joystick(0).get_name() in THROTTLE_NAME
                and pygame.joystick.Joystick(1).get_name() in JOYSTICK_NAME
            ):
                throttle = pygame.joystick.Joystick(0)
                joystick = pygame.joystick.Joystick(1)
            elif (
                pygame.joystick.Joystick(1).get_name() in THROTTLE_NAME
                and pygame.joystick.Joystick(0).get_name() in JOYSTICK_NAME
            ):
                throttle = pygame.joystick.Joystick(1)
                joystick = pygame.joystick.Joystick(0)
            else:
                print("Joysticks not supported.")
                exit(1)
        sleep(0.05)
    print("Throttle and Joystick connected!")


# Main event loop

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

    # Print inputs to console periodically (e.g., every 60 frames)
    if len(throttle_inputs) % 60 == 0:
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
