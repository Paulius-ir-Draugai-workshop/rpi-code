import syslog

import dll
import format
import pygame
import read
import transmit

# Initialize pygame
pygame.init()

syslog.syslog("Started rpi")
# Main loop
clock = pygame.time.Clock()
running = True

throttle = None
joystick = None

# connect antenna
antenna = transmit.connect_antenna()

while running:
    clock.tick(5)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # checking connection, try to reconnect if disconnected
    if read.check_connection(throttle=throttle, joystick=joystick):
        print("Controls disconnected")
        syslog.syslog("Controls disconnected")
        joystick, throttle = read.connect()

    # read values, if no values are read, try to reconnect
    values = read.read(throttle=throttle, joystick=joystick)
    if not values:
        continue

    # formatting message to bytearray
    msg = format.format_msg1(values)

    # draw gui
    # gui.parse_and_update_interface(msg)

    # run message through dll
    dll_obj = dll.Dll()
    msg_u = dll_obj.dllPack(msg)

    if not transmit.write(msg_u, antenna):
        antenna = transmit.connect_antenna()
    print("Dll: ", [int(b) for b in msg_u])
    syslog.syslog(f"Dll: {[int(b) for b in msg_u]}")

# Quit pygame
pygame.quit()
