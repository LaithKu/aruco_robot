"""
This script calculates translation and rotation between camera and ArUco Marker based
on the known marker size and calculated intrinsic camera calibration
"""

import cv2
import numpy as np


class PoseEstimator:
    def __init__(
        self,
        calibration_file,
        marker_size
    ):
        calibration = np.load(calibration_file)

        self.camera_matrix = calibration["camera_matrix"]
        self.distortion_coefficients = calibration["distortion_coefficients"]

        self.marker_size = marker_size

        half_size = marker_size / 2.0

        # Marker corner coordinates in its local 3D coordinate system
        self.object_points = np.array(
            [
                [-half_size, half_size, 0],
                [half_size, half_size, 0],
                [half_size, -half_size, 0],
                [-half_size, -half_size, 0]
            ],
            dtype=np.float32
        )

    def estimate_pose(self, marker_corners):
        image_points = marker_corners.reshape(4, 2).astype(
            np.float32
        )

        # Solve Perspective-n-Point to get translation and rotation vector
        success, rotation_vector, translation_vector = \
            cv2.solvePnP(
                self.object_points,
                image_points,
                self.camera_matrix,
                self.distortion_coefficients,
                flags=cv2.SOLVEPNP_IPPE_SQUARE
            )

        if not success:
            return None, None

        return rotation_vector, translation_vector