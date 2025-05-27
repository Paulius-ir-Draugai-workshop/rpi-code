import pygame


class Controller:
    def read_inputs(self):
        raise NotImplementedError()

    def disconnected(self):
        raise NotImplementedError()

    def get_name(self):
        raise NotImplementedError()


class ThrustmasterT16000M(Controller):
    THROTTLE_NAME = ["TWCS Throttle", "Thrustmaster TWCS Throttle"]
    JOYSTICK_NAME = ["T.16000M", "Thrustmaster T.16000M"]
    THROTTLE_ID = 2
    YAW_ID = 5
    ROLL_ID = 0
    PITCH_ID = 1

    def __init__(self, joystick, throttle):
        self.joystick = joystick
        self.throttle = throttle

    def read_inputs(self):
        values = {}
        values["throttle"] = self.throttle.get_axis(self.THROTTLE_ID)
        values["yaw"] = self.throttle.get_axis(self.YAW_ID)
        values["roll"] = self.joystick.get_axis(self.ROLL_ID)
        values["pitch"] = self.joystick.get_axis(self.PITCH_ID)
        values["hat"] = self.joystick.get_hat(0)

        return values

    def get_name(self):
        raise "Thrustmaster T.16000M"


class ThrustmasterTFlightHotas(Controller):
    NAME = ["Thrustmaster T.Flight Hotas", "T.Flight Hotas"]
    THROTTLE_ID = 5
    YAW_ID = 4
    ROLL_ID = 0
    PITCH_ID = 1

    def __init__(self, joystick):
        self.joystick = joystick

    def read_inputs(self):
        values = {}

        values["throttle"] = self.joystick.get_axis(self.THROTTLE_ID)
        values["yaw"] = self.joystick.get_axis(self.YAW_ID)
        values["roll"] = self.joystick.get_axis(self.ROLL_ID)
        values["pitch"] = self.joystick.get_axis(self.PITCH_ID)
        values["hat"] = self.joystick.get_hat(0)

        return values

    def get_name(self):
        return "Thrustmaster T.Flight Hotas"

    def disconnected(self):
        return self.joystick is None


def find_controller():
    pygame.joystick.quit()
    pygame.joystick.init()
    if pygame.joystick.get_count() >= 2:
        if (
            pygame.joystick.Joystick(0).get_name() in ThrustmasterT16000M.THROTTLE_NAME
            and pygame.joystick.Joystick(1).get_name() in ThrustmasterT16000M.JOYSTICK_NAME
        ):
            throttle = pygame.joystick.Joystick(0)
            joystick = pygame.joystick.Joystick(1)
            return ThrustmasterT16000M(joystick, throttle)
        elif (
            pygame.joystick.Joystick(1).get_name() in ThrustmasterT16000M.THROTTLE_NAME
            and pygame.joystick.Joystick(0).get_name() in ThrustmasterT16000M.JOYSTICK_NAME
        ):
            throttle = pygame.joystick.Joystick(1)
            joystick = pygame.joystick.Joystick(0)
            return ThrustmasterT16000M(joystick, throttle)
    elif pygame.joystick.get_count() == 1:
        joystick = pygame.joystick.Joystick(0)
        if joystick.get_name() in ThrustmasterTFlightHotas.NAME:
            return ThrustmasterTFlightHotas(joystick)

    return None
