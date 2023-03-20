import cv2 as cv
import numpy as numpy
import time


class LineTracker:
    def __init__(self, width, height, method='contour', kernel_size=(5, 5), preview=False, debug=False):
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
                    raise exception
                return

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
                time.sleep(0.5)
                bot._drive_motor.rotate_motor(-0.6*510)
                time.sleep(0.5)
                bot.set_drive_steer(0)
                time.sleep(0.5)
                bot._drive_motor.rotate_motor(0.6*510)
                time.sleep(0.5)
                bot.set_drive_steer(bot.steer)

                return self.track_line(frame, event, bot)
