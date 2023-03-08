import cv2
import numpy as np

class ParkingSpaceDetection:
    """
    erkennt parkplatz, soll auch position des roboters bestimmen
    """
        
    def detect_red_line(self, img):
        # threshold on red color
        lowcolor = (0,36,235)#(0,0,75)
        highcolor = (67,112,255)#(50,50,135)
        thresh = cv2.inRange(img, lowcolor, highcolor)


        # apply morphology close
        kernel = np.ones((5,5), np.uint8)
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

        # get contours and filter on area
        contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = contours[0] if len(contours) == 2 else contours[1]
        print('Contours',contours)
        #for c in contours:
        #    area = cv2.contourArea(c)
        #    if area > 5000:
        #        cv2.drawContours(result, [c], -1, (0, 255, 0), 2)
        if len(contours)>0:
            return True
        
        return False
    
    def detect_red_line2(self, img):
        result = img.copy()
        image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        lower = np.array([155,25,0])
        upper = np.array([179,255,255])
        mask = cv2.inRange(image, lower, upper)
        result = cv2.bitwise_and(result, result, mask=mask)
        print(result)
        if len(result)>0:
            return True
        
        return False