import cv2
from typing import Final


ARUCO_DICT: Final[int] = cv2.aruco.DICT_6X6_250
SQUARES_VERTICALLY: Final[int] = 7
SQUARES_HORIZONTALLY: Final[int] = 5
SQUARE_LENGTH: Final[int] = 30  
MARKER_LENGTH: Final[int] = 15  
MARGIN_PX: Final[int] = 20  

IMG_SIZE = (2480, 3508)  
OUTPUT_PATH: Final[str] = '../data/processed/charuco/ChArUco_Maker_A4.png'

def create_and_save_new_board():
    dictionary = cv2.aruco.getPredefinedDictionary(ARUCO_DICT)
    board = cv2.aruco.CharucoBoard(
        (SQUARES_HORIZONTALLY, SQUARES_VERTICALLY),
        SQUARE_LENGTH / 25.4,  
        MARKER_LENGTH / 25.4,  
        dictionary
    )

    img = board.generateImage(IMG_SIZE, MARGIN_PX, 1)

    cv2.imwrite(OUTPUT_PATH, img)

    print(f"ChArUco-Board as {OUTPUT_PATH} saved")


create_and_save_new_board()
