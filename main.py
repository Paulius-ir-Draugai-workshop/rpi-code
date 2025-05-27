import syslog

import pygame

from core import controller, dll, format, transmit


def main():
    # Initialize pygame
    pygame.init()

    syslog.syslog("Started rpi")
    # Main loop
    clock = pygame.time.Clock()
    running = True

    joystick = None

    # connect antenna
    antenna = transmit.connect_antenna()

    while running:
        clock.tick(5)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.JOYDEVICEREMOVED:
                msg = "joystick removed"
                print(msg)
                syslog.syslog(msg)
                joystick = None

        # checking connection, try to reconnect if disconnected
        if joystick is None or joystick.disconnected():
            joystick = controller.find_controller()
            if joystick is None:
                continue
            else:
                msg = f"joystick connected {joystick.get_name()}"
                print(msg)
                syslog.syslog(msg)

        # if read.check_connection(throttle=throttle, joystick=joystick):
        #     print("Controls disconnected")
        #     syslog.syslog("Controls disconnected")
        #     joystick, throttle = read.connect()

        # read values, if no values are read, try to reconnect
        values = joystick.read_inputs()
        print(values)
        # values = read.read(throttle=throttle, joystick=joystick)
        # if not values:
        #     continue

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


if __name__ == "__main__":
    main()
