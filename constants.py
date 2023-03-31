"""
Constant values for controlling the swarmrobot or simulator.
"""
# How much percent of the power, the drive motor uses to drive.
# When chaning this value, you need to adjust the DRIVE_SLEEP_TIME!
DRIVE_POWER_LIMIT = 30
# Time the robot program sleeps, while the robot drives.
# When chaning this value, you need to adjust the DRIVE_POWER_LIMIT or the robot could pause the programm execution or skip some movement(s).
DRIVE_SLEEP_TIME = 0.1
# Time the robot program sleeps, while a the robot turns.
TURN_SLEEP_TIME = 0.3
# The a
DISPLAY_CONFIRMATION_SLEEP_TIME = 2
# The time the robot parks in the parking lot.
PARKING_TIME = 10
# Rotation degree per centi meter (cm).
# If changing the tire size, adjust the DEGREE_PER_CM!
DEGREE_PER_CM = 30

# How many times the simulator tries random actions to learn and fill the q table.
NUMBER_OF_SIMULATIONS = 1000000
