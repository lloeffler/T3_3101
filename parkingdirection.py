from enum import Enum

class Parkindirection(Enum):
    """
    Enumeration to specify, in what direction the robot has to be parked.
    The values correspond to the orientation angel of the robot in the parking position, 
    in degree and devided by 10.
    """
    FORWARD = 18
    BACKWARD = 0
