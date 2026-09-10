import cv2


class ArucoDetector:
    def __init__(self):
        # Set used Aruco dictionary as 4X4
        self.dictionary = cv2.aruco.getPredefinedDictionary(
            cv2.aruco.DICT_4X4_50
        )

        # Create configuration object that controls ArUco
        self.parameters = cv2.aruco.DetectorParameters()

        # Create detection object
        self.detector = cv2.aruco.ArucoDetector(
            self.dictionary,
            self.parameters
        )

    def detect(self, frame):
        corners, ids, rejected = self.detector.detectMarkers(frame)

        return corners, ids, rejected