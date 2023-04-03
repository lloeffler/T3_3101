"""
Constant values for controlling the swarmrobot, exhibition and simulator.
"""

# region robot_drive_constants

DRIVE_POWER_LIMIT = int(30)
"""
int:
How much percent of the power, the drive motor uses to drive.

When chaning this value, you need to adjust the DRIVE_SLEEP_TIME!
"""

DRIVE_SLEEP_TIME = 0.1
"""
float:
Time the robot program sleeps, while the robot drives.

When chaning this value, you need to adjust the DRIVE_POWER_LIMIT or the robot could pause the programm execution or skip some movement(s).
"""

TURN_SLEEP_TIME = 0.3
"""
float:
Time the robot program sleeps, while a the robot turns.
"""

DEGREE_PER_CM = int(30)
"""
int:
Rotation degree per centi meter (cm).

If changing the tire size, adjust the DEGREE_PER_CM!
"""

TURNING_RADIUS_50 = 68.0
"""
float:
The turning radius at steering impact of 50 percent in centi meter (cm).
"""

TURNING_RADIUS_100 = 37.0
"""
float:
The turning radius at steering impact of 100 percent in centi meter (cm).
"""

TURNING_DIRECTIONS = [-1.0, -0.5, 0.0, 0.5, 1.0]
"""
list[float]:
List of turning directions.
Contains 2 times the number of TURN_RADIUS_XX to drive left and right plus one direction to drive straight forward or backward.
"""

# endregion robot_drive_constants

# region parking

PARKING_TIME = 10.0
"""
float:
The time the robot parks in the parking lot in seconds.
"""

# Because of the much movement in the mechanics and gears, the rho value has to be less than 20.
FORWARD_PARKING_RHO = 20.0
"""
float:
The distance between the front of the robot in the parking position and the parking entrance in centimeter (cm), when parking forward.
Part of polarcoordinates of the state/position of the robot.

In reality 24 cm.
"""

FORWARD_PARKING_PHI = 18.0
"""
float:
Angle of the distance of the parking position, when parking forward.
Part of polarcoordinates of the state/position of the robot.
"""

FORWARD_PARKING_ORIENTATION = 18.0
"""
float:
Angle of the robot in parking position, when parking forward.
Part of polarcoordinates of the state/position of the robot.
"""

BACKWARD_PARKING_RHO = 0.0
"""
float:
The distance between the front of the robot in the parking position and the parking entrance in centimeter (cm), when parking backward.
Part of polarcoordinates of the state/position of the robot.
"""

BACKWARD_PARKING_ORIENTATION = 0.0
"""
float:
Angle of the robot in parking position, when parking backward.
Part of polarcoordinates of the state/position of the robot.
"""

MAXIMAL_DISTANCE_TO_PARKING_LOT = 60.0
"""
float:
The maximal distance between the parking lot entrance and the robot in centimeter (cm), while parking.
When the Robot is further away, the parking will be aborted.
"""

# endregion parking

# region display_time

DISPLAY_CONFIRMATION_SLEEP_TIME = 2.0
"""
float:
The time a confirmation will be shown.
"""

# endregion display_time

# region exhibition

# Because of the much movement in the mechanics and gears, the distance has to be less than 15.
START_DISTANCE = int(13)
"""
int:
The distance the robot drives forward at the beginning of the programm for the exhibition in centimeter (cm).
The robot should drive about 15 cm and then start the parking progress.
"""

# Because of the much movement in the mechanics and gears, the distance has to be less than 54.
END_DISTANCE_FORWARD = int(48)
"""
int:
The distance the robot drives back to the starting position in centimeter (cm), when parking forward.
The robot should drive about 54 cm back to its starting position.
"""

END_DISTANCE_BACKWARD = int(30)
"""
int:
The distance the robot drives back to the starting position in centimeter (cm), when parking backward.
The robot should drive about 30 cm back to its starting position.
"""

# endregion exhibition

# region simulator

NUMBER_OF_SIMULATIONS = int(1000000)
"""
int:
How many times the simulator tries random actions to learn and fill the q table.
"""

# endregion simulator

# region qtable
# Q-tbale saves state as polar coordinates and orientation of the robot and actions with turning direction and drive length.

SIZE_STATE_RHO = int(MAXIMAL_DISTANCE_TO_PARKING_LOT + 1)
"""
int:
Number of possible rho values in state part of q-table.
Depends on MAXIMAL_DISTANCE_TO_PARKING_LOT.
"""

SIZE_STATE_PHI = int(36)
"""
int:
Number of possible phi values in state part of q-table.
360 degree of a full circle devided by 10 to reduce the ram usage.
"""

SIZE_STATE_ORIENTATION = int(36)
"""
int:
Number of possible orientation values in state part of q-table.
360 degree of a full circle devided by 10 to reduce the ram usage.
"""

SIZE_ACTION_DIRECTION = len(TURNING_DIRECTIONS)
"""
int:
Number of possible turning direction values in action part of q-table.
2 times the number of TURN_RADIUS_XX in robot_drive_constants region plus one direction to drive straight forward or backward.
Depends on TURNING_DIRECTIONS.
"""

SIZE_ACTION_LENTGH = int(20)
"""
int:
Number of possible drive length values in action part of q-table.

IMPORTANT:
Need to be a even number!
"""

BACKWARD_ACTION_LENGTH_SUBTRAHEND = int(SIZE_ACTION_LENTGH / 2)
"""
int:
Based on SIZE_ACTION_LENTGH subtrahend for index to length conversion to drive backward.

Please don't change.
"""

FORWARD_ACTION_LENGTH_SUBTRAHEND = BACKWARD_ACTION_LENGTH_SUBTRAHEND - 1
"""
int:
Based on SIZE_ACTION_LENTGH subtrahend for index to length conversion to drive forward.

Please don't change.
"""

MAXIMAL_RANDOM_ACTION_DIRECTION = SIZE_ACTION_DIRECTION - 1
"""
int:
Maximal possible direction index used to explore.
Depends on SIZE_ACTION_DIRECTION.

Please don't change.
"""

MAXIMAL_RANDOM_ACTION_LENGTH = SIZE_ACTION_LENTGH - 1
"""
int:
Maximal possible length index used to explore.
Depends on SIZE_ACTION_LENTGH.

Please don't change.
"""

# endregion qtable
