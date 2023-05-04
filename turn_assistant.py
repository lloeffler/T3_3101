import threading

from time import sleep

from motor import Motor
from swarmrobot import SwarmRobot

from constants import TURN_SLEEP_TIME


class TurnAssistant:
    """
    Class to execute turning moneuver with a smaler radius then just a full lock of the steering allows.
    """

    def __init__(self, bot: SwarmRobot):
        self._bot = bot

    def turn_90_deg(self, direction):
        """
        Turns the robot about 90 degrees.

        Parameter
        ---------
        direction: int or float
            Positiv one (1) turns the robot to the left.
            Negative one (-1) turns the robot to the right.
        """
        self._bot.set_drive_steer(-1.0*direction)
        sleep(TURN_SLEEP_TIME)
        self._bot.drive(15)
        self._bot.set_drive_steer(1.0*direction)
        sleep(TURN_SLEEP_TIME)
        self._bot.drive(-16)
        self._bot.set_drive_steer(-1.0*direction)
        sleep(TURN_SLEEP_TIME)
        self._bot.drive(16)
        self._bot.straight()

    def turn_180_deg(self):
        """
        Turns the robot about 180 degrees.
        """
        self._bot.set_drive_steer(1.0)
        sleep(TURN_SLEEP_TIME)
        self._bot.drive(-23)
        self._bot.set_drive_steer(-1.0)
        sleep(TURN_SLEEP_TIME)
        self._bot.drive(23)
        self._bot.set_drive_steer(1.0)
        sleep(TURN_SLEEP_TIME)
        self._bot.drive(-23)
        self._bot.set_drive_steer(-1.0)
        sleep(TURN_SLEEP_TIME)
        self._bot.drive(23)
        self._bot.straight()

    def turn_180_deg_on_spot(self):
        """
        Turns the robot about 180 degrees and corrects position to tunrning maneuver start position.
        """
        self.turn_180_deg()
        self._bot.drive(-10)

    def park_backwards(self):
        """
        Turns the robot about 180 degrees and corrects position to tunrning maneuver start position.
        Drives backward into the parking lot.
        """
        self.turn_180_deg_on_spot()
        self._bot.straight()
        self._bot.drive(-17)

    def turn_0_deg(self):
        self._bot.straight()
        self._bot.drive(19)
