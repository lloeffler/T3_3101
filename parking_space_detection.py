import cv2 as cv
import numpy as np

from skimage.transform import ProjectiveTransform, AffineTransform

from constants import RED_LOW, RED_HIGH
from parking_learner import cart2pol


class ParkingSpaceDetection:
    """
    Detects a parking lot.
    To do so, it checks if a given image of an intersection has red lines.
    Should calculate relativ position of the robot to the parking lot.
    """
    # number of failed tries
    failed_tries = 0

    def __init__(self, debug: bool = False):
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

    def calculate_position(self, img, intersection: list[list[int]]) -> tuple:
        """
        Calculates relative position of the robot to the parking lot aka intersection in the image.

        Parameter
        ---------
        img: Mat
            Image containing the intersection with the parking lot.
        intersection: list[list[int]]
            Coordinates of the intersection.

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
        new_point = np.array([intersection[0][0], intersection[0][1]])
        affine_transformed_point = affine_transformation(new_point)
        projective_transformed_point = projective_transformation(new_point)

        # Transformation to polar coordinates
        rho, phi = cart2pol(x=affine_transformed_point[0], y=affine_transformed_point[1])
        
        if self.debug:
            print('affine: x={0} y={1}'.format(affine_transformed_point[0], affine_transformed_point[1]))
            print('projective: x={0} y={1}'.format(projective_transformed_point[0], projective_transformed_point[1]))

        # Calculation of the orientation
        return (round(rho), round(phi), 18)
