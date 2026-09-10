import cv2

from vision.camera import open_camera
from vision.aruco_detector import ArucoDetector
from vision.pose_estimator import PoseEstimator


def main():
    camera = open_camera(0)
    detector = ArucoDetector()

    # Set marker side length in meters
    marker_size = 0.10

    # Change path if needed
    pose_estimator = PoseEstimator(
        "calibration/webcam/calibration/camera_calibration.npz",
        marker_size
    )

    window_name = "ArUco Pose Estimation"
    cv2.namedWindow(window_name)

    print("Camera opened successfully.")
    print("Press Q or ESC to quit.")
    try:
        while True:
            success, frame = camera.read()

            if not success:
                print("Could not read frame from camera.")
                break

            # Marker detection
            corners, ids, rejected = detector.detect(frame)
            # if marker is identified, draw marker in the frame
            # print(corners, " ", ids)
            if ids is not None:
                # print(corners, " ", ids)
                cv2.aruco.drawDetectedMarkers(
                    frame,
                    corners,
                    ids
                )

                for marker_corners, marker_id in zip(corners, ids.flatten()):
                    rotation_vector, translation_vector = \
                        pose_estimator.estimate_pose(marker_corners)

                    if translation_vector is None:
                        continue

                    x = translation_vector[0][0]
                    y = translation_vector[1][0]
                    z = translation_vector[2][0]

                    print(
                        f"Marker {marker_id}: "
                        f"x={x:.3f} m, "
                        f"y={y:.3f} m, "
                        f"z={z:.3f} m"
                    )

                    cv2.drawFrameAxes(
                        frame,
                        pose_estimator.camera_matrix,
                        pose_estimator.distortion_coefficients,
                        rotation_vector,
                        translation_vector,
                        marker_size * 0.5
                    )

                    position_text = (
                        f"ID {marker_id}: "
                        f"x={x:.2f} "
                        f"y={y:.2f} "
                        f"z={z:.2f} m"
                    )

                    corner = marker_corners.reshape(4, 2)[0]

                    text_position = (
                        int(corner[0]),
                        int(corner[1]) - 15
                    )

                    cv2.putText(
                        frame,
                        position_text,
                        text_position,
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        (0, 255, 0),
                        2
                    )


            # Show frame with drawn marker, position text and frame axis showing orientation
            cv2.imshow("Camera Test", frame)

            # waitKey() returns the key pressed while the OpenCV window is active
            key = cv2.waitKey(10) & 0xFF

            if key == ord("q") or key == ord("Q") or key == 27:
                break

            # Also stop when the user closes the window with the X button
            if cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
                break
    finally:
        # Terminate the opened camera and close its window
        camera.release()
        cv2.destroyAllWindows()

    print("Camera closed.")



if __name__ == "__main__":
    main()