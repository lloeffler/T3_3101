import random

from time import sleep

import numpy as np

from swarmrobot import SwarmRobot
from parkingdirection import Parkingdirection
from programm_type import ProgrammType

from constants import TURN_SLEEP_TIME, TURNING_RADIUS_50, TURNING_RADIUS_100, TURNING_DIRECTIONS, PARKING_TIME, FORWARD_PARKING_RHO, FORWARD_PARKING_PHI, FORWARD_PARKING_ORIENTATION, BACKWARD_PARKING_RHO, BACKWARD_PARKING_ORIENTATION, MAXIMAL_DISTANCE_TO_PARKING_LOT, SIZE_STATE_RHO, SIZE_STATE_PHI, SIZE_STATE_ORIENTATION, SIZE_ACTION_DIRECTION, SIZE_ACTION_LENTGH, BACKWARD_ACTION_LENGTH_SUBTRAHEND, FORWARD_ACTION_LENGTH_SUBTRAHEND, MAXIMAL_RANDOM_ACTION_DIRECTION, MAXIMAL_RANDOM_ACTION_LENGTH


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
    The exploration coutner limits the number of explorations to 250.000 explorations.
    The turnings radius for all allowed steer angles are fix values stored in the array self._turning_radius.
    The parking position contains the state of the right parking position, for all parking directions.
    """

    def __init__(self, bot: SwarmRobot, qtable: np.ndarray = None, alpha: float = 1, y: float = 0.95, parkingdirection: Parkingdirection = Parkingdirection.FORWARD, action: str = 'explore'):
        """
        Creates a new instance of a parking learner.

        Parameter
        ----------
        bot: SwarmRobot
            A instance of the robot.
        qtable: numpy.ndarray
            A five demensional numpy.ndarray with shape=(61, 36, 36, 5, 20), containing the q value of the state and action pairs.
            The fisrt three indices represent the state and the last two indices represent the possible actions(direction and length).
        alpha: float
            The exploration rate.
        y: float
            The other expploration rate.
        parkingdirection: Parkingdirection
            The direction of parking the robot, either FORAWARD or BACKWARD.
        action: str
            The action to even 'explore' or 'utilize' at pakring, 
        """
        qtable_is_numpy_array = qtable.__class__ == np.ndarray
        self._bot = bot
        self._qtable = qtable if qtable_is_numpy_array else np.zeros(
            shape=(SIZE_STATE_RHO, SIZE_STATE_PHI, SIZE_STATE_ORIENTATION, SIZE_ACTION_DIRECTION, SIZE_ACTION_LENTGH))
        self._state = {
            'rho': 0,
            'phi': 0,
            'orientation': 0
        }
        self._parking = False
        self._action = action
        self._alpha = alpha
        self._y = y
        self._parking_direction = parkingdirection
        self._exploration_counter = 0
        # Turning radia  for 0.5 and 1.0 steering.
        self._turning_radius = [TURNING_RADIUS_50, TURNING_RADIUS_100]
        self._parking_position = {
            'FORWARD': {
                'rho': FORWARD_PARKING_RHO,
                'phi': FORWARD_PARKING_PHI,
                'orientation': FORWARD_PARKING_ORIENTATION
            },
            'BACKWARD': {
                'rho': BACKWARD_PARKING_RHO,
                'orientation': BACKWARD_PARKING_ORIENTATION
            }
        }

    def change_parking_direction(self, new_parking_direction: Parkingdirection = Parkingdirection.FORWARD, new_qtable: np.ndarray = None) -> np.ndarray:
        """
        Changes parking direction of the robot and sets a new q-table.

        Parameter
        ----------
        new_parking_direction: Parkingdirection
            The new parking direction.
        new_qtable: np.ndarray(shape=(61, 36, 36, 5, 20))
            The new 5 dimensional q-table filled, filled with floats.
        """
        new_qtable_is_numpy_array = new_qtable.__class__ == np.ndarray
        self._parking_direction = new_parking_direction
        self._qtable = new_qtable if new_qtable_is_numpy_array else np.zeros(
            shape=(SIZE_STATE_RHO, SIZE_STATE_PHI, SIZE_STATE_ORIENTATION, SIZE_ACTION_DIRECTION, SIZE_ACTION_LENTGH))

    # region conversions

    def cart2pol(self, x: float, y: float):
        """
        Converts cartesian coordinates into polar coordinates.

        Parameter
        ----------
        x: float
            Distance between point and y-axis.
        y: float
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

        Parameter
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

    def index2direction(self, index: int = 2) -> float:
        """
        Converts an index of the q-sub-table to a direction float.

        Parameter
        ---------
        index: int
            The index of the q-subt-table, corresponding a direction.

        Returns
        -------
        float: The turning drirection, based on the index parameter. By default the direction is straight, so 0.0.
        """
        return TURNING_DIRECTIONS[index]

    def index2dlength(self, index: int = 10) -> int:
        """
        Converts an index of the q-sub-table to a length int.

        Parameter
        ---------
        index: int
            The index of the q-subt-table, corresponding a length.

        Returns
        -------
        int: The length the robot drives forward or backward, based on the index parameter.
        """
        return index - BACKWARD_ACTION_LENGTH_SUBTRAHEND if index < 10 else index - FORWARD_ACTION_LENGTH_SUBTRAHEND

    # endregion

    def set_action_utilize(self):
        """
        Sets self._action to 'utilize', to change behavior.
        """
        self._action = 'utilize'

    def set_action_explore(self, exploration_counter=0):
        """
        Sets self._action to 'explore', to change behavior and resets self._exploration_counter.

        Parameter
        ----------
        exploration_counter: int
            The new exploration counter to be set, by default 0, to reset exploration counter.
            If greater or eqals 250.000, self._action will not set to 'utilize' automaticly.
        """
        self._action = 'explore'
        self._exploration_counter = exploration_counter

    def update_state(self, direction_index: int, length_index: int) -> bool:
        """
        Calculates and sets new realtive position to parking lot as state.

        Parameter
        ----------
        direction_index: int 
            Index of the steering impact from 0 to 4
        length_index: int
            Index of how long the robot wil drive.

        Returns
        -------
        boolean : True if the robot is less equals 60 cm from the parking lot away.
        """
        # Converts indicies and rounded state to calculateready numbers.
        length = self.index2dlength(length_index)
        direction = self.index2direction(direction_index)
        state_rho = self._state['rho']
        rad_phi = np.deg2rad(self._state['phi'] * 10)
        rad_orientation = np.deg2rad(self._state['orientation'] * 10)
        # Calculates new State
        [x, y] = self.pol2cart(state_rho, rad_phi)
        if direction == 0.0:
            # Robot drives straight forward.
            [delta_x, delta_y] = self.pol2cart(
                length, rad_orientation)
            x_t = x + delta_x
            y_t = y + delta_y
            orientation_t = rad_orientation
        else:
            # Robot drives a curve.
            # Index of turning radius list based on direction index.
            turning_index = 1 if direction_index == 1 or direction_index == 3 else 0
            turning_radius = self._turning_radius[turning_index]
            # Calculating centre of rotation (x_m, y_m) of the turning circle.
            [x_m_delta, y_m_delta] = self.pol2cart(turning_radius, rad_orientation + (
                1.5 * np.pi)) if direction > 0 else self.pol2cart(turning_radius, rad_orientation + (0.5 * np.pi))
            x_m = x + x_m_delta
            y_m = y + y_m_delta
            # Calculating perimeter of the turningcicle.
            turning_perimeter = 2 * np.pi * turning_radius
            turning_radiant = 2 * np.pi * \
                (-self.index2dlength(length_index)/turning_perimeter)
            # Calculating new robot coordinates.
            [x_delta_t, y_delta_t] = self.pol2cart(
                self._turning_radius[turning_index], (rad_orientation + np.pi + turning_radiant))
            # Calculates new robot orientation
            orientation_t = rad_orientation + turning_radiant
            x_t = x_m + x_delta_t
            y_t = y_m + y_delta_t
        # Sets new position as robot state.
        [rho_t, phi_t] = self.cart2pol(x_t, y_t)
        self._state['rho'] = int(rho_t)
        self._state['phi'] = int(
            np.rint(np.rad2deg(phi_t)/10)) % SIZE_STATE_PHI
        self._state['orientation'] = int(
            np.rint(np.rad2deg(orientation_t)/10)) % SIZE_STATE_ORIENTATION
        return rho_t <= MAXIMAL_DISTANCE_TO_PARKING_LOT

    def action(self, direction_index: int, length_index: int) -> bool:
        """
        Moves Robot and calculate its new position relative to the parking lot.

        Parameter
        ----------
        direction_index: int 
            Index of the steering impact from 0 to 5.
        length_index: int
            Index of how long the robot wil drive.

        Returns
        -------
        boolean: True if the robot is less equals 60 cm from the parking lot away.
        """
        self._bot.set_drive_steer(self.index2direction(direction_index)) if self.index2direction(
            direction_index) != 0 else self._bot.straight()
        sleep(TURN_SLEEP_TIME)
        drive_length = self.index2dlength(length_index)
        self._bot.drive(length=drive_length)
        return self.update_state(direction_index=direction_index, length_index=length_index)

    def start_parking(self, distance: int = 15, angle: int = 0, orientation: int = 18):
        """
        Starts parking process.

        Parameter
        ----------
        distance: int = 15
            The distance between the robot and the parking lot. By default 15 cm.
        angle: int = 0
            The angle phi of the robot relativ to the parking lot entrance. By defautl 0 degree.
        orientation: int = 18
            The angle, that describes in what direction the front of the robot is, relativ to the parking lot entrance. By default 180 degrees saved as 18.
        """
        self._bot.stop_all()
        sleep(TURN_SLEEP_TIME)
        self._bot.straight()
        self._parking = True
        self.parking(distance=distance, angle=angle, orientation=orientation)

    def end_parking(self):
        """
        Resets the state, aka. the relativ position, to 0.
        Sets parking to false, to leave while loop from self.parking();
        """
        self._state['rho'] = 0
        self._state['phi'] = 0
        self._state['orientation'] = 0
        if self._bot._programm_type == ProgrammType.PARKING:
            self._bot.set_programm_type(ProgrammType.ENDPARKING)

    def check_location(self) -> bool:
        """
        Checks if the right parking position is reached.

        Returns
        -------
        bool: true if the robots position is correct.
        """
        right_rho = self._state['rho'] == self._parking_position[self._parking_direction.name]['rho']
        right_orientation = self._state['orientation'] == self._parking_position[self._parking_direction.name]['orientation']
        right_phi = False
        if self._parking_direction == Parkingdirection.FORWARD:
            right_phi = self._state['phi'] == self._parking_position[self._parking_direction.name]['phi']
        elif self._parking_direction == Parkingdirection.BACKWARD:
            right_phi = True
        return right_rho and right_phi and right_orientation

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
        if self.check_location():
            reward = 100.0
        if self._state['rho'] > MAXIMAL_DISTANCE_TO_PARKING_LOT:
            reward = -100.0
        return reward

    def parking(self, distance: float, angle: float, orientation: float):
        """
        Parks the robot automaticly.
        If the action is set to 'utilize', the robot will use the filled q-table to find the best steps to park.
        If the action is set to 'explore', the robot will try some random actions to find a way to park and fill the q-table.

        Parameter
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
        if self._exploration_counter == 250000 and self._action == 'explore':
            self.set_action_utilize()
        print(self._action)
        while self._parking:
            # Decides to utilize the filled q-table oder explore and fill the q-table.
            # Uses q-table to find a way to park.
            if self._action == 'utilize':
                state_qtable = self._qtable[int(self._state['rho']), int(
                    self._state['phi']), int(self._state['orientation'])]
                (action_direction_index, action_length_index) = np.unravel_index(
                    state_qtable.argmax(), state_qtable.shape)
                is_in_range = self.action(
                    action_direction_index, action_length_index)
            # Fills q-Table.
            if self._action == 'explore':
                action_direction_index = random.randint(
                    0, MAXIMAL_RANDOM_ACTION_DIRECTION)
                action_length_index = random.randint(
                    0, MAXIMAL_RANDOM_ACTION_LENGTH)
                old_state = {
                    'rho': self._state['rho'],
                    'phi': self._state['phi'],
                    'orientation': self._state['orientation']
                }
                is_in_range = self.action(
                    action_direction_index, action_length_index)
                old_q_s_t = self._qtable[int(old_state['rho']), int(old_state['phi']), int(
                    old_state['orientation']), action_direction_index, action_length_index]
                # Checks if state is out of range, sets possible action q table based on check.
                if self._state['rho'] <= MAXIMAL_DISTANCE_TO_PARKING_LOT:
                    possible_actions_qtable = self._qtable[int(self._state['rho']), int(
                        self._state['phi']), int(self._state['orientation'])]
                else:
                    possible_actions_qtable = [-100.0]
                # Fills q-Table.
                self._qtable[int(old_state['rho']), int(old_state['phi']), int(old_state['orientation']), action_direction_index, action_length_index] = (
                    1 - self._alpha) * old_q_s_t + self._alpha * (self.get_reward() + self._y * np.amax(possible_actions_qtable))
            # Stays in the parking lot for 30 seconds, after a succesfully parking manover.
            if self.check_location():
                self._parking = False
                sleep(PARKING_TIME)
            # Aborts parking, if the robot is to far away from the parking lot.
            if not is_in_range:
                print('Position:[rho: {0}, phi: {1}, ori: {2}]'.format(
                    self._state['rho'], self._state['phi'], self._state['orientation']))
                self._parking = False
        self.end_parking()

    # region simulation

    def simulated_check_location(self) -> bool:
        """
        Checks if the right parking position is calculated.

        Returns
        -------
        bool: true if calculated position is correct.
        """
        orientation = 18 if self._parking_direction == Parkingdirection.FORWARD else 0
        return (self._state['rho'] == 0 and self._state['orientation'] == orientation)

    def simulated_action(self, direction_index: int, length_index: int) -> bool:
        """
        Calculate its new position relative to the parking lot.

        Parameter
        ----------
        direction_index: int 
            Index of the steering impact from 0 to 5
        length_index: int
            Index of how long the robot wil drive.

        Returns
        -------
        boolean: True if the robot is less equals 60 cm from the parking lot away.
        """
        return self.update_state(direction_index=direction_index, length_index=length_index)

    def simulated_parking(self, distance: float, angle: float, orientation: float):
        """
        Simulates parking the robot.
        Behavies always like exploring.

        Parameter
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
        while self._parking:
            action_direction_index = random.randint(
                0, MAXIMAL_RANDOM_ACTION_DIRECTION)
            action_length_index = random.randint(
                0, MAXIMAL_RANDOM_ACTION_LENGTH)
            old_state = {
                'rho': self._state['rho'],
                'phi': self._state['phi'],
                'orientation': self._state['orientation']
            }
            # Simulates action
            is_in_range = self.simulated_action(
                action_direction_index, action_length_index)
            old_q_s_t = self._qtable[int(old_state['rho']), int(old_state['phi']), int(
                old_state['orientation']), action_direction_index, action_length_index]
            # Checks if state is out of range, sets possible action q table based on check.
            if self._state['rho'] <= MAXIMAL_DISTANCE_TO_PARKING_LOT:
                possible_actions_qtable = self._qtable[int(self._state['rho']), int(
                    self._state['phi']), int(self._state['orientation'])]
            else:
                possible_actions_qtable = [-100.0]
            # Fills q-Table.
            self._qtable[int(old_state['rho']), int(old_state['phi']), int(old_state['orientation']), action_direction_index, action_length_index] = (
                1 - self._alpha) * old_q_s_t + self._alpha * (self.get_reward() + self._y * np.amax(possible_actions_qtable))
            if not is_in_range:
                self._parking = False

    def simulated_start(self, distance: int = 15, angle: int = 0, orientation: int = 18):
        """
        Starts simulated parking process.

        Parameter
        ----------
        distance: int = 15
            The distance between the robot and the parking lot. By default 15 cm.
        angle: int = 0
            The angle phi of the robot relativ to the parking lot entrance. By defautl 0 degree.
        orientation: int = 18
            The angle, that describes in what direction the front of the robot is, relativ to the parking lot entrance. By default 180 degrees saved as 18.
        """
        self._parking = True
        self.simulated_parking(distance, angle, orientation)

    # endregion
