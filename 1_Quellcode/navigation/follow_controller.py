"""
This script determines the command needed to control to the robot to follow the x and z position
of a desired point in 3D e.g. Marker center point.
x and z needs to be in local frame of the robot
"""


class FollowController:
    def __init__(
        self,
        target_distance=0.70,
        distance_tolerance=0.05,
        lateral_tolerance=0.05
    ):
        self.target_distance = target_distance
        self.distance_tolerance = distance_tolerance
        self.lateral_tolerance = lateral_tolerance

    def get_command(self, x, z):
        if x < -self.lateral_tolerance:
            return "MOVE_LEFT"

        if x > self.lateral_tolerance:
            return "MOVE_RIGHT"

        if z > self.target_distance + self.distance_tolerance:
            return "MOVE_FORWARD"

        if z < self.target_distance - self.distance_tolerance:
            return "MOVE_BACKWARD"

        return "STOP"