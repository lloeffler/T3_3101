import time
import random

import numpy as np

from botlib.bot import Bot

# A q-learning algorithm to learn how to park the robot.
# The q-table (qtable) is five a dimensional array,
# that contains the reward of all actions from all possible states.
# The state is a dictionary, that contains the radius rho, tha angle phi and the
# orientation of the robot. Phi and orientation have the unit radians. The state
# describes the relative position of the robot to the parking lot (entrance).
# The robot is parking when self._parking is True.
# The robot can explore the possibiliteies how it can park and fill its q-table or
# it can utilize the filled q-table to execute the learned actions to park mostly
# efficient.
# Alpha is the exploration rate.
# r_t is the other exploration rate.
# The turnings radius for all allowed steer angles are fix values stored in the
# array self._turning_radius.
# The exploration coutner limits the number of explorations to 250.000 explorations.


class ParkingLearner:
    # Creates a new instance of a parking learner.
    # param bot: a botlib.bot instance of the robot.
    # param qtable: a three demensional numpy.ndarray with shape=(60, 36, 36)
    #               containing two dimensional numpy.ndarray with shape=(9, 20).
    # param alpha: the exploration rate.
    # param r_t: the other expploration rate.
    def __init__(self, bot, qtable=None, alpha=None, r_t=None):
        self._bot = bot
        self._qtable = qtable or np.ndarray(
            shape=(60, 36, 36), dtype=float)
        self._state = {
            'rho': 0,
            'phi': 0,
            'orientation': 0
        }
        self._parking = False
        self._action = 'utilize' if qtable else 'explore'
        self._alpha = alpha or 1
        self._r_t = r_t or 0.95
        if not qtable:
            for q in self._qtable:
                q = np.ndarray(shape=(9, 20), dtype=float)
        self._exploration_counter = 0
        self._turning_radius = [0, 1, 2, 3]

    # Converts cartesian coordinates into polar coordinates.
    # param x: distance between point and y-axis.
    # param y: distance between point and x-axis.
    # return tuple: rho and phi in radians of given point.
    def cart2pol(x, y):
        rho = np.sqrt(x**2 + y**2)
        phi = np.arctan2(y, x)
        return (rho, phi)

    # Converts polar coordinates into cartesian coordinates.
    # param rho: radius of the point in the unitary circle.
    # param phi: angle of phi of the point in the unitary circle in radians.
    # return tuple: x and y of given point.
    def pol2cart(rho, phi):
        x = rho * np.cos(phi)
        y = rho * np.sin(phi)
        return (x, y)

    # Sets self._action to 'utilize', to change behavior.
    def set_action_utilize(self):
        self._action = 'utilize'

    # Sets self._action to 'explore', to change behavior and resets self._exploration_counter.
    # param exploration_counter: the new exploration counter to be set, by default 0, to reset exploration counter
    def set_action_utilize(self, exploration_counter=0):
        self._action = 'explore'
        self._exploration_counter = exploration_counter

    # Calculates and sets new realtive position to parking lot as state.
    # param double direction: steering impact from -1 to +1 in 0.1 steps.
    # param int length: how long the robot wil drive in cm.
    # return boolean: True if the robot is less equals 60 cm from the parking lot away.
    def update_state(self, direction, lenght):
        [x, y] = self.pol2cart(self._state['rho'], self._state['phi'])
        if direction == 0:
            # Robot drives straight forward.
            [delta_x, delta_y] = self.pol2cart(
                lenght, self._state['orientation'])
            x_t = x + delta_x
            y_t = y + delta_y
            orientation_t = self._state['orientation']
        else:
            # Robot drives a curve.
            # Calculating centre of rotation (x_m, y_m) of the turning circle.
            [x_m_delta, y_m_delta] = self.pol2cart(self._turning_radius[abs(direction)], self._state['orientation'] + (
                1.5 * np.pi)) if direction > 0 else self.pol2cart(self._turning_radius[abs(direction)], self._state['orientation'] + (0.5 * np.pi))
            x_m = x + x_m_delta
            y_m = y + y_m_delta
            # Calculating perimeter of the turningcicle.
            turning_perimeter = 2 * np.pi * \
                self._turning_radius[abs(direction)]
            turning_radiant = 2 * np.pi * (-lenght/turning_perimeter)
            # Calculating new robot coordinates.
            [x_m_delta_t, y_m_delta_t] = self.pol2cart(self._turning_radius[abs(
                direction)], (self._state['orientation'] + np.pi + turning_radiant))
            # Calculates new robot orientation
            orientation_t = self._state['orientation'] + turning_radiant
            x_t = x_m + x_m_delta_t
            y_t = y_m + y_m_delta_t
        # Sets new position as robot state.
        [rho_t, phi_t] = self.cart2pol(x_t, y_t)
        self._state['rho'] = rho_t
        self._state['phi'] = phi_t
        self._state['orientation'] = orientation_t
        return rho_t <= 60

    # Moves Robot and calculate its new position relative to the parking lot
    # param direction: steering impact from -1 to +1 in 0.1 steps
    # param length: how long the robot wil drive in cm
    # return boolean: True if the robot is less equals 60 cm from the parking lot away
    def action(self, direction, length):
        self._bot.drive_steer(direction)
        time.sleep(0.5)
        self._bot.drive_power(20)
        time.sleep(length)
        self._bot.drive_power(0)
        return self.update_state(self, direction, length)

    # Pauses line detection and starts parking process.
    def start_parking(self):
        self._bot.linetracker._autopilot(False)
        '''
        stop pause line detection and following the line
        calculate position relativ to parking lot
        '''
        distance = 0
        angle = 0
        orientation = 180
        self._bot.drive_steer(0)
        self._bot.drive_power(0)
        self.parking(distance, angle, orientation)

    # Resets the state, aka. the relativ position, to 0.
    # Sets parking to false, to leave while loop from self.parking();
    def end_parking(self):
        self._state['rho'] = 0
        self._state['phi'] = 0
        self._state['orientation'] = 0
        ''' return to line deetection and following the line '''
        self._bot.linetracker._autopilot(True)

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
    # param angle: the angle how much the parking lot is left or right from the robot in rad.
    # param orientation: how much the robot is turned relativ to the parking lot in rad.
    def parking(self, distance, angle, orientation):
        self._state['rho'] = distance
        self._state['phi'] = angle
        self._state['orientation'] = orientation
        is_in_range = True
        # Increases exploration counter, if the robot is exploring.
        if self._action == 'explore':
            self._exploration_counter += 1
        # Limits the number of explorations to 250.000 explorations.
        if self._exploration_counte == 250000 and self._action == 'explore':
            self.set_action_utilize()
        while self._parking:
            # Decides to utilize the filled q-table oder explore and fill the q-table.
            # Uses q-table to find a way to park.
            if self._action == 'utilize':
                [action_direction, action_lenght] = np.unravel_index(self._qtable[self._state['rho'], self._state['phi'], self._state['orientation']].argmax(
                ), np.unravel_index(self._qtable[self._state['rho'], self._state['phi'], self._state['orientation']].shape))
                is_in_range = self.action(action_direction, action_lenght)
                # Stays in the parking lot for 30 seconds, after a succesfully parking manover.
                if self.check_location():
                    self._sparking = False
                    time.sleep(30)
            # Fills q-Table.
            if self._action == 'explore':
                direction = round(random.randint(-10, 11)/10, 1)
                length = 0
                while length == 0:
                    length = random.randint(-10, 11)
                ''' Add q-function to calculate the reward for the robot '''
                self._qtable[self._state['rho'], self._state['phi'], self._state['orientation']][direction, length] = (1 - self._aplha) * (
                    self._qtable[self._state['rho'], self._state['phi'], self._state['orientation']][direction, length]) + self._aplha * (self._r_t + y * max(self._qtable[new_rho, new_phi, new_orientation]))
                is_in_range = self.action(direction, length)
            # Aborts parking, if the robot is to far away from the parking lot.
            if is_in_range:
                self._sparking = False
        self.end_parking()
