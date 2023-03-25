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


class Simulator:
    """
    A clas to simulate the exhibiton parking application.
    """

    language_package = {
        'english': {
            'command': 'Enter "start" to start the parking.\nEnter "settings" to open the settings menu.\nEnter "german" to change the language. Geben Sie "deutsch" ein um die Sprache zu aendern.',
            'back': 'Enter "back" to go to the previous menu.',
            'exit': 'Enter "exit" or quit to leave to application.',
            'config': 'Enter "yes" to save the current configuration.\nEnter "no" to leave the application without saving the current configuration.',
            'qtable': 'Enter "yes" to save the current qtable.\nEnter "no" to leave the application without saving the current qtable.',
            'wrong_input': 'Error: Wrong input, please enter one of the mentioned options.',
            'settings': {
                'heading': 'Settings',
                'commands': {
                    'direction': 'Enter "direction" to change the parking direciton.',
                    'qtable': 'Enter "q", "table" or "q-table" to open the q-table settings.',
                    'action': 'Enter "action" to change the parking-learner action.'
                },
                'direction': {
                    'heading': 'Parking direction',
                    'current': 'The current parking direction is ',
                    18: 'forward',
                    0: 'backward',
                    'command': 'To change the parking direction enter either "forward" or "backward".'
                },
                'qtable': {
                    'heading': 'Q-Table settings',
                    'commmand': 'Enter "load" to load a new q-table.\nEnter "save" to save the current q-table.',
                    'load': {
                        'heading': 'Load a new q-table',
                        'command': 'Enter the name of q-table to load.\nIf the entered q-table does not exists, a empty q-table is loaded.\nEnter "abort" the abort.',
                        'save': 'Do you want to save the current q-table?\nEnter "yes" to save.\nEnter "no" to continue without saving.',
                        'not_found': 'No q-table named like this was found, creat a one.'
                    },
                    'save': {
                        'heading': 'Save the current q-table',
                        'current': 'The current q-table is named ',
                        'command': 'Are you sure, you want to save the current q-table and override the saved one?\nEnter "yes" to confirm.\nEnter "no" the abort.'
                    }
                },
                'action': {
                    'heading': 'Parking-Learner action',
                    'command': 'Enter "explore" to change the parking-learner action and let the robot learn how to park.\nEnter "utilize" to change the parking-learner action and utilize the q-table.',
                    'explore': 'Enter how many tries the robot can learn ho to park. If greater or eqals 250.000, the robot will not change to utilize automaticly.\nNo input, decimals or negative numbers resets number of tries.',
                    'confirmation': 'is set now as parking-learner action.'
                }
            }
        },
        'german': {
            'command': 'Geben Sie "start" ein, um den Einparkvorgang zu starten.\nGeben Sie "Einstellungen" ein, um das Einstellungsmenue zu oeffnen.\nGeben Sie "englisch" ein um die Sprache zu aendern. Enter "english" to change the language.',
            'back': 'Geben Sie "zurueck" ein, um zum vorherigen Menue zu gelangen.',
            'exit': 'Geben Sie "exit" oder "quit" ein um die Anwendung zu verlassen.',
            'config': 'Geben Sie "ja" ein, um die aktuelle Konfiguration zu speichern.\nGeben sie "nein" ein, um die Anwendung ohne Speichern der Konfiguration zu verlassen.',
            'qtable': 'Geben Sie "ja" ein, um die aktuelle Q-Tabelle zu speichern.\nGeben sie "nein" ein, um die Anwendung ohne Speichern der Q-Tabelle zu verlassen.',
            'wrong_input': 'Fehler: Falsche Eingabe, bitte geben Sie eine der genannten Auswahlmoeglichkeiten ein.',
            'settings': {
                'heading': 'Einstellungen',
                'commands': {
                    'direction': 'Geben Sie "Richtung" ein, um die Einparkrichtung zu aendern.',
                    'qtable': 'Geben Sie "q", "Tabelle" or "Q-Tabelle" ein, um die Einstellungen der Q-Tabelle zu oeffnen.',
                    'action': 'Geben Sie "Action" ein, um die Action des Parklerners zu aendern.'
                },
                'direction': {
                    'heading': 'Einparkrichtung',
                    'current': 'Die aktuelle Einparkrichtung ist ',
                    18: 'vorwaerts',
                    0: 'rueckwaerts',
                    'command': 'Um die Einparkrichtung zu aendern, entweder "vorwaerts" oder "rueckwaerts" eingeben.'
                },
                'qtable': {
                    'heading': 'Q-Tabellen Einstellungen',
                    'commmand': 'Geben Sie "laden" ein, um eine Q-Tabelle zu laden.\nGeben Sie "speichern" ein, um die aktuelle Q-Tabelle zu speichern.',
                    'load': {
                        'heading': 'Neue Q-Tabelle laden',
                        'command': 'Geben Sie den Namen der Q-Tabelle ein, um diese zu laden.\nWenn die eingegebene Q-Tabelle nicht existiert, wird eine neue angelegt.\nGeben Sie "abbrechen" zum Abbrechen ein.',
                        'save': 'Moechten Sie die aktuelle Q-Tabelle speichern?\nGeben Sie "ja" ein, um zu speichern.\nGeben Sie "nein" ein, um ohne zu speichern fortzufahren.',
                        'not_found': 'Es wurde keine Q-Tabelle mit diesem Namen gefunden. Eine neue Q-Tabelle wird erstellt.'
                    },
                    'save': {
                        'heading': 'Speichern der aktuellen Q-Tabelle',
                        'current': 'Die aktuelle Q-Tabelle heißt ',
                        'command': 'Sind Sie sicher, dass sie die akutelle Q-Tabelle speichern und ueberschreiben moechten?\nGeben Sie "ja" zum Bestaetigen ein.\nGeben Sie "nein" zum Abbrechen ein.'
                    }
                },
                'action': {
                    'heading': 'Parklerner Action',
                    'command': 'Geben Sie "explore" ein, um den Roboter einparken lernen zu lassen.\nGeben Sie "utilize" ein, um die bisher gelernte Q-Tabelle auszunutzen.',
                    'explore': 'Geben Sie ein, wie viele Versuche der Roboter hat, um einparken zu lernen. Bei 250.000 oder mehr, aendert sich die Action nicht mehr automatisch.\nKeine Eingabe, Dezimalzahlen oder negative Zahlen setzen die Anzahl der Versuche zurueck.',
                    'confirmation': 'ist jetzt als Action des Parklerners eingestellt.'
                }
            }
        }
    }

    def __init__(self):
        print("Python versoin: {}".format(sys.version))
        # Create instance of the robot.
        self._bot = None
        # Loads configuration.
        self.load_config()
        self._qtable_pair = {}
        self._parking_learner = None
        self.laod_qtable_pair(name=self.config['qtable_name'])
        # Creates instance of parking_learner.
        self._parking_learner = ParkingLearner(
            bot=self._bot, qtable=self._qtable_pair[self.config['direction'].value], alpha=self.config['alpha'], y=self.config['y'], parkingdirection=self.config['direction'], action=self.config['action'])
        print('Initialazion exhibition done.')

    def load_config(self):
        """
        Load configuration from a config file named exhibition_parking.conf.
        """
        print('Load configuration')
        config_string = ''
        # Checks if configuration file exsist.
        if isfile('./exhibition_parking.conf'):
            # Reads configration file.
            with open("./exhibition_parking.conf") as config_file:
                config_string = config_file.read()
            # Checks if configuration file mathces to the needed format and sets configuration if so.
            if compile('\{"language": "(english|german)", "qtable_name": "[\_\-\.\w]+", "alpha": \d+\.\d+, "y": \d+\.\d+, "direction": "(FORWARD|BACKWARD)", "action": "(explore|utilize)", "color": "(True|False)"\}').match(config_string):
                self.config = loads(config_string)
                self.config['direction'] = Parkingdirection[self.config['direction']]
                print('Loaded configuration:')
            else:
                print(
                    'Configurationfile does not match to the needed format or content. Please check your configurationfile.')
                raise Exception('Missmatching configfile')
        # If config does not match to the nedded format, de default configuration is loaded.
        else:
            self.config = {
                "language": "english",
                "qtable_name": "default",
                "alpha": 1.0,
                "y": 0.95,
                "direction": "{}".format(Parkingdirection.FORWARD.name),
                "action": "explore",
                "color": True
            }
            print('Loaded default configuration:')
        print(self.config_to_string(pretty=True))

    def save_config(self):
        """
        Saves configuration to a config file named exhibition_parking.conf.
        """
        with open(file="./exhibition_parking.conf", mode='w') as config_file:
            config_file.write((self.config_to_string()))

    def config_to_string(self, pretty: bool = False) -> str:
        """
        Converts the configuration into a string.

        Parameter
        ---------
        pretty: bool
            If the String should be formatted or not.

        Returns
        -------
        str: The config as sorted json-string.
        """
        return '{0}{1}"language": "{2}",{1}{3}"qtable_name": "{4}",{1}{3}"alpha": {5},{1}{3}"y": {6},{1}{3}"direction": "{7}",{1}{3}"action": "{8}",{1}{3}"color": "{9}"{10}{11}'.format('{', '\n\t' if pretty else '', self.config['language'], '' if pretty else ' ', self.config['qtable_name'], self.config['alpha'], self.config['y'], self.config['direction'].name, self.config['action'], self.config['color'], '\n' if pretty else '', '}')

    def main(self, random_start: bool = False):
        """
        The main function, which handles inputs.

        Parameter
        ---------
        random_start: bool
            If the commandline argument random_start is set, the start function will generate random start positions.
        """
        self.print_menu()
        user_input = input('> ').lower()
        while user_input != 'quit' and user_input != 'exit':
            execution_time = None
            if user_input == 'start':
                execution_time = self.start(random_start=random_start)
            elif user_input == 'settings' or user_input == 'einstellungen':
                self.settings()
            elif user_input == 'english' or user_input == 'englisch':
                self.config['language'] = 'english'
            elif user_input == 'german' or user_input == 'deutsch':
                self.config['language'] = 'german'
            else:
                print(
                    self.language_package[self.config['language']]['wrong_input'])
            self.print_menu(execution_time)
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
        system('cls' if name == 'nt' else 'clear')

    def print_menu(self, execution_time: datetime.timedelta = None):
        """
        Prints main menu.
        """
        self.clear()
        PrintLogo.print_color(
            PrintLogo) if self.config['color'] else PrintLogo.print_bw(PrintLogo)
        print(self.language_package[self.config['language']]['command'])
        print(self.language_package[self.config['language']]['exit'])
        if execution_time != None:
            print("Last simulation executed in: {}".format(execution_time))

    def print_settings_menu(self):
        """
        Prints settings menu.
        """
        print(
            self.language_package[self.config['language']]['settings']['heading'])
        print(
            self.language_package[self.config['language']]['settings']['commands']['direction'])
        print(
            self.language_package[self.config['language']]['settings']['commands']['action'])
        print(
            self.language_package[self.config['language']]['settings']['commands']['qtable'])
        print(self.language_package[self.config['language']]['back'])

    def settings(self):
        """
        Handles user input for settings menu.
        """
        self.print_settings_menu()
        user_input = input('> ').lower()
        while user_input != 'back' and user_input != 'zurueck':
            if user_input == 'direction' or user_input == 'richtung':
                self.parking_direction_settings()
            elif (user_input == 'q' or user_input == 'table' or user_input == 'q-table' or user_input == 'tabelle' or user_input == 'q-tabelle'):
                self.qtable_settings()
            elif user_input == 'action':
                self.action_settings()
            else:
                print(
                    self.language_package[self.config['language']]['wrong_input'])
            self.print_settings_menu()
            user_input = input('> ').lower()

    def print_direciton_settings_menu(self):
        """
        Prints direction settings menu.
        """
        print(self.language_package[self.config['language']]
              ['settings']['direction']['heading'])
        print("{} {}.".format(self.language_package[self.config['language']]['settings']['direction']['current'],
              self.language_package[self.config['language']]['settings']['direction'][self._parking_learner._parking_direction.value]))
        print("{}.".format(
            self.language_package[self.config['language']]['settings']['direction']['command']))

    def parking_direction_settings(self):
        """
        Handles user input for direction settings.
        Sets parking direction and matching q-table par for forward an backward parking.
        """
        self.print_direciton_settings_menu()
        user_input = input('> ').lower()
        while user_input != 'back' and user_input != 'zurueck':
            if user_input == 'forward' or user_input == 'vorwaerts':
                self._qtable_pair[self._parking_learner._parking_direction.value] = self._parking_learner._qtable
                self._parking_learner.change_parking_direction(
                    new_parking_direction=Parkingdirection.FORWARD, new_qtable=self._qtable_pair[Parkingdirection.FORWARD.value])
                self.config['direction'] = Parkingdirection.FORWARD.name
                break
            elif user_input == 'backward' or user_input == 'rueckwaerts':
                self._qtable_pair[self._parking_learner._parking_direction.value] = self._parking_learner._qtable
                self._parking_learner.change_parking_direction(
                    new_parking_direction=Parkingdirection.BACKWARD, new_qtable=self._qtable_pair[Parkingdirection.BACKWARD.value])
                self.config['direction'] = Parkingdirection.BACKWARD.name
                break
            else:
                print(
                    self.language_package[self.config['language']]['wrong_input'])
            self.print_direciton_settings_menu()
            user_input = input('> ').lower()

    def print_qtable_settings_menu(self):
        """
        Prints q-table settings menu.
        """
        print(self.language_package[self.config['language']]
              ['settings']['qtable']['heading'])
        print("{}.".format(
            self.language_package[self.config['language']]['settings']['qtable']['command']))
        print(self.language_package[self.config['language']]['back'])

    def qtable_settings(self):
        """
        Handles user input for q-table settings.
        Load or save a qtable pair, for forward an backward parking.
        """
        self.print_qtable_settings_menu()
        user_input = input('> ').lower()
        while user_input != 'back' and user_input != 'zurueck':
            if user_input == 'load' or user_input == 'laden':
                self.load_qtable_menu()
                return
            if user_input == 'save' or user_input == 'speichern':
                self.save_qtable()
                return
            self.print_qtable_settings_menu()
            print(
                self.language_package[self.config['language']]['wrong_input'])
            user_input = input('> ').lower()

    def load_qtable_menu(self, wrong_input: bool = False):
        """
        Prints q-table load menu.
        Handles user input.
        Loads q-table pair or creates a new one.

        Parameter
        ---------
        wrong_input: bool = False
            Prints the wrong input message if set, True a wrong input was entered, by default False.
        """
        print(
            self.language_package[self.config['language']]['settings']['qtable']['load']['heading'])
        print(
            self.language_package[self.config['language']]['settings']['qtable']['load']['command'])
        if wrong_input:
            print(
                self.language_package[self.config['language']]['wrong_input'])
        user_input = input('> ').lower()
        if user_input != 'abort' and user_input != 'abbrechen' and user_input != '':
            filename = user_input
            # Ask user to save the current q-table.
            print(
                self.language_package[self.config['language']]['settings']['qtable']['load']['save'])
            user_input = input('> ').lower()
            while user_input != 'yes' and user_input != 'ja' or user_input != 'no' and user_input != 'nein':
                if user_input == 'abort' or user_input == 'abbrechen':
                    return
                print(
                    self.language_package[self.config['language']]['wrong_input'])
                print(
                    self.language_package[self.config['language']]['settings']['qtable']['load']['save'])
                user_input = input('> ').lower()
            # Calls save q-table function.
            if user_input == 'yes' or user_input == 'ja':
                self.save_qtable()
            # Calls actual loading q-table pair function
            self.laod_qtable_pair(name=filename)
        # Recursive while loop if nothing is entered as name.
        if user_input == '':
            print(
                self.language_package[self.config['language']]['wrong_input'])
            self.load_qtable_menu(wrong_input=True)

    def laod_qtable_pair(self, name: str):
        """
        Loads q-table pair from file into self._qtable_pair.
        Creates a new q-table pari if file with q-table pair not exsist.

        Parameter
        ----------
        name: str
            Name of the file containg the q-table pair.
        """
        print('Load q-table')
        self.config['qtable_name'] = name
        path = "./{}.npz".format(name)
        # Checks if file exists with q-table pair exists.
        if isfile(path):
            # Loads q-table pair from file.
            with np.load(file=path, allow_pickle=True) as data:
                self._qtable_pair[18] = data[Parkingdirection.FORWARD.name]
                self._qtable_pair[0] = data[Parkingdirection.BACKWARD.name]
        else:
            # Creates ne q-table pair.
            self._qtable_pair[18] = np.zeros(
                shape=(60, 36, 36, 5, 20), dtype=float)
            self._qtable_pair[0] = np.zeros(
                shape=(60, 36, 36, 5, 20), dtype=float)
        # Sets new q-table in parking_learner.
        if self._parking_learner != None:
            self._parking_learner.change_parking_direction(
                new_parking_direction=self._parking_learner._parking_direction, new_qtable=self._qtable_pair[self._parking_learner._parking_direction.value])

    def print_save_qtable_menu(self):
        """
        Prints q-table save menu.
        """
        print(
            self.language_package[self.config['language']]['settings']['qtable']['save']['heading'])
        print("{}{}".format(self.language_package[self.config['language']]
              ['settings']['qtable']['save']['current'], self.config['qtable_name']))
        print(self.language_package[self.config['language']]
              ['settings']['qtable']['save']['command'])

    def save_qtable(self):
        """
        Handles user input.
        Saves current q-table pair.
        """
        self.print_save_qtable_menu()
        user_input = input('> ').lower()
        while user_input != 'yes' and user_input != 'ja' and user_input != 'no' and user_input != 'nein':
            print(
                self.language_package[self.config['language']]['wrong_input'])
            self.print_save_qtable_menu()
        # Saves the current q-table pair, if the question was confirmed.
        if user_input == 'yes' or user_input == 'ja':
            self._qtable_pair[self._parking_learner._parking_direction.value] = self._parking_learner._qtable
            np.savez_compressed(self.config['qtable_name'], FORWARD=self._qtable_pair[Parkingdirection.FORWARD.value],
                                BACKWARD=self._qtable_pair[Parkingdirection.FORWARD.value])

    def print_action_settings_menu(self):
        """
        Prints menu to change parking_learner action.
        """
        print(self.language_package[self.config['language']]
              ['settings']['action']['heading'])
        print(self.language_package[self.config['language']]['back'])

    def action_settings(self):
        """
        Handles user input.
        Changes parking_learner.action
        """
        self.print_action_settings_menu()
        user_input = input('> ').lower()
        while user_input != 'back' and user_input != 'zurueck':
            if user_input == 'utilize':
                self._parking_learner.set_action_utilize()
                self.config['action'] = 'utilize'
                print("'{}' {}".format(self._parking_learner._action,
                      self.language_package[self.config['language']]['settings']['action']['confirmation']))
                sleep(1)
                return
            elif user_input == 'explore':
                print(
                    self.language_package[self.config['language']]['settings']['action']['explore'])
                user_input = input('> ').lower()
                if user_input.isnumeric():
                    entered_number = abs(int(user_input))
                    exploration_counter = 250000 - entered_number if entered_number < 250000 else 250001
                else:
                    exploration_counter = 0
                self._parking_learner.set_action_explore(
                    exploration_counter=exploration_counter)
                self.config['action'] = 'explore'
                print("'{}' {}".format(self._parking_learner._action,
                      self.language_package[self.config['language']]['settings']['action']['confirmation']))
                sleep(1)
                return
            elif user_input == "back":
                return
            print(
                self.language_package[self.config['language']]['wrong_input'])
            self.print_action_settings_menu()
            user_input = input('> ').lower()

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
        for x in range(250000):
            if random_start:
                start_distance = randint(0, 60)
                start_angle = randint(0, 35)
                start_orientation = randint(0, 35)
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
        sleep(2)
        return end_time - start_time


if __name__ == '__main__':
    try:
        # Checks for random_start in comandline arguments.
        random_start = True if 'random_start' in sys.argv[
            1:] or 'random' in sys.argv[1:] else False
        # Generates simulator instance.
        runner = Simulator()
        # Executes simulation.
        runner.main(random_start=random_start)
    except Exception as exception:
        try:
            # If any error is catched, it is tried to write into an error log file.
            log_file = open("error.log", "a")
            log_file.write("{}\nTraceback:\n{}".format(
                str(exception), traceback.format_exc()))
            log_file.close()
        except Exception as inner_exception:
            # If the logging into a file failes, the error is printed to the command line.
            print('Outer Exception:')
            traceback.print_exception()
            print('Inner Exception')
            traceback.print_exception()
