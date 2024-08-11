import numpy as np
import cv2 as cv
import glob

# 1. Calibration Settings
# Number of internal corners on the chessboard (not the number of squares)
CORNERS_X = 7  # Number of corners along the width (horizontal)
CORNERS_Y = 7  # Number of corners along the height (vertical)

# Size of a chessboard square in millimeters
SQUARE_SIZE_MM = 20  # Adjust this to your chessboard square size

# Termination criteria for refining corner detection (accuracy and iterations)
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# 2. Prepare Object Points
# 3D points in real-world space based on the actual square size
object_points_template = np.zeros((CORNERS_X * CORNERS_Y, 3), np.float32)
object_points_template[:, :2] = np.mgrid[0:CORNERS_X, 0:CORNERS_Y].T.reshape(-1, 2) * SQUARE_SIZE_MM

# Arrays to store 3D object points and 2D image points from all calibration images
object_points = []  # Real-world 3D points
image_points = []   # Corresponding 2D points in image plane

# 3. Load Calibration Images
# Specify the path to your calibration images
CALIBRATION_IMAGES_PATH = '../data/raw/calibration/*.jpg'
images = sorted(glob.glob(CALIBRATION_IMAGES_PATH))

# 4. Process Each Image
for image_file in images:
    image = cv.imread(image_file)
    gray_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    # Find chessboard corners
    found, corners = cv.findChessboardCorners(gray_image, (CORNERS_X, CORNERS_Y), None)

    if found:
        object_points.append(object_points_template)

        # Refine corner detection for better accuracy
        refined_corners = cv.cornerSubPix(gray_image, corners, (11, 11), (-1, -1), criteria)
        image_points.append(refined_corners)

        # Visual feedback: Draw and display the corners
        cv.drawChessboardCorners(image, (CORNERS_X, CORNERS_Y), refined_corners, found)
        cv.imshow('Chessboard Corners', image)
        cv.waitKey(500)  # Display for 500ms (you can adjust this)

# 5. Camera Calibration
# Use the detected points to calibrate the camera
sample_image = cv.imread(images[0])
image_height, image_width = sample_image.shape[:2]
ret, camera_matrix, distortion_coefficients, rotation_vectors, translation_vectors = cv.calibrateCamera(
    object_points, image_points, (image_width, image_height), None, None
)

# 6. Save Calibration Results
# Save the camera matrix and distortion coefficients for future use
RESULT_OUTPUT_PATH = "../config/calibration.yml"
calibration_file = cv.FileStorage(RESULT_OUTPUT_PATH, cv.FILE_STORAGE_WRITE)
calibration_file.write("camera_matrix", camera_matrix)
calibration_file.write("distortion_coefficients", distortion_coefficients)
calibration_file.release()

# 7. Display an Undistorted Example Image
optimal_camera_matrix, roi = cv.getOptimalNewCameraMatrix(camera_matrix, distortion_coefficients, (image_width, image_height), 1, (image_width, image_height))
undistorted_image = cv.undistort(sample_image, camera_matrix, distortion_coefficients, None, optimal_camera_matrix)

# Optionally crop the image to the valid region of interest (ROI)
x, y, w, h = roi
undistorted_image_cropped = undistorted_image[y:y + h, x:x + w]

# Display the original and undistorted images
cv.imshow('Original Image', sample_image)
cv.imshow('Undistorted Image', undistorted_image_cropped)
cv.waitKey(0)
cv.destroyAllWindows()
