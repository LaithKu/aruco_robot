import cv2

from vision.aruco_detector import ArucoDetector
from vision.pose_estimator import PoseEstimator
from navigation.follow_controller import FollowController
from robot.lekiwi_interface import LeKiwiInterface


# Keep movement disabled until camera, calibration and pose estimation
# have been tested successfully on the real robot.
ENABLE_MOVEMENT = True


def main():
    robot = LeKiwiInterface(
        port="/dev/ttyACM0",
        linear_speed=0.07
    )

    detector = ArucoDetector()

    # Real marker side length in meters
    marker_size = 0.95

    # Calibration parameters of the LeKiwi front camera
    pose_estimator = PoseEstimator(
        "calibration/lekiwi/calibration/camera_calibration.npz",
        marker_size
    )

    follow_controller = FollowController(
        target_distance=0.50,
        distance_tolerance=0.05,
        lateral_tolerance=0.05
    )

    # Only this marker will be used as the navigation target
    target_id = 0

    window_name = "LeKiwi ArUco Follow Controller"
    cv2.namedWindow(window_name)

    print("Connecting to LeKiwi...")
    robot.connect()

    print("LeKiwi connected successfully.")
    print(f"Following marker ID {target_id}")

    if ENABLE_MOVEMENT:
        print("WARNING: Robot movement is ENABLED.")
    else:
        print("Robot movement is DISABLED.")

    print("Press Q or ESC to quit.")

    try:
        while True:
            # Get the latest frame from the LeKiwi front camera
            frame = robot.get_frame()

            # Detect ArUco markers
            corners, ids, rejected = detector.detect(frame)

            # Default command if the target marker is not visible
            command = "STOP"
            target_found = False

            if ids is not None:
                # Draw boundaries around all detected markers
                cv2.aruco.drawDetectedMarkers(
                    frame,
                    corners,
                    ids
                )

                # Combine marker id and corners in one element and proceed
                # with the pose estimation and visualisation for each detected marker separately
                for marker_corners, marker_id in zip(corners, ids.flatten()):
                    # Estimate relative pose to camera
                    rotation_vector, translation_vector = pose_estimator.estimate_pose(marker_corners)

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

                    # Draw local marker coordinate system with origin in the center of each marker
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

                    # Get corner position of first corner (upper left corner)
                    corner = marker_corners.reshape(4, 2)[0]

                    text_position = (
                        int(corner[0]),
                        int(corner[1]) - 15     # y offset between position text and marker boundary
                    )

                    # Show position text above each marker
                    cv2.putText(
                        frame,
                        position_text,
                        text_position,
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        (0, 255, 0),
                        2
                    )

                    # Navigation
                    # Ignore all markers for navigation except the selected target
                    if marker_id != target_id:
                        continue
                    target_found = True
                    command = follow_controller.get_command(x, z)

            # Stop if target is not found
            if not target_found:
                command = "STOP"

            # Send the calculated command only when movement was
            # explicitly enabled.
            if ENABLE_MOVEMENT:
                robot.execute(command)
            else:
                # Make sure the robot remains stationary during testing
                robot.stop()

            cv2.putText(
                frame,
                f"Command: {command}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 255),
                2
            )

            movement_status = (
                "MOVEMENT ENABLED"
                if ENABLE_MOVEMENT
                else "MOVEMENT DISABLED"
            )

            cv2.putText(
                frame,
                movement_status,
                (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 0, 255),
                2
            )

            # Show frame with drawn marker, position text and frame axis showing orientation
            cv2.imshow(window_name, frame)

            # waitKey() returns the key pressed while the OpenCV window is active
            key = cv2.waitKey(10) & 0xFF

            if key == ord("q") or key == ord("Q") or key == 27:
                break

            # Also stop when the user closes the window with the X button
            if cv2.getWindowProperty(window_name,cv2.WND_PROP_VISIBLE) < 1:
                break

    finally:
        # Stop the base before disconnecting from the robot
        print("Stopping robot...")
        robot.stop()

        print("Disconnecting from LeKiwi...")
        robot.disconnect()

        cv2.destroyAllWindows()

    print("LeKiwi disconnected.")


if __name__ == "__main__":
    main()