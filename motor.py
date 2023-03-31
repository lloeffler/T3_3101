from time import sleep

from brickpi3 import BrickPi3


class Motor:
    _bp = BrickPi3()
    STATUS_POWER = 1

    def __init__(self, port):
        self._port = port
        self._default_power_limit = 85
        self._power_limit = 0

        self.limit(power_limit=self._default_power_limit)

    def status(self):
        return self._bp.get_motor_status(self._port)
    
    def limit(self, power_limit: int = 0):
        """
        Limits the powere of the motor.

        Parameter
        ---------
        power_limit: int = 0
            The motor will be limited at the power limit in percent, by default 0.
            A powerlimit of 0 will unset the powere limit, it is set to 100 percent.
        """
        self._bp.set_motor_limits(self._port, power=power_limit)
        self._power_limit = power_limit

    def get_power_limit(self) -> int:
        """
        Returns the current power limit of this motor.
        """
        return self._power_limit

    def change_power(self, pnew):
        import math

        if 100 < abs(pnew):
            return

        STEP_SIZE = 25.0
        pcur = self.status()[self.STATUS_POWER]
        # delta < 0: slow down; 0 < delta: accelerate
        delta = pnew - pcur
        steps = math.ceil(abs(delta)/STEP_SIZE)

        if steps == 0:
            return

        inc = delta/float(steps)

        for _ in range(steps):
            pcur += inc
            self._bp.set_motor_power(self._port, pcur)
            sleep(0.25)
        self._bp.set_motor_power(self._port, pnew)

    def set_power(self, pnew):
        if 100 < abs(pnew):
            return

        self._bp.set_motor_power(self._port, pnew)

    def stop(self):
        self.set_power(0)

    def rotate_motor(self, degree):
        """
        Rotates the motor.
        A degree of 30 is equals to 1 cm.
        """
        self._bp.set_motor_position_relative(self._port, degree)


class CalibratedMotor(Motor):
    def __init__(self, port, pmin=None, pmax=None, calpow=20):
        super().__init__(port)

        # calibration power
        self._calpow = calpow
        # minimum position
        self._pmin = pmin
        # maximum position
        self._pmax = pmax

        # if min and max were given, calculate initial position
        if self._pmin and self._pmax:
            self._pinit = (self._pmax + self._pmin) * 0.5
        else:
            # initial position for this motor. will be determined in `calibrate`
            self._pinit = None

    def calibrate(self, verbose=False):
        CALIBRATE_SLEEP = 0.75

        if verbose:
            print('Moving to pmin')
        self.set_power(-self._calpow)
        encprev, encnow = 0, None
        while encprev != encnow:
            encprev = encnow
            sleep(CALIBRATE_SLEEP)
            encnow = self._bp.get_motor_encoder(self._port)
        self._pmin = encnow
        self.set_power(0)
        if verbose:
            print('pmin = {}', self._pmin)

        if verbose:
            print('Moving to pmax')
        self.set_power(self._calpow)
        encprev, encnow = 0, None
        while encprev != encnow:
            encprev = encnow
            sleep(CALIBRATE_SLEEP)
            encnow = self._bp.get_motor_encoder(self._port)
        self._pmax = encnow
        self.set_power(0)
        if verbose:
            print('pmax = {}', self._pmax)

        if self._pmax == self._pmin:
            raise Exception('motor {} does not move'.format(self._port))

        self._pinit = (self._pmax + self._pmin) * 0.5
        if verbose:
            print('pinit = {}', self._pinit)
        sleep(0.5)
        self.to_init_position()

    def calibrate_offset(self, offset, verbose=False):
        CALIBRATE_SLEEP = 0.75

        if verbose:
            print('Moving to pmin')
        self.set_power(-self._calpow)
        encprev, encnow = 0, None
        while encprev != encnow:
            encprev = encnow
            sleep(CALIBRATE_SLEEP)
            encnow = self._bp.get_motor_encoder(self._port)
        self._pmin = encnow
        self.set_power(0)
        if verbose:
            print('pmin = {}', self._pmin)
        self._pmax = self._pmin + offset
        if verbose:
            print('pmax = {}', self._pmax)

        self._pinit = (self._pmax + self._pmin) * 0.5
        if verbose:
            print('pinit = {}', self._pinit)
        sleep(0.5)
        self.to_init_position()

    def set_position(self, pnew):
        if (self._pmin and self._pmax) and not (self._pmin <= pnew <= self._pmax):
            raise Exception('position ({} < {} < {}) is invalid for motor {}'.format(
                self._pmin, pnew, self._pmax, self._port))
        self._bp.set_motor_position(self._port, pnew)

    def to_init_position(self):
        if self._pinit == None:
            raise Exception(
                'initial position for motor {} not known'.format(self._port))
        self.set_position(self._pinit)

    def position_from_factor(self, factor):
        assert self._pinit and self._pmin and self._pmax
        if 0 == factor:
            return self._pinit
        if 0 < factor:
            return self._pinit + (self._pmax - self._pinit) * factor
        return self._pinit - (self._pinit - self._pmin) * abs(factor)
