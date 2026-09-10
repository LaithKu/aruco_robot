"""
This script tests connection to LeKiwi robot using LeKiwi_interface
additionally, it tests if the front camera of the robot can be opened
"""

import cv2

from lekiwi_interface import LeKiwiInterface


def main():
    robot = LeKiwiInterface()

    print("Connecting to LeKiwi...")

    robot.connect()

    print("Connected.")
    print("Press Q or ESC to quit.")

    try:
        while True:
            frame = robot.get_frame()

            print(
                "Frame shape:",
                frame.shape
            )

            cv2.imshow(
                "LeKiwi Front Camera",
                frame
            )

            key = cv2.waitKey(10) & 0xFF

            if key == ord("q") or key == ord("Q") or key == 27:
                break

    finally:
        robot.stop()
        robot.disconnect()
        cv2.destroyAllWindows()

    print("Disconnected.")


if __name__ == "__main__":
    main()