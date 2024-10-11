from typing import Final
import numpy as np
import cvzone
import cv2 as cv
import glob
import os

# 1. Calibration Settings
ARUCO_DICT_TYPE: Final[int] = cv.aruco.DICT_6X6_250
BOARD_SQUARES_X: Final[int] = 7  # Number of squares along the X-axis
BOARD_SQUARES_Y: Final[int] = 5  # Number of squares along the Y-axis
SQUARE_LENGTH_MM: Final[float] = 30.0  # Square length in millimeters
MARKER_LENGTH_MM: Final[float] = 15.0  # Marker length in millimeters

# 2. Create the ChArUco board
aruco_dict = cv.aruco.getPredefinedDictionary(ARUCO_DICT_TYPE)
board = cv.aruco.CharucoBoard(
    size=(BOARD_SQUARES_X, BOARD_SQUARES_Y),
    squareLength=SQUARE_LENGTH_MM,
    markerLength=MARKER_LENGTH_MM,
    dictionary=aruco_dict
)

# 3. Create Detector Parameters
detector_params = cv.aruco.DetectorParameters()
charuco_params = cv.aruco.CharucoParameters()
charuco_detector = cv.aruco.CharucoDetector(board, charuco_params, detector_params)

# 4. Prepare Arrays to Store Object Points and Image Points
all_obj_points = []  # 3D points in real world space
all_img_points = []  # 2D points in image plane
image_size = None  # To store image size

# 5. Load Calibration Images
CALIBRATION_IMAGES_PATH: Final[str] = '../data/raw/calibration/*.JPG'
images = sorted(glob.glob(CALIBRATION_IMAGES_PATH))

if not images:
    print("No calibration images found. Check the path.")
    exit()

# Get the 3D coordinates of all the ChArUco corners
chessboard_corners = board.getChessboardCorners()  # List of Point3f
chessboard_corners = np.array(chessboard_corners)  # Convert to numpy array

# 6. Process Each Image
for image_file in images:
    image = cv.imread(image_file)
    if image is None:
        print(f"Image could not be loaded: {image_file}")
        continue

    gray_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    if image_size is None:
        image_size = gray_image.shape[::-1]

    # Detect markers and Charuco corners
    charuco_corners, charuco_ids, marker_corners, marker_ids = charuco_detector.detectBoard(gray_image)

    if charuco_ids is not None and len(charuco_ids) > 0:
        # Build object points and image points
        obj_points = []
        img_points = []

        for i in range(len(charuco_ids)):
            corner_id = charuco_ids[i][0]  # Get the id of the corner
            obj_point = chessboard_corners[corner_id]  # Get the corresponding 3D point
            img_point = charuco_corners[i][0]  # Get the 2D image point

            obj_points.append(obj_point)
            img_points.append(img_point)

        all_obj_points.append(np.array(obj_points, dtype=np.float32))
        all_img_points.append(np.array(img_points, dtype=np.float32))

        # Visual feedback
        cv.aruco.drawDetectedMarkers(image, marker_corners, marker_ids)
        cv.aruco.drawDetectedCornersCharuco(image, charuco_corners, charuco_ids)

        cv.imshow('Detected Markers and Charuco Corners', image)
        cv.waitKey(500)
    else:
        print(f"No Charuco corners detected in image: {image_file}")

cv.destroyAllWindows()

# 7. Camera Calibration
if len(all_obj_points) == 0 or len(all_img_points) == 0:
    print("No Charuco corners detected. Calibration cannot be performed.")
    exit()

ret, camera_matrix, distortion_coefficients, rotation_vectors, translation_vectors = cv.calibrateCamera(
    objectPoints=all_obj_points,
    imagePoints=all_img_points,
    imageSize=image_size,
    cameraMatrix=None,
    distCoeffs=None
)

print("Camera matrix:\n", camera_matrix)
print("Distortion coefficients:\n", distortion_coefficients)

# 8. Save Calibration Results
RESULT_OUTPUT_PATH: Final[str] = "../config/camera_calibration.yaml"
os.makedirs(os.path.dirname(RESULT_OUTPUT_PATH), exist_ok=True)
calibration_file = cv.FileStorage(RESULT_OUTPUT_PATH, cv.FILE_STORAGE_WRITE)
calibration_file.write("camera_matrix", camera_matrix)
calibration_file.write("distortion_coefficients", distortion_coefficients)
calibration_file.release()
print(f"Calibration data saved to {RESULT_OUTPUT_PATH}")

# 9. Display an Undistorted Example Image
sample_image = cv.imread(images[0])
if sample_image is None:
    print("Sample image could not be loaded.")
    exit()

image_height, image_width = sample_image.shape[:2]
optimal_camera_matrix, roi = cv.getOptimalNewCameraMatrix(camera_matrix, distortion_coefficients,
                                                          (image_width, image_height), 1, (image_width, image_height))
undistorted_image = cv.undistort(sample_image, camera_matrix, distortion_coefficients, None, optimal_camera_matrix)

# Optionally crop the image to the valid region of interest (ROI)
x, y, w, h = roi
undistorted_image_cropped = undistorted_image[y:y + h, x:x + w]

# Display the original and undistorted images
img_stack = cvzone.stackImages([sample_image, undistorted_image_cropped], 2, 1)
cv.imshow("original image ------------------------------ cropped image", img_stack)
cv.waitKey(0)
cv.destroyAllWindows()
