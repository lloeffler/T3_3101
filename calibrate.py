#!/usr/bin/python3
import threading

from time import sleep

from swarmrobot import SwarmRobot

def calibrate_function():
    """
    Executes Swarmrobot calibration, including forklift calibration.
    """
    bot = SwarmRobot()

    bot.calibrate(True, True)
    print('Calibration finished')
    sleep(1)

def output_function():
    """
    Prints output to with instruction for the user.
    """
    red = '\033[31m'
    reset = '\033[0m'
    sleep(2)
    print('\n\n{0}Please unplug the calbe of the fork tilt motor.{1}\n\n'.format(red, reset))
    sleep(2)
    print('\n\n{0}Please plug in the calbe of the fork tilt motor.{1}\n\n'.format(red, reset))

if __name__ == "__main__":
    user_input = input('Press [ENTER] to start calibration...')

    calbiration = threading.Thread(target=calibrate_function, args=())
    user_output = threading.Thread(target=output_function, args=())
    
    calbiration.start()
    user_output.start()
    
    calbiration.join()
    user_output.join()