"""
This script is used to calculate the camera intrinsic matrix
based on images taken by the camera of a known chessboard
"""

import glob
import cv2
import numpy as np


def main():
    # Number of inner chessboard corners
    chessboard_size = (10, 7)

    # Prepare 3D coordinates of the chessboard corners
    # Each object point represents a square from the chessboard
    object_points_template = np.zeros(
        (chessboard_size[0] * chessboard_size[1], 3),
        dtype=np.float32
    )

    # set z coordinate to 0
    object_points_template[:, :2] = np.mgrid[
        0:chessboard_size[0],
        0:chessboard_size[1]
    ].T.reshape(-1, 2)

    object_points = []
    image_points = []

    # Change path if needed
    image_files = glob.glob("webcam/images/*.jpg")

    if not image_files:
        raise RuntimeError("No calibration images found.")

    image_size = None

    # Find Corners of the chessboard images
    for filename in image_files:
        image = cv2.imread(filename)

        gray = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2GRAY
        )

        image_size = gray.shape[::-1]

        found, corners = cv2.findChessboardCorners(
            gray,
            chessboard_size
        )

        if not found:
            print(f"No chessboard found in {filename}")
            continue

        # Improve the corner positions to sub-pixel accuracy
        corners_refined = cv2.cornerSubPix(
            gray,
            corners,
            (11, 11),
            (-1, -1),
            (
                cv2.TERM_CRITERIA_EPS
                + cv2.TERM_CRITERIA_MAX_ITER,
                30,
                0.001
            )
        )

        object_points.append(object_points_template)
        image_points.append(corners_refined)

        print(f"Used: {filename}")

    if len(object_points) < 5:
        raise RuntimeError(
            "Not enough valid calibration images. Minimum of 5 images is required"
        )

    # Calculation camera parameters based on the object and corresponding image points
    error, camera_matrix, distortion_coefficients, _, _ = \
        cv2.calibrateCamera(
            object_points,
            image_points,
            image_size,
            None,
            None
        )

    print("\nCalibration finished.")
    print(f"Reprojection error: {error}")

    print("\nCamera matrix:")
    print(camera_matrix)

    print("\nDistortion coefficients:")
    print(distortion_coefficients)

    # Change directory if needed
    np.savez(
        "webcam/calibration/camera_calibration.npz",
        camera_matrix=camera_matrix,
        distortion_coefficients=distortion_coefficients
    )

    print(
        "\nCalibration saved to "
        "calibration/camera_calibration.npz"
    )


if __name__ == "__main__":
    main()