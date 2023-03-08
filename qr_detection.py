import cv2


class QrDetection:
    """
    Scan and detect QR Code
    """
    def __init__(self):
        # QR code detection object
        self.detector = cv2.QRCodeDetector()
    
    
    def detect_qr(self, img):
        """
        get bounding box coords and data

        :param image
        :return data and coordinates from QR Code
        """
        data, points, _ = self.detector.detectAndDecode(img)

        return data, points


    def compare_road(self, data, goal):
        """
        compare data from QR Code with goal

        :param data from QR Code
        :param goal which is predefined
        :return direction where to drive
        """
        direction = None
        if data is not None:
            if data == "lagern":
                direction = data
            else:
                for line in data.split(";"):
                    if line.find(goal) is not -1:
                        direction = line.split(":")[1]
        return direction

