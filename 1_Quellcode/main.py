import cv2

from vision.camera import open_camera
from vision.aruco_detector import ArucoDetector
from vision.pose_estimator import PoseEstimator
from navigation.follow_controller import FollowController


def main():
    camera = open_camera(0)
    detector = ArucoDetector()

    # Real marker side length in meters
    marker_size = 0.10

    # Change path if needed
    pose_estimator = PoseEstimator(
        "calibration/webcam/calibration/camera_calibration.npz",
        marker_size
    )

    # Follow Controller
    follow_controller = FollowController(
        target_distance=0.30,       # Desired Destination from target
        distance_tolerance=0.05,
        lateral_tolerance=0.05
    )
    # Only this marker will be used as the navigation target
    target_id = 0

    window_name = "ArUco Follow Controller"
    cv2.namedWindow(window_name)

    print("Camera opened successfully.")
    print(f"Following marker ID {target_id}")
    print("Press Q or ESC to quit.")
    try:
        while True:
            success, frame = camera.read()

            if not success:
                print("Could not read frame from camera.")
                break

            # Marker detection
            corners, ids, rejected = detector.detect(frame)
            # print(corners, " ", ids)

            # Default command if the target marker is not visible
            command = "STOP"
            target_found = False

            if ids is not None:
                # print(corners, " ", ids)
                # Draw marker boundaries
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

                    # Draw local frame axes with origin in the center of each marker
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

                    # Get corner position of first corene (upper left corner)
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

            cv2.putText(
                frame,
                f"Command: {command}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 255),
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