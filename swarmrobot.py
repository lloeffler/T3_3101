from motor import CalibratedMotor, Motor
from pidcontroller import PIDController
from line_tracking import LineTracker
from programm_type import ProgrammType
from threading import Thread, Event
import cv2

class SwarmRobot:
    def __init__(self, programm_type: ProgrammType = ProgrammType.AUTOMATIC):
        self._drive_motor = Motor(Motor._bp.PORT_B)
        self._steer_motor = CalibratedMotor(Motor._bp.PORT_D, calpow=40)
        self._fork_lift_motor = CalibratedMotor(Motor._bp.PORT_C, calpow=50)
        self._fork_tilt_motor = CalibratedMotor(Motor._bp.PORT_A, calpow=40)

        # Camera
        self._camera = cv2.VideoCapture(0)
        
        self._event = Event()
        
        self.goal = '1'
        self.steer = 0
        self.full_rotation_deg = 510
        self.last_line_tracking = 0
        self.power_lvl = 0

        # Linetracking
        self._track_process = None
        self._track_active = False
        self._pid_controller = PIDController(verbose=False)
        self._line_tracker = LineTracker(self._camera.get(cv2.CAP_PROP_FRAME_WIDTH), self._camera.get(cv2.CAP_PROP_FRAME_HEIGHT), preview=False, debug=False)

        # Navigation
        self._programm_type = programm_type
        self._navigation_process = None
        self._navigation_active = False
        self._navigator = None
        
        # Intersection detection
        self._intsecdet_process = None
        self._intsecdet_active = False
        self._intersection_detector = None
        self.intersection = []
        
    def __del__(self):
        self._steer_motor.to_init_position()
        self.stop_all()

    def change_drive_power(self, pnew):
        self._drive_motor.change_power(pnew)

    def set_drive_power(self, pnew):
        self._drive_motor.set_power(pnew)

    def set_drive_steer(self, pnew):
        pos = self._steer_motor.position_from_factor(pnew)
        self._steer_motor.set_position(pos)
    
    def set_programm_type(self, programmtype: ProgrammType):
        """
        Sets new programmtype.

        Parameter
        ----------
        programmtype: ProgrammType
            The new programm type, defines what programm the robot executes.
        """
        self._programm_type = programmtype

    def calibrate(self, calibrate_forklift=False, verbose=False):
        print('Calibrating steering')
        self._steer_motor.calibrate(verbose)
        if(calibrate_forklift):
            print('Calibrating forklift lift motor')
            self._fork_lift_motor.calibrate(verbose)
            print('Calibrating forklift tilt motor')
            self._fork_tilt_motor.calibrate_offset(53000,verbose)

    def stop_all(self):
        self._drive_motor.stop()
        self._steer_motor.stop()

    def _setup_autopilot(self):
        from time import sleep

        def follow(event):
            try:
                while True:
                    if not self._track_active:
                        sleep(0.5)

                    if self._track_active:
                        _,frame = self._camera.read()
                        if frame is not None:
                            pos = self._line_tracker.track_line(frame, event, self)
                            self.last_line_tracking = pos
                            if pos != None:
                                self.steer = self._pid_controller.pid(pos)
                                self.set_drive_steer(self.steer)
            except KeyboardInterrupt:
                self.stop_all()
            finally:
                self.stop_all()

        self._track_process = Thread(group=None, target=follow, daemon=True, args=(self._event,))
        self._track_process.start()

    def get_autopilot_state(self):
        return self._track_active

    def set_autopilot_state(self, active:bool):
        self._track_active = active
        if(active and self._track_process == None):
            self._setup_autopilot()

    def _setup_classifier(self):
        from .classifier import Classifier
        
    def _setup_navigation(self):
        from time import sleep
        from navigation import Navigator

        if self._navigator == None:
            self._navigator = Navigator(self._camera.get(cv2.CAP_PROP_FRAME_WIDTH), self._camera.get(cv2.CAP_PROP_FRAME_HEIGHT), self, preview=True, debug=False)
        
        def navigate(event):
            try:
                while True:
                    if not self._navigation_active:
                        sleep(5)
                        
                    if self._navigation_active:
                        _,frame = self._camera.read()
                        if frame is not None:
                            self._navigator.navigate(frame, event)
            except KeyboardInterrupt:
                self.stop_all()
            finally:
                self.stop_all()
        
        self._navigation_process = Thread(group=None, target=navigate, daemon=True, args=(self._event,))
        self._navigation_process.start()
    
    def set_navigaton_state(self, active:bool):
        self._navigation_active = active
        if(active and self._navigation_process == None):
            self._setup_navigation()
            
    def _setup_intersection_detection(self):
        from time import sleep
        from intersection_detection import IntersectionDetection

        if self._intersection_detector == None:
            self._intersection_detector = IntersectionDetection(self._camera.get(cv2.CAP_PROP_FRAME_WIDTH), self._camera.get(cv2.CAP_PROP_FRAME_HEIGHT), self, preview=True, debug=False)
        
        def detect_intersection():
            try:
                while True:
                    if not self._intsecdet_active:
                        sleep(5)
                        
                    if self._intsecdet_active:
                        _,frame = self._camera.read()
                        if frame is not None:
                            self._intersection_detector.detect_intersection(frame)
            except KeyboardInterrupt:
                self.stop_all()
            finally:
                self.stop_all()
        
        self._intsecdet_process = Thread(group=None, target=detect_intersection, daemon=True)
        self._intsecdet_process.start()
    
    def set_intsecdet_state(self, active:bool):
        self._intsecdet_active = active
        if(active and self._intsecdet_process == None):
            self._setup_intersection_detection()
            
    def set_goal(self, goal):
        self.goal = goal
        
    def set_power_lvl(self, lvl):
        self.power_lvl = lvl