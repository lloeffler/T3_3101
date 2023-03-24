import threading
from time import sleep

from motor import Motor


class TurnAssistant:
    def __init__(self, bot):
        self._bot = bot

        self._full_rotation_deg = 510

    # direction 1 = links -1 = rechts
    def turn_90_deg(self, direction):
        sleep(0.5)
        self._bot.set_drive_steer(-1.0*direction)
        sleep(0.5)
        # self._bot._drive_motor.rotate_motor(1.2*self._full_rotation_deg)
        self._bot.drive(20)
        sleep(0.5)
        self._bot.set_drive_steer(1.0*direction)
        sleep(0.5)
        # self._bot._drive_motor.rotate_motor(-1*self._full_rotation_deg)
        self._bot.drive(-17)
        sleep(0.5)
        self._bot.set_drive_steer(-0.3*direction)
        sleep(0.5)
        # self._bot._drive_motor.rotate_motor(1.2*self._full_rotation_deg)
        self._bot.drive(20)
        sleep(0.5)
        self._bot.set_drive_steer(0)
        sleep(0.5)

    def turn_180_deg(self):
        self._bot.set_drive_steer(1.0)
        # self._bot._drive_motor.rotate_motor(-1.3*self._full_rotation_deg)
        self._bot.drive(-22)
        sleep(0.5)
        self._bot.set_drive_steer(-1.0)
        # self._bot._drive_motor.rotate_motor(1.3*self._full_rotation_deg)
        self._bot.drive(22)
        sleep(0.5)
        self._bot.set_drive_steer(1.0)
        # self._bot._drive_motor.rotate_motor(-1.3*self._full_rotation_deg)
        self._bot.drive(-22)
        sleep(0.5)
        self._bot.set_drive_steer(-1.0)
        # self._bot._drive_motor.rotate_motor(1.4*self._full_rotation_deg)
        self._bot.drive(24)
        sleep(0.5)
        self._bot.set_drive_steer(0)
        sleep(0.5)

    def turn_180_deg_on_spot(self):
        self._bot.set_drive_steer(1.0)
        sleep(0.5)
        # self._bot._drive_motor.rotate_motor(-0.6*self._full_rotation_deg)
        self._bot.drive(-10)
        sleep(0.5)
        self._bot.set_drive_steer(-1.0)
        sleep(0.5)
        # self._bot._drive_motor.rotate_motor(0.7*self._full_rotation_deg)
        self._bot.drive(12)
        sleep(0.5)
        self._bot.set_drive_steer(1.0)
        sleep(0.5)
        # self._bot._drive_motor.rotate_motor(-0.6*self._full_rotation_deg)
        self._bot.drive(-10)
        sleep(0.5)
        self._bot.set_drive_steer(-1.0)
        sleep(0.5)
        # self._bot._drive_motor.rotate_motor(0.8*self._full_rotation_deg)
        self._bot.drive(13)
        sleep(0.5)
        self._bot.set_drive_steer(1.0)
        sleep(0.5)
        # self._bot._drive_motor.rotate_motor(-0.6*self._full_rotation_deg)
        self._bot.drive(-10)
        sleep(0.5)
        self._bot.set_drive_steer(-1.0)
        sleep(0.5)
        # self._bot._drive_motor.rotate_motor(0.8*self._full_rotation_deg)
        self._bot.drive(13)
        sleep(0.5)
        self._bot.set_drive_steer(1.0)
        sleep(0.5)
        # self._bot._drive_motor.rotate_motor(-0.6*self._full_rotation_deg)
        self._bot.drive(-10)
        self._bot.set_drive_steer(0)
        sleep(0.5)

    def park_backwards(self):
        self.turn_180_deg_on_spot()
        sleep(0.5)
        self._bot.set_drive_steer(0)
        sleep(0.5)
        # self._bot._drive_motor.rotate_motor(-1.0*self._full_rotation_deg)
        self._bot.drive(-17)

    def turn_0_deg(self):
        sleep(0.5)
        self._bot.set_drive_steer(0)
        sleep(0.5)
        # self._bot._drive_motor.rotate_motor(1.1*self._full_rotation_deg)
        self._bot.drive(19)
