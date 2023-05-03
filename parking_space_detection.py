import cv2 as cv
import numpy as np

from constants import RED_LOW, RED_HIGH

class ParkingSpaceDetection:
    """
    erkennt parkplatz, soll auch position des roboters bestimmen
    """
    # number of failed tries
    failed_tries = 0

    def __init__(self, debug: bool=False):
        self.debug = debug

    def detect_red_line(self, img):
        # threshold on red color
        thresh = cv.inRange(img, RED_LOW, RED_HIGH)

        # apply morphology close
        kernel = np.ones((5, 5), np.uint8)
        thresh = cv.morphologyEx(thresh, cv.MORPH_CLOSE, kernel)

        # get contours and filter on area
        contours = cv.findContours(
            thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        contours = contours[0] if len(contours) == 2 else contours[1]
        if self.debug:
            print('Contours', contours)
        # for c in contours:
        #    area = cv.contourArea(c)
        #    if area > 5000:
        #        cv.drawContours(result, [c], -1, (0, 255, 0), 2)
        if len(contours) > 0:
            return True

        return False

    def detect_red_line2(self, img):
        result = img.copy()
        try:
            image = cv.cvtColor(img, cv.COLOR_BGR2HSV)
        except Exception as exception:
            self.failed_tries += 1
            if self.failed_tries > 5:
                raise exception
            return False
        lower = np.array([155, 25, 0])
        upper = np.array([179, 255, 255])
        mask = cv.inRange(image, lower, upper)
        result = cv.bitwise_and(result, result, mask=mask)
        print(result)
        if len(result) > 0:
            return True

        return False
