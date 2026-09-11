"""
This script is the interface to run ArUco based navigation locally
on the Raspberry Pi5 of the LeKiwi robot running wit LeRobot
"""

from lerobot.cameras import Cv2Rotation, ColorMode
from lerobot.cameras.opencv import OpenCVCameraConfig
from lerobot.robots.lekiwi import LeKiwi, LeKiwiConfig


class LeKiwiInterface:
    def __init__(
        self,
        # Change depending on Raspi configuration
        port="/dev/ttyACM0",
        robot_id="aruco_lekiwi",
        linear_speed=0.10
    ):
        self.linear_speed = linear_speed

        front_camera = OpenCVCameraConfig(
            # Change depending on Raspi configuration
            index_or_path="/dev/video0",
            fps=30,
            width=640,
            height=480,
            color_mode=ColorMode.BGR,
            fourcc="MJPG"
            # rotation=Cv2Rotation.ROTATE_180
        )

        config = LeKiwiConfig(
            port=port,
            id=robot_id,
            cameras={
                "front": front_camera
            }
        )

        self.robot = LeKiwi(config)

    def connect(self):
        self.robot.connect()

    def get_frame(self):
        observation = self.robot.get_observation()
        return observation["front"]

    def execute(self, command):
        if command == "MOVE_FORWARD":
            self._send_velocity(
                x_velocity=self.linear_speed
            )

        elif command == "MOVE_BACKWARD":
            self._send_velocity(
                x_velocity=-self.linear_speed
            )

        elif command == "MOVE_LEFT":
            self._send_velocity(
                y_velocity=self.linear_speed
            )

        elif command == "MOVE_RIGHT":
            self._send_velocity(
                y_velocity=-self.linear_speed
            )

        else:
            self.stop()

    def stop(self):
        self.robot.stop_base()

    def _send_velocity(
        self,
        x_velocity=0.0,
        y_velocity=0.0,
        theta_velocity=0.0
    ):
        # Get current position of arm
        observation = self.robot.get_observation()

        action = {
            key: value
            for key, value in observation.items()
            if key.endswith(".pos")
        }

        # Update only base velocities and send previous arm positions back
        action.update({
            "x.vel": x_velocity,
            "y.vel": y_velocity,
            "theta.vel": theta_velocity
        })

        self.robot.send_action(action)

    def disconnect(self):
        self.robot.disconnect()