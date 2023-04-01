"""
Constant values for controlling the swarmrobot or simulator.
"""

# region robot_drive_constants

DRIVE_POWER_LIMIT = 30
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

DEGREE_PER_CM = 30
"""
int:
Rotation degree per centi meter (cm).
If changing the tire size, adjust the DEGREE_PER_CM!
"""

# endregion robot_drive_constants

# region display_time

DISPLAY_CONFIRMATION_SLEEP_TIME = 2.0
"""
float:
The time a confirmation will be shown.
"""

# endregion display_time

# region exhibition

PARKING_TIME = 10.0
"""
float:
The time the robot parks in the parking lot in seconds.
"""

# Because of the much movement in the mechanics and gears, the distance has to be less than 15.
START_DISTANCE = 13
"""
int:
The distance the robot drives forward at the beginning of the programm for the exhibition.
The robot should drive about 15 cm and then start the parking progress.
"""

END_DISTANCE_FORWARD = 54
"""
int:
The distance the robot drives back to the starting position, when parking forward.
"""

END_DISTANCE_BACKWARD = 30
"""
int:
The distance the robot drives back to the starting position, when parking backward.
"""

# endregion exhibition

# region simulator

NUMBER_OF_SIMULATIONS = 1000000
"""
int:
How many times the simulator tries random actions to learn and fill the q table.
"""

# endregion simulator
