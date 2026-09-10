import cv2

from vision.camera import open_camera
from vision.aruco_detector import ArucoDetector


def main():
    camera = open_camera(0)
    detector = ArucoDetector()

    window_name = "ArUco Detection"
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
                print(corners, " ", ids)
                cv2.aruco.drawDetectedMarkers(
                    frame,
                    corners,
                    ids
                )

            # Show frame with drawn marker
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