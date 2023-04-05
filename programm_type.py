from enum import Enum


class ProgrammType(Enum):
    """
    Enumeration to specify, what programm runs the robot.
    """
    AUTOMATIC = 00  # Default behavior.
    DONE = 99  # Exits main programm.
    PARKING = 10  # Follows the black line and starts reinforced parking.
    ENDPARKING = 1099  # Signals end of praking programm.

# Original Author: Lukas Loeffler
