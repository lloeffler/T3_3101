#!/usr/bin/python3
import sys
import traceback
import datetime

from random import randint
from json import loads
from re import compile
from time import sleep
from os.path import isfile
from os import system, name

import numpy as np

from parking_learner import ParkingLearner
from parkingdirection import Parkingdirection
from print_logo import PrintLogo

from exhibition import Exhibition

from constants import DISPLAY_CONFIRMATION_SLEEP_TIME, NUMBER_OF_SIMULATIONS, SIZE_STATE_RHO, SIZE_STATE_PHI, SIZE_STATE_ORIENTATION, SIZE_ACTION_DIRECTION, SIZE_ACTION_LENTGH


class Simulator(Exhibition):
    """
    A class to simulate the exhibiton parking application.
    """

    def __init__(self, random_start: bool = False):
        """
        Calls __init__ function of parent class and sets additional random start attribute.

        Parameter
        ---------
        random_start: bool
            If the commandline argument random_start is set, the start function will generate random start positions.
        """
        super().__init__()
        self._random_start = random_start
        self._execution_time = None

    def main(self, administrator_mode: bool = False, park_lot_detection: bool = False):
        """
        The main function, which handles inputs.

        Parameter
        ---------
        random_start: bool
            If the commandline argument random_start is set, the start function will generate random start positions.
        """
        self.print_menu(administrator_mode=administrator_mode)
        user_input = input('> ').lower()
        while user_input != 'quit' and user_input != 'exit':
            wrong_input = False
            self._execution_time = None
            if user_input == 'start':
                self._execution_time = self.start(random_start=random_start)
            elif user_input == 'settings' or user_input == 'einstellungen':
                self.settings(administrator_mode=administrator_mode)
            elif user_input == 'english' or user_input == 'englisch':
                self.config['language'] = 'english'
            elif user_input == 'german' or user_input == 'deutsch':
                self.config['language'] = 'german'
            else:
                wrong_input = True
            self.print_menu(
                administrator_mode=administrator_mode, wrong_input=wrong_input)
            user_input = input('> ').lower()
        # Asks user at quitting the application, to save the current configuration.
        print(self.language_package[self.config['language']]['config'])
        user_input = input('> ').lower()
        while user_input != 'yes' and user_input != 'ja' and user_input != 'no' and user_input != 'nein':
            print(
                self.language_package[self.config['language']]['wrong_input'])
            print(self.language_package[self.config['language']]['config'])
            user_input = input('> ').lower()
        if user_input == 'yes' or user_input == 'ja':
            self.save_config()
        # Asks user at quitting the application, to save the current q-table.
        print(self.language_package[self.config['language']]['qtable'])
        user_input = input('> ').lower()
        while user_input != 'yes' and user_input != 'ja' and user_input != 'no' and user_input != 'nein':
            print(
                self.language_package[self.config['language']]['wrong_input'])
            print(self.language_package[self.config['language']]['qtable'])
            user_input = input('> ').lower()
        if user_input == 'yes' or user_input == 'ja':
            self.save_qtable()
        print('Bye')

    def clear(self):
        """
        Clears comand line output
        """
        red = '\033[31m'
        reset = '\033[0m'
        system('cls' if name == 'nt' else 'clear')
        PrintLogo.print_color(
            PrintLogo) if self.config['color'] else PrintLogo.print_bw(PrintLogo)
        print('\n{0}\t\t\t!SIMULATOR!\n{1}'.format(red, reset))

    def print_menu(self, administrator_mode: bool = False, wrong_input: bool = False):
        """
        Prints main menu.
        """
        self.clear()
        print(self.language_package[self.config['language']]['command'])
        print(self.language_package[self.config['language']]['exit'])
        if self._execution_time != None:
            print("Last simulation executed in: {}".format(self._execution_time))

    def start(self, random_start: bool = False):
        """
        Start simulation parking process to learn and fill a q-table.

        Parameter
        ---------
        random_start: bool
            Says if the startposition is random or default, by default false.
            If true, the start position is generated randomly.
            If false, the default start position is used.

        Returns
        -------
        timedelta: The executiontime of the simulation.
        """
        print("Start simulation")
        start_time = datetime.datetime.now()
        # To change the number of runs, change to number in the following line.
        for x in range(NUMBER_OF_SIMULATIONS):
            if random_start:
                start_distance = randint(0, SIZE_STATE_RHO - 1)
                start_angle = randint(0, SIZE_STATE_PHI - 1)
                start_orientation = randint(0, SIZE_STATE_ORIENTATION - 1)
            else:
                start_distance = 15
                start_angle = 0
                start_orientation = 18
            single_start_execution_time = datetime.datetime.now()
            print("Running simulation number {}".format(x + 1))
            self._parking_learner.simulated_start(
                distance=start_distance, angle=start_angle, orientation=start_orientation)
            single_end_execution_time = datetime.datetime.now()
            print("Finished simulation number {} in {}".format(
                x + 1, single_end_execution_time - single_start_execution_time))
        end_time = datetime.datetime.now()
        print("Finished similation in {}".format(end_time - start_time))
        sleep(DISPLAY_CONFIRMATION_SLEEP_TIME)
        return end_time - start_time


if __name__ == '__main__':
    try:
        # Checks for random_start in comandline arguments.
        random_start = True if 'random_start' in sys.argv[
            1:] or 'random' in sys.argv[1:] else False
        # Generates simulator instance.
        runner = Simulator(random_start=random_start)
        # Executes simulation.
        runner.main(administrator_mode=True)
    except Exception as exception:
        try:
            # If any error is catched, it is tried to write into an error log file.
            log_file = open("error.log", "a")
            log_file.write("[Simulator|{0}] {1}\nTraceback:\n{2}".format(
                datetime.datetime.now().isoformat(), str(exception), traceback.format_exc()))
            log_file.close()
        except Exception as inner_exception:
            # If the logging into a file failes, the error is printed to the command line.
            print('Outer Exception:')
            traceback.print_exception()
            print('Inner Exception')
            traceback.print_exception()

# Original Author: Lukas Loeffler
