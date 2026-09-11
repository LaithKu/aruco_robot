"""
This script is used to capture images of the calibration chessboard from different angels
"""


import os
import cv2

from vision.camera import open_camera


def main():
    camera = open_camera(0)

    # change path depending on camera
    # use "lekiwi/images" for LeKiwi
    output_directory = "webcam/images"
    os.makedirs(output_directory, exist_ok=True)

    image_counter = 0
    window_name = "Calibration Image Capture"

    print("Press SPACE to save an image.")
    print("Press Q or ESC to quit.")

    try:
        while True:
            success, frame = camera.read()

            if not success:
                print("Could not read frame.")
                break

            cv2.putText(
                frame,
                f"Saved images: {image_counter}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )

            cv2.imshow(window_name, frame)

            # waitKey() returns the key pressed while the OpenCV window is active
            key = cv2.waitKey(10) & 0xFF

            # Save frame if space is pressed
            if key == ord(" "):
                filename = os.path.join(
                    output_directory,
                    f"calibration_{image_counter:02d}.jpg"
                )

                cv2.imwrite(filename, frame)
                print(f"Saved: {filename}")

                image_counter += 1

                if key == ord("q") or key == ord("Q") or key == 27:
                    break

                # Also stop when the user closes the window with the X button
                if cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
                    break

    finally:
        camera.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()