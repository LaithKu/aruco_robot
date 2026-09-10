"""
This script tests connection to LeKiwi robot using LeKiwi_interface
additionally, it tests if the simple movement commands can be executed
"""

import time

from lekiwi_interface import LeKiwiInterface


def main():
    robot = LeKiwiInterface(
        linear_speed=0.05
    )

    print("Connecting to LeKiwi...")
    robot.connect()

    print("Connected.")
    print("Testing a short forward movement.")

    try:
        robot.execute("MOVE_FORWARD")

        time.sleep(0.5)

        robot.stop()

        print("Movement test finished.")

    finally:
        robot.stop()
        robot.disconnect()

    print("Disconnected.")


if __name__ == "__main__":
    main()