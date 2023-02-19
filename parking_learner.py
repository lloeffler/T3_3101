import time
import random

import numpy as np

from botlib.bot import Bot

# A q-learning algorithm to learn how to park the robot.


class ParkingLearner:
    def __init__(self, bot, qtable=None):
        self._bot = bot
        self._qtable = qtable or np.ndarray(
            shape=(60, 36, 36), dtype=float)
        self._state = {
            'rho': 0,
            'phi': 0,
            'orientation': 0,
            'parking': False,
            'action': 'utilize' if qtable else 'explore'
        }
        if not qtable:
            for q in self._qtable:
                q = np.ndarray(shape=(21, 20), dtype=float)

        self._turning_radius = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    # Converts cartesian coordinates into polar coordinates.
    # param x: distance between point and y-axis.
    # param y: distance between point and x-axis.
    # return tuple: rho and phi of given point.
    def cart2pol(x, y):
        rho = np.sqrt(x**2 + y**2)
        phi = np.arctan2(y, x)
        return (rho, phi)

    # Converts polar coordinates into cartesian coordinates.
    # param rho: radius of the point in the unitary circle.
    # param phi: angel of phi of the point in the unitary circle.
    # return tuple: x and y of given point.
    def pol2cart(rho, phi):
        x = rho * np.cos(phi)
        y = rho * np.sin(phi)
        return (x, y)

    # Calculates and sets new realtive position to parking lot as state.
    # param double direction: steering impact from -1 to +1 in 0.1 steps.
    # param int length: how long the robot wil drive in cm.
    # return boolean: if the robot is less equals 60 cm from the parking lot away.
    def update_state(self, direction, lenght):
        [x, y] = self.pol2cart(self._state['rho'], self._state['phi'])
        if direction == 0:
            # Robot drives straight forward
            [delta_x, delta_y] = self.pol2cart(
                lenght, self._state['orientation'])
            x_t = x + delta_x
            y_t = y + delta_y
        else:
            # Robot drives a curve
            x_t = x
            y_t = y

        [rho_t, phi_t] = self.cart2pol(x_t, y_t)
        self._state['rho'] = rho_t
        self._state['phi'] = phi_t
        return rho_t <= 60

    # Moves Robot and calculate its new position relative to the parking lot
    # param direction: steering impact from -1 to +1 in 0.1 steps
    # param length: how long the robot wil drive in cm
    ''' return boolean: if the robot is less equals 60 cm from the parking lot away '''

    def action(self, direction, length):
        self._bot.drive_steer(direction)
        time.sleep(0.5)
        self._bot.drive_power(20)
        time.sleep(length)
        self._bot.drive_power(0)
        self.update_state(self, direction, length)

    # Pauses line detection and starts parking process.
    def start_parking(self):
        '''
        stop pause line detection and following the line
        calculate position relativ to parking lot
        '''
        distance = 0
        angel = 0
        orientation = 180
        self._bot.drive_steer(0)
        self._bot.drive_power(0)
        self.parking(distance, angel, orientation)

    # Resets state/relativ position to 0.
    # Sets parking to false, to leave while loop from self.parking();
    def abort_parking(self):
        self._state['rho'] = 0
        self._state['phi'] = 0
        self._state['orientation'] = 0
        self._state['parking'] = False
        ''' return to line deetection and following the line '''

    # Checks if the right parking position is reached.
    # return boolean: true if calculated pisition is correct, proofed by optical detection.
    def check_location(self):
        calculated = (self._state['rho'] ==
                      0 and self._state['orientation'] == 0)
        ''' somthing with opencv, check if parking lot entrance is in lower x% and in the middle of the picture.
         if actual position and calculated position not true, recalculate current position, based on seen parking lot position. '''
        return calculated

    # Parks the robot automaticly.
    # If the action is set to 'utilize', the robot will use the filled q-table to find the best steps to park.
    # If the action is set to 'explore', the robot will try some random actions to find a way to park and fill the q-table.
    # param distance: the distance between the robot and tha parking lot in cm.
    # param angel: the angel how much the parking lot is left or right from the robot in degree (°).
    # param orientation: how much the robot is turned relativ to the parking lot in degree (°).
    def parking(self, distance, angel, orientation):
        self._state['rho'] = distance
        self._state['phi'] = angel
        self._state['orientation'] = orientation
        while self._state['parking']:
            # Decides to utilize the filled q-table oder explore and fill the q-table.
            # Uses q-table to find a way to park.
            if self._state['action'] == 'utilize':
                [action_direction, action_lenght] = np.unravel_index(self._qtable[self._state['rho'], self._state['phi'], self._state['orientation']].argmax(
                ), np.unravel_index(self._qtable[self._state['rho'], self._state['phi'], self._state['orientation']].shape))
                self.action(action_direction, action_lenght)
                # Stays in the parking lot for 30 seconds, after a succesfully parking manover.
                if self.check_location():
                    self._state['parking'] = False
                    time.sleep(30)
            # Fills q-Table
            if self._state['action'] == 'explore':
                direction = round(random.randint(-10, 11)/10, 1)
                length = 0
                while length == 0:
                    length = random.randint(-10, 11)
                ''' Add q-function to calculate the reward for the robot '''
                self.action(direction, length)
            # Aborts parking, if the robot is to far away from the parking lot.
            if self._state['rho'] > 60:
                self.abort_parking()
