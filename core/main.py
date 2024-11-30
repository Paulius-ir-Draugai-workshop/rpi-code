from time import sleep

import format
import pygame

# Initialize pygame
pygame.init()

# Arrays to store inputs
throttle_inputs = []
joystick_inputs = []

# Main loop
clock = pygame.time.Clock()
running = True

# Initialize throttle and joystick
throttle = None
joystick = None

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


# Connect controls initially
connect_controls()

# Main event loop
while running:
    time_delta = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Check if both controls are still connected
    if pygame.joystick.get_count() < 2 or throttle is None or joystick is None:
        print("Lost connection to one or both controls. Waiting to reconnect...")
        connect_controls()
        continue

    # Update throttle values and store in the list
    values = {}
    if throttle is not None:
        if throttle.get_numaxes() >= 8:
            values["throttle"] = throttle.get_axis(2)
            values["yaw"] = throttle.get_axis(5)

    # Update joystick values and store in the list
    hat = (0, 0)
    shoot_torpedo = 0
    if joystick is not None:
        if joystick.get_numaxes() >= 4:
            values["roll"] = joystick.get_axis(0)
            values["pitch"] = joystick.get_axis(1)
        if joystick.get_numhats() >= 1:
            hat = joystick.get_hat(0)

        shoot_torpedo = joystick.get_button(0)

    # Print inputs to console periodically (e.g., every 60 frames)
    if len(throttle_inputs) % 60 == 0:
        # print(" ".join([f"{k}: {v}" for k, v in values.items()]))
        f_axes = format.format_axes(values)
        f_hat = format.format_hat(hat)
        print(f_axes, "hat:", f_hat, "torpedo:", shoot_torpedo, sep=" ")
        print(format.checksum(f_axes, f_hat))
        print("Msg: ", format.format_msg1(f_axes, f_hat))
        # print("Throttle Inputs:", throttle_inputs[-1])
        # print("Joystick Inputs:", joystick_inputs[-1])

# Quit pygame
pygame.quit()
