from time import sleep

import cv2 as cv
import numpy as numpy

from constants import TURN_SLEEP_TIME


class LineTracker:
    def __init__(self, width, height, bot, method='contour', kernel_size=(5, 5), preview: bool=False, debug: bool=False):
        """
        Parameter
        ---------
        width: int
        height: int
            width and heigth describe the pixel resolution of the tracking image?
        bot: SwarmRobot
            Instance of the robot itself. Used to adjust the steering.
        method: str
            [?DEPRICATED?] Defined by previos students. I don't know what it is for, probably it could be remove.
        kernel_size: tupel
            Size of kernel for gausian blur.
        preview: bool
            WARNING only set true when using a GUI! If true, the current frame with detected lines will be displayed in a window next to the console.
        debug: bool
            WARNING only set true when using a GUI! If true, the current frame will be displayed in the single steps like black and white, blured and so on.
        """
        # Define Region of interest
        self.resolution = (int(width), int(height))
        w = self.resolution[0]//3
        h = self.resolution[1]//2
        self.roi_x1 = self.resolution[0]//2 - w//2
        self.roi_y1 = self.resolution[1] - h
        self.roi_x2 = self.roi_x1 + w
        self.roi_y2 = self.roi_y1 + h

        # Constants
        self.method = method
        self.kernel_size = kernel_size
        self.preview = preview
        self.debug = debug

        # number of failed tries
        self.failed_tries = 0

        # SwarmRobot
        self.bot = bot;

    def track_line(self, frame, event, bot):
        if not event.isSet():
            # Cut out Region of interest
            if self.debug:
                cv.imshow('Frame', frame)
            frame = frame[self.roi_y1:self.roi_y2, self.roi_x1:self.roi_x2]

            # Convert to grayscale
            try:
                gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
                if self.debug:
                    cv.imshow('Gray', gray)
            except Exception as exception:
                self.failed_tries += 1
                if self.failed_tries > 5:
                    print('Line tracking error, please check error log.')
                    raise exception
                return
            
            # Reset failed tries after a successfull trie, to prevent just stopping after to many fails.
            self.failed_tries = 0

            # Gausian blur
            blur = cv.GaussianBlur(gray, self.kernel_size, 0)
            if self.debug:
                cv.imshow('Blur', blur)

            # Color thresholding
            # thresh = cv.adaptiveThreshold(blur ,255,cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY_INV,11,2)
            rel, thresh = cv.threshold(blur, 60, 255, cv.THRESH_BINARY_INV)
            if self.debug:
                cv.imshow('Thresh', thresh)

            # Find contours
            contours, hierarchy = cv.findContours(
                thresh.copy(), 1, cv.CHAIN_APPROX_NONE)

            # Find the biggest detected contour
            if len(contours) > 0:
                c = max(contours, key=cv.contourArea)
                M = cv.moments(c)

                if M['m00'] == 0:
                    return None

                cx = int(M['m10']/M['m00'])
                cy = int(M['m01']/M['m00'])

                if self.preview:
                    cv.line(frame, (cx, 0), (cx, 720), (255, 0, 0), 1)
                    cv.line(frame, (0, cy), (1280, cy), (255, 0, 0), 1)

                    cv.drawContours(frame, contours, -1, (0, 255, 0), 1)

                    cv.imshow('Preview', frame)

                return ((cx*2) / frame.shape[1]) - 1
            else:
                steer = bot.steer * -1
                bot.set_drive_steer(steer)
                sleep(TURN_SLEEP_TIME)
                bot.drive(10)
                bot.set_drive_steer(0)
                sleep(TURN_SLEEP_TIME)
                bot.drive(10)
                sleep(TURN_SLEEP_TIME)
                bot.set_drive_steer(bot.steer)

                return self.track_line(frame, event, bot)
