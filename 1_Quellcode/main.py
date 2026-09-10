import cv2

from vision.camera import open_camera


def main():
    camera = open_camera(0)

    window_name = "Camera Test"
    cv2.namedWindow(window_name)

    print("Camera opened successfully.")
    print("Press Q to quit.")

    while True:
        success, frame = camera.read()

        if not success:
            print("Could not read frame from camera.")
            break

        cv2.imshow("Camera Test", frame)

        # waitKey() returns the key pressed while the OpenCV window is active
        key = cv2.waitKey(10) & 0xFF

        if key == ord("q") or key == ord("Q") or key == 27:
            break

        # Also stop when the user closes the window with the X button
        if cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
            break

    # Terminate the opened camera and close its window
    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()