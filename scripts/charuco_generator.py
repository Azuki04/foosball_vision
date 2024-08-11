import cv2

ARUCO_DICT = cv2.aruco.DICT_6X6_250
SQUARES_VERTICALLY = 7
SQUARES_HORIZONTALLY = 5
SQUARE_LENGTH = 30  
MARKER_LENGTH = 15  
MARGIN_PX = 20  

IMG_SIZE = (2480, 3508)  
OUTPUT_NAME = 'ChArUco_Marker_A4.png'

def create_and_save_new_board():
    dictionary = cv2.aruco.getPredefinedDictionary(ARUCO_DICT)
    board = cv2.aruco.CharucoBoard(
        (SQUARES_HORIZONTALLY, SQUARES_VERTICALLY),
        SQUARE_LENGTH / 25.4,  
        MARKER_LENGTH / 25.4,  
        dictionary
    )

    img = board.generateImage(IMG_SIZE, MARGIN_PX, 1)

    cv2.imwrite(OUTPUT_NAME, img)

    print(f"ChArUco-Board as {OUTPUT_NAME} saved")


create_and_save_new_board()
