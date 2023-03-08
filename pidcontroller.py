import math

class PIDController:
    # PID constants
    kp = 1
    ki = 0.01
    kd = 0.2

    lastError = 0
    totalError = 0
    lastValue = 0

    centerpoint = 0

    def __init__(self, verbose = False):
        self._verbose = verbose

    def pid(self, value: int) -> float:
        error = value - self.centerpoint
        self.totalError += error

        proportional = error * self.kp
        integral = self.totalError * self.ki
        derivative = (error - self.lastError) * self.kd

        pidReturn = proportional + integral + derivative

        # set lastError and totalError to 0 when value passes centerpoint
        if ((self.lastValue > self.centerpoint and value < self.centerpoint) or (
                self.lastValue < self.centerpoint and value > self.centerpoint)):
            self.lastError = 0
            self.totalError = 0

        if (error == 0):
            self.totalError = 0
        if (self.totalError > 50):
            self.totalError = 50
        if (self.totalError < -50):
            self.totalError = -50
        if (pidReturn > 1):
            pidReturn = 1
        if (pidReturn < -1):
            pidReturn = -1

        if(self._verbose):
            print("value: " + str(value) + " | error: " + str(error) + " | lastError: " + str(
                self.lastError) + " | totalError: " + str(self.totalError))
            print("PID: " + str(pidReturn) + " | P: " + str(proportional) + " | I: " + str(integral) + " | D: " + str(
                derivative))
            print("---------------------------------------------")

        self.lastError = error
        self.lastValue = value
        return pidReturn