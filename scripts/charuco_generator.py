import cv2
import numpy as np
from typing import Final
import os

# Constants
ARUCO_DICT: Final[int] = cv2.aruco.DICT_6X6_250
SQUARES_X: Final[int] = 7  # Number of squares along the X-axis
SQUARES_Y: Final[int] = 5  # Number of squares along the Y-axis
SQUARE_LENGTH_MM: Final[float] = 30.0  # Square length in millimeters
MARKER_LENGTH_MM: Final[float] = 15.0  # Marker length in millimeters
OUTPUT_PATH: Final[str] = '../data/processed/charuco/ChArUco_Board_A4.png'


def create_and_save_charuco_board():
    # Create dictionary and Charuco board
    aruco_dict = cv2.aruco.getPredefinedDictionary(ARUCO_DICT)

    # Instantiate CharucoBoard directly
    board = cv2.aruco.CharucoBoard(
        size=(SQUARES_X, SQUARES_Y),
        squareLength=SQUARE_LENGTH_MM,
        markerLength=MARKER_LENGTH_MM,
        dictionary=aruco_dict
    )

    # Calculate image size to maintain board proportions
    dpi = 300  # Dots per inch for printing
    mm_to_inch = 1 / 25.4
    img_width = int(SQUARES_X * SQUARE_LENGTH_MM * mm_to_inch * dpi)
    img_height = int(SQUARES_Y * SQUARE_LENGTH_MM * mm_to_inch * dpi)
    img_size = (img_width, img_height)

    # Generate the Charuco board image
    board_image = board.generateImage(
        outSize=img_size,
        marginSize=0,
        borderBits=1
    )

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    # Save the image
    cv2.imwrite(OUTPUT_PATH, board_image)
    print(f"ChArUco board saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    create_and_save_charuco_board()
