import syslog
from time import sleep

import pygame

THROTTLE_NAME = ["TWCS Throttle", "Thrustmaster TWCS Throttle"]
JOYSTICK_NAME = ["T.16000M", "Thrustmaster T.16000M"]

THROTTLE_ID = 2
YAW_ID = 5
ROLL_ID = 0
PITCH_ID = 1


def check_connection(joystick, throttle):
    return pygame.joystick.get_count() < 2 or throttle is None or joystick is None


def connect():
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
                syslog.syslog("Joysticks not supported.")
                return (None, None)
        sleep(0.05)
    print("Throttle and Joystick connected!")
    syslog.syslog("Throttle and Joystick connected!")
    return (joystick, throttle)


def read(joystick, throttle):
    values = {}
    if throttle is not None:
        values["throttle"] = throttle.get_axis(THROTTLE_ID)
        values["yaw"] = throttle.get_axis(YAW_ID)
    else:
        return None

    if joystick is not None:
        values["roll"] = joystick.get_axis(ROLL_ID)
        values["pitch"] = joystick.get_axis(PITCH_ID)
        values["hat"] = joystick.get_hat(0)
    else:
        return None

    return values
