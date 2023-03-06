import json
import re
import time
import sys
import os.path

import numpy as np

from botlib import Bot
from parking_learner import ParkingLearner
from parkingdirection import Parkingdirection


class Exhibition:
    """
    A small aplication for the 'Hanover Messe', to demonstrate a parking swarm robot. The parking will be self learnd by the robot with q-learning.

    Attributes
    ----------
    language_package: dictionary
        Contains menu translaiton in english and german.
    config: dict
        A dictionary containing the current configuration.
            {
                'language': str, the current language, by default english.
                'qtable_name': str, the name of the current q-table, by default 'default'.
                'alpha': float, the current exploration rate, by default 1.
                'y': float, the other current exploration rate, by default 0.95.
                'direction': Parkingdirection, the current parking direction, by default Parkingdirection.FORWARD.
            }
    _qtable_pair: List/dict
        The current q-tables for parking forward an backward.
        A q-table is a three demensional numpy.ndarray with shape=(60, 36, 36), containing two dimensional numpy.ndarray with shape=(9, 20).
        The q-table contains the potential reward of every combination of state (relativ position of the robot to the parking lot) and action (lenght and direction driving).
    """
    language_package = {
        'english': {
            'command': 'Enter "start" to start the parking.\nEnter "settings" to open the settings menu.\nEnter "german" to change the language. Geben Sie "deutsch" ein um die Sprache zu ändern.',
            'back': 'Enter "back" to go to the previous menu.',
            'exit': 'Enter "exit" or quit to leave to application.',
            'config': 'Enter "yes" to save the current configuration.\nEnter "no" to leave the application without saving the current configuration.',
            'wrong_input': 'Error: Wrong input, please enter one of the mentioned options.',
            'settings': {
                'heading': 'Settings',
                'commands': {
                    'direction': 'Enter "direction" to change the parking direciton.',
                    'qtable': 'Enter "q", "table" or "q-table" to open the q-table settings.'
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
            }
        },
        'german': {
            'command': 'Geben Sie "start" ein, um den Einparkvorgang zu starten.\nGeben Sie "Einstellungen" ein, um das Einstellungsmenü zu öffnen.\nGeben Sie "englisch" ein um die Sprache zu ändern. Enter "english" to change the language.',
            'back': 'Geben Sie "zurück" ein, um zum vorherigen Menü zu gelangen.',
            'exit': 'Geben Sie "exit" oder "quit" ein um die Anwendung zu verlassen.',
            'config': 'Geben Sie "ja" ein, um die aktuelle Konfiguration zu speichern.\nGeben sie "nein" ein, um die Anwendung ohne speichern der Konfiguration zu verlassen.',
            'wrong_input': 'Fehler: Falsche Eingabe, bitte geben Sie eine der genannten Auswahlmöglichkeiten ein.',
            'settings': {
                'heading': 'Einstellungen',
                'commands': {
                    'direction': 'Geben Sie "Richtung" ein, um die Einparkrichtung zu ändern.',
                    'qtable': 'Geben Sie "q", "Tabelle" or "Q-Tabelle" ein, um die Einstellungen der Q-Tabelle zu öffnen.'
                },
                'direction': {
                    'heading': 'Einparkrichtung',
                    'current': 'Die aktuelle Einparkrichtung ist ',
                    18: 'vorwärts',
                    0: 'rückwärts',
                    'command': 'Um die Einparkrichtung zu ändern, entweder "vorwärts" oder "rückwärts" eingeben.'
                },
                'qtable': {
                    'heading': 'Q-Tabellen Einstellungen',
                    'commmand': 'Geben Sie "laden" ein, um eine Q-Tabelle zu laden.\nGeben Sie "speichern" ein, um die aktuelle Q-Tabelle zu speichern.',
                    'load': {
                        'heading': 'Neue Q-Tabelle laden',
                        'command': 'Geben Sie den Namen der Q-Tabelle ein, um diese zu laden.\nWenn die eingegebene Q-Tabelle nicht existiert, wird eine neue angelegt.\nGeben Sie "abbrechen" zum Abbrechen ein.',
                        'save': 'Möchten Sie die aktuelle Q-Tabelle speichern?\nGeben Sie "ja" ein, um zu speichern.\nGeben Sie "nein" ein, um ohne zu speichern fortzufahren.',
                        'not_found': 'Es wurde keine Q-Tabelle mit diesem Namen gefunden. Eine neue Q-Tabelle wird erstellt.'
                    },
                    'save': {
                        'heading': 'Speichern der aktuellen Q-Tabelle',
                        'current': 'Die aktuelle Q-Tabelle heißt ',
                        'command': 'Sind Sie sicher, dass sie die akutelle Q-Tabelle speichern und überschreiben möchten?\nGeben Sie "ja" zum Bestätigen ein.\nGeben Sie "nein" zum Abbrechen ein.'
                    }
                }
            }
        }
    }

    def __init__(self):
        # Create instance of the robot.
        self._bot = Bot()
        self._linetracker = self._bot.linetracker()
        # Loads configuration.
        self.load_config()
        self.laod_qtable_pair(
            name=self.config['qtable_name'])
        # Creates instance of parking_learner.
        self._parking_learner = ParkingLearner(
            bot=self._bot, qtable=self._qtable_pair[18], alpha=self.config['alpha'], y=self.config['y'], parkingdirection=self.config['dircetion'])
        print('Calibrate robot')
        # Waits a second before calibrating the robot.
        time.sleep(1)
        self._bot.calibrate()

    def load_config(self):
        """
        Load configuration from a config file named exhibition_parking.conf.
        """
        config_string = ''
        # Checks if configuration file exsist.
        if os.path.isfile('./exhibition_parking.conf'):
            # Reads configration file.
            with open("./exhibition_parking.conf") as config_file:
                config_string = config_file.read()
        # Checks if configuration file mathces to the needed format and sets configuration if so.
        if re.compile("\{'language': '[english|german]', 'qtable_name': '[A-Za-z0-9]+', 'alpha': \d+\.\d+, 'y': \d+\.\d+, 'direction': [FORWARD|BACKWARD]\}").match(config_string):
            self.config = json.loads(config_string)
        # If config does not match to the nedded format, de default configuration is loaded.
        else:
            self.config = {
                'language': 'english',
                'qtable_name': 'default',
                'alpha': 1.0,
                'y': 0.95,
                'direction': Parkingdirection.FORWARD
                }

    def save_config(self):
        """
        Saves configuration to a config file named exhibition_parking.conf.
        """
        with open(file="./exhibition_parking.conf", mode='w') as config_file:
            config_file.write(str(self.config))

    def main(self, administartor_mode: bool = False):
        """
        The main function, which handles inputs.

        Parameters
        ----------
        administartor_mode: bool = False
            If administrationmode is active, True, the exit command will be shown, by default False.
        """
        self.print_menu(administartor_mode)
        user_input = input('> ').lower()
        while user_input != 'quit' and user_input != 'exit':
            if user_input == 'start':
                self.start()
            elif user_input == 'settings' or user_input == 'einstellungen':
                self.settings()
            elif user_input == 'english' or user_input == 'englisch':
                self.config['language'] = 'english'
            elif user_input == 'german' or user_input == 'deutsch':
                self.config['language'] = 'german'
            else:
                print(f"{self.language_package[self.config['language']]['wrong_input']}")
            self.print_menu(administartor_mode)
            user_input = input('> ').lower()
        print(f"{self.language_package[self.config['language']]['config']}")
        user_input = input('> ').lower()
        while user_input != 'yes' and user_input != 'ja' and user_input != 'no' and user_input != 'nein':
            print(f"{self.language_package[self.config['language']]['wrong_input']}")
            print(f"{self.language_package[self.config['language']]['config']}")
            user_input = input('> ').lower()
        if user_input == 'yes' or user_input == 'ja':
            self.save_config()
        print('Bye')

    def print_menu(self, administartor_mode: bool = False):
        """
        Prints main menu.

        Parameters
        ----------
        administartor_mode: bool = False
            If administrationmode is active, True, the exit command will be shown, by default False.
        """
        print(f"{self.language_package[self.config['language']]['command']}")
        if administartor_mode:
            print(f"{self.language_package[self.config['language']]['exit']}")

    def print_settings_menu(self, administartor_mode: bool = False):
        """
        Prints settings menu.

        Parameters
        ----------
        administartor_mode: bool = False
            If administrationmode is active, True, the q-table settings will be shown, by default False.
        """
        print(
            f"{self.language_package[self.config['language']]['settings']['heading']}")
        print(
            f"{self.language_package[self.config['language']]['settings']['commands']['direction']}")
        if administartor_mode:
            print(
                f"{self.language_package[self.config['language']]['settings']['commands']['qtable']}")
        print(f"{self.language_package[self.config['language']]['back']}")

    def settings(self, administartor_mode: bool = False):
        """
        Handles user input for settings menu.

        Parameters
        ----------
        administartor_mode: bool = False
            If administrationmode is active, True, the q-table settings will be enabled, by default False.
        """
        self.print_settings_menu(administartor_mode)
        user_input = input('> ').lower()
        while user_input != 'back' and user_input != 'zurück':
            if user_input == 'direction' or user_input == 'richtung':
                self.direction_settings()
            elif (user_input == 'q' or user_input == 'table' or user_input == 'q-table' or user_input == 'tabelle' or user_input == 'q-tabelle') and administartor_mode:
                self.qtable_settings()
            else:
                print(f"{self.language_package[self.config['language']]['wrong_input']}")
            self.print_settings_menu(administartor_mode)
            user_input = input('> ').lower()

    def print_direciton_settings_menu(self):
        """
        Prints direction settings menu.
        """
        print(f"{self.language_package[self.config['language']]['settings']['direction']['heading']}")
        print(
            f"{self.language_package[self.config['language']]['settings']['direction']['current']} {self.language_package[self.config['language']]['settings']['direction'][self._parking_learner._parking_direction.value]}.")
        print(f"{self.language_package[self.config['language']]['settings']['direction']['command']}.")

    def direction_settings(self):
        """
        Handles user input for direction settings.
        Sets parking direction and matching q-table par for forward an backward parking.
        """
        self.print_direciton_settings_menu()
        user_input = input('> ').lower()
        while user_input != 'back' and user_input != 'zurück':
            if user_input == 'forward' or user_input == 'vorwärts':
                self._parking_learner.change_parking_direction(
                    new_parking_direction=Parkingdirection.FORWARD, new_qtable=self._qtable_pair[Parkingdirection.FORWARD.value])
                self.config['direction'] = Parkingdirection.FORWARD.name
                break
            elif user_input == 'backward' or user_input == 'rückwärts':
                self._parking_learner.change_parking_direction(
                    new_parking_direction=Parkingdirection.BACKWARD, new_qtable=self._qtable_pair[Parkingdirection.BACKWARD.value])
                self.config['direction'] = Parkingdirection.BACKWARD.name
                break
            else:
                print(f"{self.language_package[self.config['language']]['wrong_input']}")
            self.print_direciton_settings_menu()
            user_input = input('> ').lower()

    def print_qtable_settings_menu(self):
        """
        Prints q-table settings menu.
        """
        print(f"{self.language_package[self.config['language']]['settings']['qtable']['heading']}")
        print(f"{self.language_package[self.config['language']]['settings']['qtable']['command']}.")
        print(f"{self.language_package[self.config['language']]['back']}")

    def qtable_settings(self):
        """
        Handles user input for q-table settings.
        Load or save a qtable pair, for forward an backward parking.
        """
        self.print_qtable_settings_menu()
        user_input = input('> ').lower()
        while user_input != 'back' and user_input != 'zurück':
            if user_input == 'load' or user_input == 'laden':
                self.load_qtable()
            if user_input == 'save' or user_input == 'speichern':
                self.save_qtable()

    def load_qtable(self):
        """
        Prints q-table load menu.
        Handles user input.
        Loads q-table pair or creates a new one.
        """
        print(
            f"{self.language_package[self.config['language']]['settings']['qtable']['load']['heading']}")
        print(
            f"{self.language_package[self.config['language']]['settings']['qtable']['load']['command']}")
        user_input = input('> ').lower()
        if user_input != 'abort' and user_input != 'abbrechen' and user_input != '':
            filename = user_input
            # Ask user to save the current q-table.
            print(
                f"{self.language_package[self.config['language']]['settings']['qtable']['load']['save']}")
            user_input = input('> ').lower()
            while user_input != 'yes' and user_input != 'ja' or user_input != 'no' and user_input != 'nein':
                if user_input == 'abort' or user_input == 'abbrechen':
                    return
                print(f"{self.language_package[self.config['language']]['wrong_input']}")
                print(
                    f"{self.language_package[self.config['language']]['settings']['qtable']['load']['save']}")
                user_input = input('> ').lower()
            # Calls save q-table function.
            if user_input == 'yes' or user_input == 'ja':
                self.save_qtable()
            # Calls actual loading q-table pair function
            self.laod_qtable_pair(name=filename)
        # Recursive while loop if nothing is entered as name.
        if user_input == '':
            print(f"{self.language_package[self.config['language']]['wrong_input']}")
            self.load_qtable()

    def laod_qtable_pair(self, name: str):
        """
        Loads q-table pair from file into self._qtable_pair.
        Creates a new q-table pari if file with q-table pair not exsist.

        Parameters
        ----------
        name: str
            Name of the file containg the q-table pair.
        """
        self.config['qtable_name'] = name
        path = f"./{name}.npz"
        # Checks if file exists with q-table pair exists
        if os.path.isfile(path):
            # Loads q-table pair from file.
            with np.load(path) as data:
                self._qtable_pair[18] = data[Parkingdirection.FORWARD.name]
                self._qtable_pair[0] = data[Parkingdirection.BACKWARD.name]
        else:
            # Creates ne q-table pair
            self._qtable_pair[18] = np.ndarray(
                shape=(60, 36, 36), dtype=np.ndarray)
            self._qtable_pair[0] = np.ndarray(
                shape=(60, 36, 36), dtype=np.ndarray)
            for table in self._qtable_pair:
                for q in table:
                    q = np.ndarray(shape=(9, 20), dtype=float)
        # Sets new q-table in parking_learner
        self._parking_learner.change_parking_direction(
            new_parking_direction=self._parking_learner._parking_direction, new_qtable=self._qtable_pair[self._parking_learner._parking_direction.value])

    def print_save_qtable_menu(self):
        """
        Prints q-table save menu.
        """
        print(
            f"{self.language_package[self.config['language']]['settings']['qtable']['save']['heading']}")
        print(
            f"{self.language_package[self.config['language']]['settings']['qtable']['save']['current']}{self.config['qtable_name']}")
        print(
            f"{self.language_package[self.config['language']]['settings']['qtable']['save']['command']}")

    def save_qtable(self):
        """
        Handles user input.
        Saves current q-table pair.
        """
        self.print_save_qtable_menu()
        user_input = input('> ').lower()
        while user_input != 'yes' and user_input != 'ja' and user_input != 'no' and user_input != 'nein':
            print(f"{self.language_package[self.config['language']]['wrong_input']}")
            self.print_save_qtable_menu()
        # Saves the current q-table pair, if the question was confirmed.
        if user_input == 'yes' or user_input == 'ja':
            np.savez_compressed(self.config['qtable_name'], forward=self._qtable_pair[Parkingdirection.FORWARD.value],
                                backward=self._qtable_pair[Parkingdirection.FORWARD.value])


if __name__ == '__main__':
    try:
        administartor_mode = True if 'administartor_mode' in sys.argv[
            1:] or 'administartormode' in sys.argv[1:] else False
        runner = Exhibition()
        runner.main(administartor_mode)
    except Exception as exception:
        try:
            log_file = open("error.log", "a")
            log_file.write(exception.__traceback__)
            log_file.close()
        except Exception as inner_exception:
            print('Outer Exception:')
            print(exception.__traceback__)
            print('Inner Exception')
            print(f"{inner_exception.__traceback__}")
