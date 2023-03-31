#!/usr/bin/python3
from time import sleep

from swarmrobot import SwarmRobot
from turn_assistant import TurnAssistant

from constances import TURN_SLEEP_TIME


def right1(bot: SwarmRobot):
    """
    Steers to 25% to the right.

    Parameter
    ----------
    bot: SwarmRobot
        A instance of the robot.
    """
    bot.set_drive_steer(0.25)
    sleep(TURN_SLEEP_TIME)


def right2(bot: SwarmRobot):
    """
    Steers to 50% to the right.

    Parameter
    ----------
    bot: SwarmRobot
        A instance of the robot.
    """
    bot.set_drive_steer(0.5)
    sleep(TURN_SLEEP_TIME)


def right3(bot: SwarmRobot):
    """
    Steers to 75% to the right.

    Parameter
    ----------
    bot: SwarmRobot
        A instance of the robot.
    """
    bot.set_drive_steer(0.75)
    sleep(TURN_SLEEP_TIME)


def right4(bot: SwarmRobot):
    """
    Steers to 100% to the right.

    Parameter
    ----------
    bot: SwarmRobot
        A instance of the robot.
    """
    bot.set_drive_steer(1)
    sleep(TURN_SLEEP_TIME)


def right90(turn_assistant: TurnAssistant):
    """
    Turns the robot about 90 degree to the right.

    Parameter
    ----------
    turn_assistant: TurnAssistant
        A instance of the turn assistand.
    """
    turn_assistant.turn_90_deg(direction=-1)


def left1(bot: SwarmRobot):
    """
    Steers to 25% to the left.

    Parameter
    ----------
    bot: SwarmRobot
        A instance of the robot.
    """
    bot.set_drive_steer(-0.25)
    sleep(TURN_SLEEP_TIME)


def left2(bot: SwarmRobot):
    """
    Steers to 50% to the left.

    Parameter
    ----------
    bot: SwarmRobot
        A instance of the robot.
    """
    bot.set_drive_steer(-0.5)
    sleep(TURN_SLEEP_TIME)


def left3(bot: SwarmRobot):
    """
    Steers to 75% to the left.

    Parameter
    ----------
    bot: SwarmRobot
        A instance of the robot.
    """
    bot.set_drive_steer(-0.75)
    sleep(TURN_SLEEP_TIME)


def left4(bot: SwarmRobot):
    """
    Steers to 100% to the left.

    Parameter
    ----------
    bot: SwarmRobot
        A instance of the robot.
    """
    bot.set_drive_steer(-1)
    sleep(TURN_SLEEP_TIME)


def left90(turn_assistant: TurnAssistant):
    """
    Turns the robot about 90 degree to the left.

    Parameter
    ----------
    turn_assistant: TurnAssistant
        A instance of the turn assistand.
    """
    turn_assistant.turn_90_deg(direction=1)


def straight(bot: SwarmRobot):
    """
    Steers straight.

    Parameter
    ----------
    bot: SwarmRobot
        A instance of the robot.
    """
    bot.straight()


def turn180(turn_assistant: TurnAssistant):
    """
    Turns the robot about 180 degree.

    Parameter
    ----------
    turn_assistant: TurnAssistant
        A instance of the turn assistand.
    """
    turn_assistant.turn_180_deg()


def turn180onspot(turn_assistant: TurnAssistant):
    """
    Turns the robot about 180 degree.

    Parameter
    ----------
    turn_assistant: TurnAssistant
        A instance of the turn assistand.
    """
    turn_assistant.turn_180_deg_on_spot()


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
    sleep(TURN_SLEEP_TIME)


def rotate(bot: SwarmRobot):
    """
    Ask the user how many degree the motor should rotate.
    510 degree equals one rotation of the tier.
    Uses the self._bot._drive_motor.rotate_motor function to drive.
    """
    print("enter how many degree the drive motor should rotate,\n510 degree equals one rotation of the tier:")
    degree = int(input(">"))
    bot._drive_motor.rotate_motor(degree=degree)
    sleep(TURN_SLEEP_TIME)


def autorotate(bot: SwarmRobot):
    """
    Ask the user how many degree the motor should rotate.
    510 degree equals one rotation of the tier.
    Uses the self._bot._drive_motor.rotate_motor function to drive.
    """
    print("enter how many degree the drive motor should rotate,\n510 degree equals one rotation of the tier:")
    degree = int(input(">"))
    (degree_steps, degree_rest) = divmod(degree, 30)
    bot.drive(length=degree_steps)
    bot._drive_motor.rotate_motor(degree=degree_rest)


def drive1(bot: SwarmRobot):
    """
    Lets the robot drive 1 cm.

    Parameter
    ----------
    bot: SwarmRobot
        A instance of the robot.
    """
    bot.drive(1)


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
    straight(bot)
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
    print("turn180 -> turns robot about 180 degree")
    print("turn180onspot -> turns robot about 180 degree and corrects to turning maneuver start position")
    print("drive -> enter time to drive in seconds to drive")
    print("rotate -> enter degree to rotate the drive motor to drive")
    print("autorotate -> enter degree to rotate the drive motor to drive in multiple steps")
    print("drive1 -> robot drive 1 cm forward")
    print("set_speed -> enter new driving speed")
    print("reset -> resets speed and steering")
    print("end -> quits programm")
    print("help -> prints this help")


bot = SwarmRobot()

speed = 20

bot.calibrate(False, True)

bot.set_drive_steer(0)

turn_assistant = TurnAssistant(bot=bot)

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
    if user_input == "lright90":
        right90(turn_assistant=turn_assistant)
    if user_input == "left1":
        left1(bot=bot)
    if user_input == "left2":
        left2(bot=bot)
    if user_input == "left3":
        left3(bot=bot)
    if user_input == "left4":
        left4(bot=bot)
    if user_input == "left90":
        left90(turn_assistant=turn_assistant)
    if user_input == "straight":
        straight(bot=bot)
    if user_input == "turn180":
        turn180(turn_assistant=turn_assistant)
    if user_input == "turn180onspot":
        turn180onspot(turn_assistant=turn_assistant)
    if user_input == "drive":
        drive(bot=bot, dspeed=speed)
    if user_input == "rotate":
        rotate(bot=bot)
    if user_input == "autorotate":
        autorotate(bot=bot)
    if user_input == "drive1":
        drive1(bot=bot)
    if user_input == "reset":
        speed = reset(bot=bot)
    if user_input == "set_speed":
        speed = set_speed(speed=speed)
    if user_input == "help":
        help()
    user_input = input("enter something\n>")
