#!/usr/bin/python3
from time import sleep

from swarmrobot import SwarmRobot


def right1(bot: SwarmRobot):
    """
    Steers to 25% to the right.

    Parameter
    ----------
    bot: SwarmRobot
        A instance of the robot.
    """
    bot.set_drive_steer(0.25)
    sleep(0.5)


def right2(bot: SwarmRobot):
    """
    Steers to 50% to the right.

    Parameter
    ----------
    bot: SwarmRobot
        A instance of the robot.
    """
    bot.set_drive_steer(0.5)
    sleep(0.5)


def right3(bot: SwarmRobot):
    """
    Steers to 75% to the right.

    Parameter
    ----------
    bot: SwarmRobot
        A instance of the robot.
    """
    bot.set_drive_steer(0.75)
    sleep(0.5)


def right4(bot: SwarmRobot):
    """
    Steers to 100% to the right.

    Parameter
    ----------
    bot: SwarmRobot
        A instance of the robot.
    """
    bot.set_drive_steer(1)
    sleep(0.5)


def left1(bot: SwarmRobot):
    """
    Steers to 25% to the left.

    Parameter
    ----------
    bot: SwarmRobot
        A instance of the robot.
    """
    bot.set_drive_steer(-0.25)
    sleep(0.5)


def left2(bot: SwarmRobot):
    """
    Steers to 50% to the left.

    Parameter
    ----------
    bot: SwarmRobot
        A instance of the robot.
    """
    bot.set_drive_steer(-0.5)
    sleep(0.5)


def left3(bot: SwarmRobot):
    """
    Steers to 75% to the left.

    Parameter
    ----------
    bot: SwarmRobot
        A instance of the robot.
    """
    bot.set_drive_steer(-0.75)
    sleep(0.5)


def left4(bot: SwarmRobot):
    """
    Steers to 100% to the left.

    Parameter
    ----------
    bot: SwarmRobot
        A instance of the robot.
    """
    bot.set_drive_steer(-1)
    sleep(0.5)


def straight(bot: SwarmRobot):
    """
    Steers straight.

    Parameter
    ----------
    bot: SwarmRobot
        A instance of the robot.
    """
    bot.set_drive_steer(-0.25)
    sleep(0.5)
    bot.set_drive_steer(0.25)
    sleep(0.5)
    bot.set_drive_steer(0.)
    sleep(0.5)


def drive(bot: SwarmRobot, dspeed: int):
    """
    Ask the user how long/many seconds the robot should drive with the current speed.

    Parameter
    ----------
    bot: SwarmRobot
        A instance of the robot.
    dspeed: int
        The current (drive) speed.
        The robot drives forward if dspeed is greate than 0.
        The robot drives backward if dspeed is less than 0.
    """
    print("enter how long to drive with power:")
    print(dspeed)
    sec = input(">")
    bot.set_drive_power(dspeed)
    sleep(int(sec))
    bot.set_drive_power(0)
    sleep(0.5)


def reset(bot: SwarmRobot) -> int:
    """
    Stops the robot.
    Resets the steering of the robot.

    Parameter
    ----------
    bot: SwarmRobot
        A instance of the robot.

    Returns
    -------
    int:
        The default speed of 20.
    """
    bot.stop_all()
    sleep(0.5)
    bot.set_drive_steer(-0.25)
    sleep(0.5)
    bot.set_drive_steer(0.25)
    sleep(0.5)
    bot.set_drive_steer(0)
    sleep(0.5)
    return 20


def set_speed(speed: int = 20):
    """
    Asks the user for the speed to be set.
    The entered speed has to be between -100 and +100 and not 0.

    Returns
    -------
    int:
        The default speed of 20.
    """
    new_speed = int(
        input("enter speed between -100 and +100\n20 equals about 5-6 cm per second\n>"))
    return new_speed if new_speed >= -100 and new_speed <= 100 else speed


def help():
    """
    Prints commands aka help.
    """
    print("commands:\n")
    print("left1 -> left steer 0.25\tright1 -> right steer 0.25")
    print("left2 -> left steer 0.5\tright2 -> right steer 0.5")
    print("left3 -> left steer 0.75\tright3 -> right steer 0.75")
    print("left4 -> left steer 1\tright4 -> right steer 1")
    print("straight -> steer straight")
    print("drive -> enter time to drive in seconds to drive")
    print("set_speed -> enter new driving speed")
    print("reset -> resets speed and steering")
    print("end -> quits programm")
    print("help -> prints this help")


bot = SwarmRobot()

speed = 20

bot.calibrate(False, True)

bot.set_drive_steer(0)

help()

user_input = input("enter something\n>")

# Behavior based on user input.
while user_input != "end" and user_input != "exit" and user_input != "quit":
    print(user_input)
    if user_input == "right1":
        right1(bot=bot)
    if user_input == "right2":
        right2(bot=bot)
    if user_input == "right3":
        right3(bot=bot)
    if user_input == "right4":
        right4(bot=bot)
    if user_input == "left1":
        left1(bot=bot)
    if user_input == "left2":
        left2(bot=bot)
    if user_input == "left3":
        left3(bot=bot)
    if user_input == "left4":
        left4(bot=bot)
    if user_input == "drive":
        drive(bot=bot, dspeed=speed)
    if user_input == "reset":
        speed = reset(bot=bot)
    if user_input == "set_speed":
        speed = set_speed(speed=speed)
    if user_input == "help":
        help()
    if user_input == "straight":
        straight(bot=bot)
    user_input = input("enter something\n>")
