import time
import sys
import os.path

import numpy as np

from botlib.bot import Bot
from parking_learner import ParkingLearner
from parkingdirection import Parkingdirection


class Exhibition:
    """
    A small aplication for the 'Hanover Messe', to demonstrate a parking swarm robot. The parking will be self learnd by the robot with q-learning.

    Attributes
    ----------
    language_package: dictionary
        Contains menu translaiton in english and german.
    language: string = 'english'
        The current language, by default english.
    forward_qtable: np.ndarray
        A three demensional numpy.ndarray with shape=(60, 36, 36), containing two dimensional numpy.ndarray with shape=(9, 20).
    """
    language_package = {
        'english': {
            'command': 'Enter start to start the parking.\nEnter settings to open the settings menu.\nEnter german to change the language. Geben Sie deutsch ein um die Sprache zu ändern.',
            'back': 'Enter back to go to the previous menu.',
            'exit': 'Enter exit or quit to leave to application.',
            'wrong_input': 'Error: Wrong input, please enter one of the mentioned options.',
            'settings': {
                'heading': 'Settings',
                'commands': {
                    'direction': 'Enter direction to change the parking direciton.',
                    'qtable': 'Enter q, table or q-table to open the q-table settings.'
                },
                'direction': {
                    'heading': 'Parking direction',
                    'current': 'The current parking direction is ',
                    18: 'forward',
                    0: 'backward',
                    'command': 'To change the parking direction enter either forward or backward.'
                },
                'qtable': {
                    'heading': 'Q-Table settings',
                    'commmand': 'Enter load to load a new q-table.\nEnter save to save the current q-table.',
                    'load': {
                        'heading': 'Load a new q-table',
                        'command': 'Enter the name of q-table to load.\nIf the entered q-table does not exists, a empty q-table is loaded.\nEnter abort the abort.'
                    },
                    'save': {
                        'heading': 'Save the current q-table',
                        'current': 'The current q-table is named ',
                        'command': 'Are you sure, you want to save the current q-table and override the saved one?\nEnter yes to confirm.\nEnter no the abort.'
                    }
                },
            }
        },
        'german': {
            'command': 'Geben Sie "start" ein, um den Einparkvorgang zu starten.\nGeben Sie "Einstellungen" ein, um das Einstellungsmenü zu öffnen.\nGeben Sie englisch ein um die Sprache zu ändern. Enter english to change the language.',
            'back': 'Geben Sie "zurück" ein, um zum vorherigen Menü zu gelangen.',
            'exit': 'Geben Sie "exit" oder "quit" ein um die Anwendung zu verlassen.',
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
                    'command': 'Um die Einparkrichtung zu ändern, entweder vorwärts oder rückwärts eingeben.'
                },
                'qtable': {
                    'heading': 'Q-Tabellen Einstellungen',
                    'commmand': 'Geben Sie "laden" ein, um eine Q-Tabelle zu laden.\nGeben Sie "speichern" ein, um die aktuelle Q-Tabelle zu speichern.',
                    'load': {
                        'heading': 'Neue Q-Tabelle laden',
                        'command': 'Geben Sie den Namen der Q-Tabelle ein, um diese zu laden.\nWenn die eingegebene Q-Tabelle nicht existiert, wird eine neue angelegt.\nGeben Sie "abbrechen" zum Abbrechen ein.'
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
    language = 'english'

    def __init__(self):
        self._bot = Bot()
        self._linetracker = self._bot.linetracker()
        self._qtable_pair = self._laod_qtable(qtable='default')
        alpha, y = self.load_exploration_rates() 
        self._parking_learner = ParkingLearner(bot=self._bot, qtable=self._qtable_pair[18], alpha=alpha, y=y)
        print('Calibrate robot')
        self._bot.calibrate()

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
                self.language = 'english'
            elif user_input == 'german' or user_input == 'deutsch':
                self.language = 'german'
            else:
                print(f"{self.language_package['wrong_input']}")
            self.print_menu(administartor_mode)
            user_input = input('> ').lower()
        # cleanup

    def print_menu(self, administartor_mode: bool = False):
        """
        Prints main menu.

        Parameters
        ----------
        administartor_mode: bool = False
            If administrationmode is active, True, the exit command will be shown, by default False.
        """
        print(f"{self.language_package[self.language]['command']}")
        if administartor_mode:
            print(f"{self.language_package[self.language]['exit']}")

    def print_settings_menu(self, administartor_mode: bool = False):
        """
        Prints settings menu.

        Parameters
        ----------
        administartor_mode: bool = False
            If administrationmode is active, True, the q-table settings will be shown, by default False.
        """
        print(f"{self.language_package[self.language]['settings']['heading']}")
        print(
            f"{self.language_package[self.language]['settings']['commands']['direction']}")
        if administartor_mode:
            print(
                f"{self.language_package[self.language]['settings']['commands']['qtable']}")
        print(f"{self.language_package[self.language]['back']}")

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
                print(f"{self.language_package['wrong_input']}")
            self.print_settings_menu(administartor_mode)
            user_input = input('> ').lower()

    def print_direciton_settings_menu(self):
        """
        Prints direction settings menu.
        """
        print(f"{self.language_package['settings']['direction']['heading']}")
        print(f"{self.language_package['settings']['direction']['current']} {self.language_package['settings']['direction'][self._parking_learner._parking_direction.value]}.")
        print(f"{self.language_package['settings']['direction']['command']}.")

    def direction_settings(self):
        """
        Handles user input for direction settings.
        Sets parking direction and matching q-table par for forward an backward parking.
        """
        self.print_direciton_settings_menu()
        user_input = input('> ').lower()
        while user_input != 'back' and user_input != 'zurück':
            if user_input == 'forward' or user_input == 'vorwärts':
                self._parking_learner.change_parking_direction(new_parking_direction=Parkingdirection.FORWARD, new_qtable=self._qtable_pair[Parkingdirection.FORWARD.value])
                break
            elif user_input == 'backward' or user_input == 'rückwärts':
                self._parking_learner.change_parking_direction(new_parking_direction=Parkingdirection.BACKWARD, new_qtable=self._qtable_pair[Parkingdirection.BACKWARD.value])
                break
            else:
                print(f"{self.language_package['wrong_input']}")
            self.print_direciton_settings_menu()
            user_input = input('> ').lower()

    def print_qtable_settings_menu(self):
        """
        Prints q-table settings menu.
        """
        print(f"{self.language_package['settings']['qtable']['heading']}")
        print(f"{self.language_package['settings']['qtable']['command']}.")
        print(f"{self.language_package[self.language]['back']}")

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
                
    def load_qtable(self):
        """
        Prints q-table load menu.
        Handles user input.
        Loads q-table pair or creates a new one.
        """
        print(f"{self.language_package['settings']['qtable']['load']['heading']}")
        print(f"{self.language_package['settings']['qtable']['load']['command']}")


if __name__ == '__main__':
    administartor_mode = True if 'administartor_mode' in sys.argv[
        1:] or 'administartormode' in sys.argv[1:] else False
    runner = Exhibition()
    runner.main(administartor_mode)
