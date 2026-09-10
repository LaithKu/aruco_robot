"""
This script is used to generate ArUco markers with different IDs in different sizes and save them as png
"""

import cv2


def main():
    marker_id = 0
    marker_size = 500

    # Use 4X4 Standard Dictionary with IDs from 0 to 49
    aruco_dictionary = cv2.aruco.getPredefinedDictionary(
        cv2.aruco.DICT_4X4_50
    )

    marker_image = cv2.aruco.generateImageMarker(
        aruco_dictionary,
        marker_id,
        marker_size
    )

    # Save image as png to local file
    output_path = f"aruco_marker_{marker_id}.png"

    cv2.imwrite(output_path, marker_image)

    print(f"Marker saved as {output_path}")


if __name__ == "__main__":
    main()