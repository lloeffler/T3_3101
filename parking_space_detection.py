import traceback
import datetime

import cv2 as cv
import numpy as np

from math import degrees

from skimage.transform import ProjectiveTransform, AffineTransform

from intersection_detection import IntersectionDetection
from constants import RED_LOW, RED_HIGH, DEFAULT_ORIENTATION
from parking_learner import cart2pol


class ParkingSpaceDetection:
    """
    Detects a parking lot.
    To do so, it checks if a given image of an intersection has red lines.
    Should calculate relativ position of the robot to the parking lot.
    """
    # number of failed tries
    failed_tries = 0

    def __init__(self, intersection_detector: IntersectionDetection, debug: bool = False, preview: bool = False):
        self.preview = preview
        self.debug = debug
        self._intersection_detector = intersection_detector

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
        if self.preview:
            cv.imshow('thresh', thresh)
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

    def calculate_position(self, intersections: list, intersection_index: int, detected_lines: list) -> tuple:
        """
        Calculates relative position of the robot to the parking lot aka intersection in the image.

        Parameter
        ---------
        intersections: list
            Liast of all intersections.
        intersection_index: int
            Index of the intersection looked for.

        Returns
        -------
        tuple: Position with rho, phi and orientation of the robot relativ to the parking lot aka intersection.
        """

        # Known pixel
        src = np.array([[320, 480], [320, 0], [547, 300], [447, 67]])

        # Known coordinates
        dst = np.array([[8.1, 0.0], [50.5, 0.0], [17.0, 11.5], [43.0, 11.5]])

        # affine transformation
        affine_transformation = AffineTransform()
        affine_transformation.estimate(src, dst)

        # projective Transformation
        projective_transformation = ProjectiveTransform()
        projective_transformation.estimate(src, dst)

        # Calculation of the coordinate
        new_point = np.array([intersections[intersection_index]
                             [0][0], intersections[intersection_index][0][1]])
        affine_transformed_point = affine_transformation(new_point)
        projective_transformed_point = projective_transformation(new_point)

        # Transformation to polar coordinates
        rho, phi = cart2pol.__func__(
            x=affine_transformed_point[0][0], y=affine_transformed_point[0][1])

        if self.debug:
            print('affine: x={0} y={1}'.format(
                affine_transformed_point[0][0], affine_transformed_point[0][1]))
            print('projective: x={0} y={1}'.format(
                projective_transformed_point[0][0], projective_transformed_point[0][1]))
            
        try:
            # Get lines of intersection.
            intersection_lines = self._intersection_detector.get_lines_from_intersection(
                intersection_index=intersection_index, detected_lines=detected_lines)
            print('intersection_lines: {}'.format(intersection_lines))
            # Get vertical line from intersection.
            line_rho, line_theta = self._intersection_detector.get_vertical_line(intersection_lines)[0] #macht probleme
            # Calculation of the orientation, based on the theta value of the vertical line in the intersection.
            # Difference between line angle and pi/2 (90 degree as radiant).
            delta_theta = line_theta - (np.pi/2)
            # Not rounded orientation as radiant.
            # Pi (180 degree as radiant) is the default orientation when the line is measured with pi/2 (90 degree as radiant) to the images x-axis.
            orientation_radiant = np.pi - delta_theta
            # Not rounded orientation.
            orientation = degrees(orientation_radiant)/10 # weiter als zeile 122 war ich noch nicht
        except Exception as exception:
            orientation = DEFAULT_ORIENTATION
            error_str = "[Parking_space_detection|{0}] {1}\nTraceback:\n{2}".format(
                datetime.datetime.now().isoformat(), str(exception), traceback.format_exc())
            if self.debug:
                print(error_str)
            log_file = open("error.log", "a")
            log_file.write(error_str)
            log_file.close()
        return (int(round(rho)), int(round(phi)), int(round(orientation)))
