import cv2


def open_camera(camera_index=0):
    """
    Opens a camera and returns the OpenCV VideoCapture object.
    """

    camera = cv2.VideoCapture(camera_index)

    if not camera.isOpened():
        raise RuntimeError(f"Could not open camera with index {camera_index}")

    return camera