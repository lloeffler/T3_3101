from motor import Motor
import threading

import time

class TurnAssistant:
    def __init__(self, bot):
        self._bot = bot
        
        self._full_rotation_deg = 510
        
    #direction 1 = links -1 = rechts
    def turn_90_deg(self, direction):
        time.sleep(0.5)
        self._bot.set_drive_steer(-1.0*direction)
        time.sleep(0.5)
        self._bot._drive_motor.rotate_motor(1.2*self._full_rotation_deg)
        time.sleep(0.5)
        self._bot.set_drive_steer(1.0*direction)
        time.sleep(0.5)
        self._bot._drive_motor.rotate_motor(-1*self._full_rotation_deg)
        time.sleep(0.5)
        self._bot.set_drive_steer(-0.3*direction)
        time.sleep(0.5)
        self._bot._drive_motor.rotate_motor(1.2*self._full_rotation_deg)
        time.sleep(0.5)
        self._bot.set_drive_steer(0)
        
    def turn_180_deg(self):
        self._bot.set_drive_steer(1.0)
        self._bot._drive_motor.rotate_motor(-1.3*self._full_rotation_deg)
        time.sleep(1)
        self._bot.set_drive_steer(-1.0)
        self._bot._drive_motor.rotate_motor(1.3*self._full_rotation_deg)
        time.sleep(1)
        self._bot.set_drive_steer(1.0)
        self._bot._drive_motor.rotate_motor(-1.3*self._full_rotation_deg)
        time.sleep(1)
        self._bot.set_drive_steer(-1.0)
        self._bot._drive_motor.rotate_motor(1.4*self._full_rotation_deg)
        time.sleep(1)
        self._bot.set_drive_steer(0)
        
    def turn_180_deg_on_spot(self):
        self._bot.set_drive_steer(1.0)
        time.sleep(0.5)
        self._bot._drive_motor.rotate_motor(-0.6*self._full_rotation_deg)
        time.sleep(0.5)
        self._bot.set_drive_steer(-1.0)
        time.sleep(0.5)
        self._bot._drive_motor.rotate_motor(0.7*self._full_rotation_deg)
        time.sleep(0.5)
        self._bot.set_drive_steer(1.0)
        time.sleep(0.5)
        self._bot._drive_motor.rotate_motor(-0.6*self._full_rotation_deg)
        time.sleep(0.5)
        self._bot.set_drive_steer(-1.0)
        time.sleep(0.5)
        self._bot._drive_motor.rotate_motor(0.8*self._full_rotation_deg)
        time.sleep(0.5)
        self._bot.set_drive_steer(1.0)
        time.sleep(0.5)
        self._bot._drive_motor.rotate_motor(-0.6*self._full_rotation_deg)
        time.sleep(0.5)
        self._bot.set_drive_steer(-1.0)
        time.sleep(0.5)
        self._bot._drive_motor.rotate_motor(0.8*self._full_rotation_deg)
        time.sleep(0.5)
        self._bot.set_drive_steer(1.0)
        time.sleep(0.5)
        self._bot._drive_motor.rotate_motor(-0.6*self._full_rotation_deg)
        self._bot.set_drive_steer(0)
        
    def park_backwards(self):
        self.turn_180_deg_on_spot()
        time.sleep(0.5)
        self._bot.set_drive_steer(0)
        time.sleep(0.5)
        self._bot._drive_motor.rotate_motor(-1.0*self._full_rotation_deg)
        time.sleep(0.5)
        self._bot._drive_motor.rotate_motor(-0.1*self._full_rotation_deg)
        
    def turn_0_deg(self):
        time.sleep(0.5)
        self._bot.set_drive_steer(0)
        time.sleep(0.5)
        self._bot._drive_motor.rotate_motor(1.1*self._full_rotation_deg)
        time.sleep(0.5)
        self._bot._drive_motor.rotate_motor(0.1*self._full_rotation_deg)