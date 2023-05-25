import sys

from datetime import datetime  # Usage is commented.
# from time import sleep

import numpy as np
import cv2 as cv

from collections import defaultdict

from constants import RED_LOW, RED_HIGH, MAXIMAL_THETA_RADIANT_VERTICAL


class IntersectionDetection:

    def __init__(self, width, height, bot, kernel_size=(5, 5), preview=False, debug=False):
        # Define Region of interest
        self.resolution = (int(width), int(height))
        w = self.resolution[0]//3
        h = self.resolution[1]//2
        self.roi_x1 = self.resolution[0]//2 - w//2
        self.roi_y1 = self.resolution[1] - h
        self.roi_x2 = self.roi_x1 + w
        self.roi_y2 = self.roi_y1 + h

        self.lines = []
        self.segmented = []

        # Constants
        self.kernel_size = kernel_size
        self.preview = preview
        self.debug = debug

        self._bot = bot

        # number of failed tries
        self.failed_tries = 0

    def segment_by_angle_kmeans(self, lines, k=2, **kwargs):
        """
        Group lines by their angle using k-means clustering.

        Code from here:
        https://stackoverflow.com/a/46572063/1755401
        """

        # Define criteria = (type, max_iter, epsilon)
        default_criteria_type = cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER
        criteria = kwargs.get('criteria', (default_criteria_type, 10, 1.0))

        flags = kwargs.get('flags', cv.KMEANS_RANDOM_CENTERS)
        attempts = kwargs.get('attempts', 10)

        # Get angles in [0, pi] radians
        angles = np.array([line[0][1] for line in lines])

        # Multiply the angles by two and find coordinates of that angle on the Unit Circle
        pts = np.array([[np.cos(2 * angle), np.sin(2 * angle)]
                       for angle in angles], dtype=np.float32)

        # Run k-means
        if sys.version_info[0] == 2:
            # python 2.x
            ret, labels, centers = cv.kmeans(pts, k, criteria, attempts, flags)
        else:
            # python 3.x, syntax has changed.
            labels, centers = cv.kmeans(
                pts, k, None, criteria, attempts, flags)[1:]

        labels = labels.reshape(-1)  # Transpose to row vector

        # Segment lines based on their label of 0 or 1
        segmented = defaultdict(list)
        for i, line in zip(range(len(lines)), lines):
            segmented[labels[i]].append(line)

        self.segmented = list(segmented.values())
        # print("Segmented lines into two groups: %d, %d" % (len(segmented[0]), len(segmented[1])))

        return self.segmented

    def intersection(self, line1, line2):
        """
        Find the intersection of two lines
        specified in Hesse normal form.

        Returns closest integer pixel locations.

        See here:
        https://stackoverflow.com/a/383527/5087436
        """

        rho1, theta1 = line1[0]
        rho2, theta2 = line2[0]
        A = np.array([[np.cos(theta1), np.sin(theta1)],
                      [np.cos(theta2), np.sin(theta2)]])
        b = np.array([[rho1], [rho2]])
        x0, y0 = np.linalg.solve(A, b)
        x0, y0 = int(np.round(x0)), int(np.round(y0))

        return [[x0, y0]]

    def segmented_intersections(self, lines):
        """
        Find the intersection between groups of lines.
        """

        intersections = []
        for i, group in enumerate(lines[:-1]):
            for next_group in lines[i + 1:]:
                for line1 in group:
                    for line2 in next_group:
                        intersections.append(self.intersection(line1, line2))

        return intersections

    # def drawLines(img, lines, color=(0, 0, 255)):
    #     """
    #     Draw lines on an image
    #     """
    #     for line in lines:
    #         for rho, theta in line:
    #             a = np.cos(theta)
    #             b = np.sin(theta)
    #             x0 = a * rho
    #             y0 = b * rho
    #             x1 = int(x0 + 1000 * (-b))
    #             y1 = int(y0 + 1000 * (a))
    #             x2 = int(x0 - 1000 * (-b))
    #             y2 = int(y0 - 1000 * (a))
    #             cv.line(img, (x1, y1), (x2, y2), color, 1)

    def detect_intersection(self, img):
        height, width, _ = img.shape
        height_crop = int(height / 4)
        width_crop = int(width / 4)
        resized = img[height - height_crop:height,
                      width_crop:width - width_crop, :]

        # Copy of colored imagesection with the intersection
        resized_full_colored = resized.copy()

        try:
            # Turn red dots into black
            mask = cv.inRange(resized, RED_LOW, RED_HIGH)
            resized[mask != 0] = [0, 0, 0]
            if self.preview:
                cv.imshow('red_to_black', resized)

            # Convert to grayscale
            gray = cv.cvtColor(resized, cv.COLOR_BGR2GRAY)
        except Exception as exception:
            self.failed_tries += 1
            if self.failed_tries > 5:
                raise exception
            return

        # extract black areas
        _, thresh = cv.threshold(gray, 40, 255, cv.THRESH_BINARY_INV)
        # do some image processing
        eroded = cv.dilate(thresh, None, iterations=1)
        eroded = cv.erode(eroded, None, iterations=3)
        dilated = cv.dilate(eroded, None, iterations=2)

        blur = cv.medianBlur(dilated, 5)

        # Make binary image
        adapt_type = cv.ADAPTIVE_THRESH_GAUSSIAN_C
        thresh_type = cv.THRESH_BINARY_INV
        bin_img = cv.adaptiveThreshold(
            blur, 255, adapt_type, thresh_type, 11, 2)

        if self.debug:
            cv.imshow('bin_img-intersecrtion', bin_img)

        # Detect lines
        rho = 2
        theta = np.pi / 180
        thresh = 350
        self.lines = cv.HoughLines(bin_img, rho, theta, thresh)

        # print("Found lines: %d" % (len(lines)))
        intersections = []
        if self.lines is not None and len(self.lines) > 0 :
            # Cluster line angles into 2 groups (vertical and horizontal)
            self.segmented = self.segment_by_angle_kmeans(self.lines, 2)

            # Find the intersections of each vertical line with each horizontal line
            intersections = self.segmented_intersections(self.segmented)

            self._bot.intersection_img = resized_full_colored

        self._bot.intersection = intersections
        # print(datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])

    def get_right_upper_corner_intersection(self, img, intersection):
        if img is not None:
            height, width, _ = img.shape
            height_crop = int(height / 4)
            width_crop = int(width / 4)
            y = 1 + int(height_crop/3)
            x = 1
            h = intersection[0][0] + (3*height_crop) - 125
            w = intersection[0][1] + width_crop + 110
            crop_img = img[y:y+h, x:x+w]
            return crop_img

    def get_intersection_coordinates(self, intersection):
        n = 0
        for val in intersection:
            if ((intersection[0][0][0]+2) > 0 and (intersection[0][0][1]+2) > 0):
                return n
            n = n+1
        return -1

    def get_lines_from_intersection(self, intersection_index: int, detected_lines: list):
        """
        Gets the lines that form the interscetion idetified by the given intersection index.

        Parameter
        ---------
        intersection_index: int
            index of the intersection, formed from the lines of interest.

        Retunrs
        -------
        list[]: Lines with rho and theta, that form the intersection with the index of intersection_index.
        """
        # Get the intersection coordinates
        intersection = self._bot.intersection[intersection_index][0] # macht probleme
        if self.debug:
            print('intersection[0] : {0} intersection[1] : {1}'.format(intersection[0], intersection[1]))

        # Find the lines that form the intersection
        lines = []
        # additional to lines, i need to make segmented from line 77 into a object vairable
        for group in detected_lines:
            for line in group:
                rho, theta = line[0]
                a = np.cos(theta)
                b = np.sin(theta)
                x0 = a * rho
                y0 = b * rho
                x1 = int(x0 + 1000 * (-b))
                y1 = int(y0 + 1000 * (a))
                x2 = int(x0 - 1000 * (-b))
                y2 = int(y0 - 1000 * (a))

                # Check if the line passes through the intersection
                if abs((y2 - y1) * intersection[0] - (x2 - x1) * intersection[1] + x2 * y1 - y2 * x1) < 1e-6: # macht probleme
                    lines.append(line)

        return lines

    def get_vertical_line(self, lines: list):
        """
        Checks if a line in the given list of lines is vertical and returns the first vertical line.

        Parameter
        ---------
        lines: list
            List of lines to be checked.

        Returns
        -------
        None: If no vertical line is contained.
        list: List containing the first vertical line in the given lines. the line has rho, the distanceto the coordinates origin (0,0), and theta, the angle to the x-axis.
        """
        for line in lines:
            rho, theta = line[0]
            if abs(theta - np.pi / 2) < MAXIMAL_THETA_RADIANT_VERTICAL:
                return line[0]

    def get_horizontal_line(self, lines: list):
        """
        Checks if a line in the given list of lines is horizontal and returns the first vertical line.

        Parameter
        ---------
        lines: list
            List of lines to be checked.

        Returns
        -------
        None: If no horizontal line is contained.
        list: List containing the first horizontal line in the given lines. the line has rho, the distanceto the coordinates origin (0,0), and theta, the angle to the x-axis.
        """
        for line in lines:
            rho, theta = line[0]
            if not abs(theta - np.pi / 2) < MAXIMAL_THETA_RADIANT_VERTICAL:
                return line[0]

    # img_with_segmented_lines = np.copy(img)
    #
    # # Draw vertical lines in green
    # vertical_lines = segmented[1]
    # img_with_vertical_lines = np.copy(img)
    # drawLines(img_with_segmented_lines, vertical_lines, (0, 255, 0))
    #
    # # Draw horizontal lines in yellow
    # horizontal_lines = segmented[0]
    # img_with_horizontal_lines = np.copy(img)
    # drawLines(img_with_segmented_lines, horizontal_lines, (0, 255, 255))
    #
    # # Draw intersection points in magenta
    # for point in intersections:
    #     pt = (point[0][0], point[0][1])
    #     length = 5
    #     cv.line(img_with_segmented_lines, (pt[0], pt[1] - length), (pt[0], pt[1] + length), (255, 0, 255),
    #              1)  # vertical line
    #     cv.line(img_with_segmented_lines, (pt[0] - length, pt[1]), (pt[0] + length, pt[1]), (255, 0, 255), 1)
    #
    # cv.imshow("Segmented lines", img_with_segmented_lines)
    # cv.waitKey()
    # cv.imwrite("intersection_points.jpg", img_with_segmented_lines)
