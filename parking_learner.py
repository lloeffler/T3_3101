import time
import random

import numpy as np

from swarmrobot import SwarmRobot
from parkingdirection import Parkingdirection


class ParkingLearner:
    """
    A q-learning algorithm to learn how to park the robot.
    The q-table (qtable) is five a dimensional array, that contains the reward of all actions from all possible states.
    The state is a dictionary, that contains the radius rho, tha angle phi and the orientation of the robot. Phi and orientation have the unit degree.
    The state describes the relative position of the robot to the parking lot (entrance).
    The robot is parking when self._parking is True.
    The robot can explore the possibiliteies how it can park and fill its q-table or it can utilize the filled q-table to execute the learned actions to park mostly efficient.
    Alpha is the exploration rate.
    y is the other exploration rate.
    The parkingdirection is the direction of parking the robot, either FORAWARD or BACKWARD. The Value of the orientation ist the angle in the parking position.
    The turnings radius for all allowed steer angles are fix values stored in the array self._turning_radius.
    The exploration coutner limits the number of explorations to 250.000 explorations.
    """

    def __init__(self, bot: SwarmRobot, qtable: np.ndarray = None, alpha: float = 1, y: float = 0.95, parkingdirection: Parkingdirection = Parkingdirection.FORWARD):
        """
        Creates a new instance of a parking learner.

        Parameters
        ----------
        bot: botlib.bot
            A instance of the robot.
        qtable: numpy.ndarray
            A three demensional numpy.ndarray with shape=(60, 36, 36), containing two dimensional numpy.ndarray with shape=(9, 20).
        alpha: float 
            The exploration rate.
        y: float 
            The other expploration rate.
        parkingdirection: Parkingdirection
            The direction of parking the robot, either FORAWARD or BACKWARD.
        """
        self._bot = bot
        self._qtable = qtable or np.ndarray(
            shape=(60, 36, 36), dtype=np.ndarray)
        self._state = {
            'rho': 0,
            'phi': 0,
            'orientation': 0
        }
        self._parking = False
        self._action = 'utilize' if qtable else 'explore'
        self._alpha = alpha
        self._y = y
        self._parking_direction = parkingdirection
        if not qtable:
            for q in self._qtable:
                q = np.ndarray(shape=(9, 20), dtype=float)
        self._exploration_counter = 0
        self._turning_radius = [0, 1, 2, 3]

    def change_parking_direction(self, new_parking_direction: Parkingdirection = Parkingdirection.FORWARD, new_qtable: np.ndarray = None) -> np.ndarray:
        """
        Changes parking direction of the robot and sets a new q-table.

        Parameters
        ----------
        new_parking_direction: Parkingdirection
            The new parking direction.
        new_qtable: np.ndarray(shape=(60, 36, 36))
            The new 3 dimensional q-table filled, with 2 dimensional np.ndarray(shape=(9, 20), dtype=float) filled with floats.

        Returns
        -------
        np.ndarray(60, 36, 36), dtype=np.ndarray(shape=(9, 20), dtype=float)): The previous q-table.
        """
        old_q_table = self._qtable
        self._parking_direction = new_parking_direction
        self._qtable = new_qtable or np.ndarray(
            shape=(60, 36, 36), dtype=np.ndarray)
        if not new_qtable:
            for q in self._qtable:
                q = np.ndarray(shape=(9, 20), dtype=float)
        return old_q_table

    def cart2pol(self, x: float, y: float):
        """
        Converts cartesian coordinates into polar coordinates.

        Parameters
        ----------
        x: int
            Distance between point and y-axis.
        y: int
            Distance between point and x-axis.

        Returns
        ------
        tuple : rho and phi in radians of given point.
        """
        rho = np.sqrt(x**2 + y**2)
        phi = np.arctan2(y, x)
        return (rho, phi)

    def pol2cart(self, rho: float, phi: float):
        """
        Converts polar coordinates into cartesian coordinates.

        Parameters
        ----------
        rho: float 
            Radius of the point in the unitary circle.
        phi: float 
            Angle of phi of the point in the unitary circle in radians.

        Returns
        ------
        tuple: x and y of given point.
        """
        x = rho * np.cos(phi)
        y = rho * np.sin(phi)
        return (x, y)

    def set_action_utilize(self):
        """
        Sets self._action to 'utilize', to change behavior.
        """
        self._action = 'utilize'

    def set_action_utilize(self, exploration_counter=0):
        """
        Sets self._action to 'explore', to change behavior and resets self._exploration_counter.

        Parameters
        ----------
        exploration_counter: int
            The new exploration counter to be set, by default 0, to reset exploration counter.
            If greater or eqals 250.000, self._action will not set to 'utilize' automaticly.
        """
        self._action = 'explore'
        self._exploration_counter = exploration_counter

    def update_state(self, direction: float, lenght: int) -> bool:
        """
        Calculates and sets new realtive position to parking lot as state.

        Parameters
        ----------
        direction: float 
            Steering impact from -1 to +1 in 0.1 steps.
        length: int
            How long the robot wil drive in cm.

        Returns
        -------
        boolean : True if the robot is less equals 60 cm from the parking lot away.
        """
        [x, y] = self.pol2cart(
            self._state['rho'], np.deg2rad(self._state['phi']))
        if direction == 0:
            # Robot drives straight forward.
            [delta_x, delta_y] = self.pol2cart(
                lenght, np.deg2rad(self._state['orientation']))
            x_t = x + delta_x
            y_t = y + delta_y
            orientation_t = self._state['orientation']
        else:
            # Robot drives a curve.
            # Calculating centre of rotation (x_m, y_m) of the turning circle.
            [x_m_delta, y_m_delta] = self.pol2cart(self._turning_radius[abs(direction)], np.deg2rad(self._state['orientation']) + (
                1.5 * np.pi)) if direction > 0 else self.pol2cart(self._turning_radius[abs(direction)], np.deg2rad(self._state['orientation']) + (0.5 * np.pi))
            x_m = x + x_m_delta
            y_m = y + y_m_delta
            # Calculating perimeter of the turningcicle.
            turning_perimeter = 2 * np.pi * \
                self._turning_radius[abs(direction)]
            turning_radiant = 2 * np.pi * (-lenght/turning_perimeter)
            # Calculating new robot coordinates.
            [x_delta_t, y_delta_t] = self.pol2cart(self._turning_radius[abs(
                direction)], (np.deg2rad(self._state['orientation']) + np.pi + turning_radiant))
            # Calculates new robot orientation
            orientation_t = np.deg2rad(
                self._state['orientation']) + turning_radiant
            x_t = x_m + x_delta_t
            y_t = y_m + y_delta_t
        # Sets new position as robot state.
        [rho_t, phi_t] = self.cart2pol(x_t, y_t)
        self._state['rho'] = rho_t
        self._state['phi'] = np.rint(np.rad2deg(phi_t)/10)
        self._state['orientation'] = np.rint(np.rad2deg(orientation_t)/10)
        return rho_t <= 60

    def action(self, direction: float, length: int) -> bool:
        """
        Moves Robot and calculate its new position relative to the parking lot.

        Parameters
        ----------
        direction: float 
            Steering impact from -1 to +1 in 0.1 steps.
        length: int
            How long the robot wil drive in cm.

        Returns
        -------
        boolean: True if the robot is less equals 60 cm from the parking lot away.
        """
        self._bot.drive_steer(direction)
        time.sleep(0.5)
        self._bot.drive_power(20) if length > 0 else self._bot.drive_power(-20)
        time.sleep(abs(length))
        self._bot.drive_power(0)
        return self.update_state(direction=direction, lenght=length)

    def start_parking(self, distance: int = 15, angle: int = 0, orientation: int = 18):
        """
        Pauses line detection and starts parking process.

        Parameters
        ----------
        distance: int = 15
            The distance between the robot and the parking lot. By default 15 cm.
        angle: int = 0
            The angle phi of the robot relativ to the parking lot entrance. By defautl 0 degree.
        orientation: int = 18
            The angle, that describes in what direction the front of the robot is, relativ to the parking lot entrance. By default 180 degrees saved as 18.
        """
        # Stop pause line detection and following the line
        self._bot.linetracker._autopilot(False)
        self._bot.stop_all()
        self._bot.drive_steer(0)
        self._parking = True
        self.parking(distance, angle, orientation)

    def end_parking(self):
        """
        Resets the state, aka. the relativ position, to 0.
        Sets parking to false, to leave while loop from self.parking();
        """
        self._state['rho'] = 0
        self._state['phi'] = 0
        self._state['orientation'] = 0
        ''' return to line deetection and following the line '''
        self._bot.linetracker._autopilot(True)

    def check_location(self) -> bool:
        """
        Checks if the right parking position is reached.
        return bool: true if calculated pisition is correct, proofed by optical detection.
        """
        calculated = (self._state['rho'] ==
                      0 and self._state['orientation'] == 0)
        ''' somthing with opencv, check if parking lot entrance is in lower x% and in the middle of the picture.
         if actual position and calculated position not true, recalculate current position, based on seen parking lot position. '''
        return calculated

    def get_reward(self) -> float:
        """
        Calculates reward of the current state and action combination.

        Returns
        -------
        float: The reward of the current action.
            +100.0: If the robot is parked.
            +/-0.0: If the robot is neither parked or leaving the parking area.
            -100.0: If the robot is leaving the parking area.
        """
        reward = 0.0
        if (self._state['rho'] == 0 and self._state['orientation'] == self._parking_direction.value):
            reward = 100.0
        if (self._state['rho'] > 60):
            reward = -100.0
        return reward

    def parking(self, distance: float, angle: float, orientation: float):
        """
        Parks the robot automaticly.
        If the action is set to 'utilize', the robot will use the filled q-table to find the best steps to park.
        If the action is set to 'explore', the robot will try some random actions to find a way to park and fill the q-table.

        Parameters
        ----------
        distance: float
            The distance between the robot and tha parking lot in cm.
        angle: float
            The angle how much the parking lot is left or right from the robot in rad.
        orientation: float
            How much the robot is turned relativ to the parking lot in rad.
        """
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
                    self._parking = False
                    time.sleep(10)
            # Fills q-Table.
            if self._action == 'explore':
                direction = round(random.randint(-10, 11)/10, 1)
                length = 0
                while length == 0:
                    length = random.randint(-10, 11)
                old_state = {
                    'rho': self._state['rho'],
                    'phi': self._state['phi'],
                    'orientation': self._state['orientation']
                }
                is_in_range = self.action(direction, length)
                self._qtable[self._state['rho'], self._state['phi'], self._state['orientation']][direction, length] = (1 - self._aplha) * self._qtable([old_state['rho'], old_state['phi'], old_state['orientation']], [
                    direction, length]) + self._aplha * (self.reward([old_state['rho'], old_state['phi'], old_state['orientation']], [direction, length]) + self._y * max(self._qtable[self._state['rho'], self._state['phi'], self._state['orientation']]))
            # Aborts parking, if the robot is to far away from the parking lot.
            if is_in_range:
                self._parking = False
        self.end_parking()
