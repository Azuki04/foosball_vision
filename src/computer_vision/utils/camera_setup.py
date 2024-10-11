import cv2
import numpy as np
import yaml


def opencv_matrix_constructor(loader, node):
    matrix_data = loader.construct_mapping(node, deep=True)
    rows = matrix_data['rows']
    cols = matrix_data['cols']
    data = matrix_data['data']
    matrix = np.array(data, dtype=np.float64).reshape((rows, cols))
    return matrix

yaml.add_constructor('tag:yaml.org,2002:opencv-matrix', opencv_matrix_constructor, Loader=yaml.SafeLoader)

class CameraSetup:
    def __init__(self, camera_id, width, height, fps, calibration_file=None):
        self.camera_id = camera_id
        self.width = width
        self.height = height
        self.fps = fps

        self.cap = cv2.VideoCapture(camera_id)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.cap.set(cv2.CAP_PROP_FPS, fps)

        self.camera_matrix = None
        self.dist_coeffs = None
        self.new_camera_matrix = None  # To store the optimal new camera matrix

        if calibration_file:
            self.load_calibration(calibration_file)

    def load_calibration(self, calibration_file):
        """Loads the calibration data from a YAML file."""
        with open(calibration_file, 'r') as file:
            calibration_data = yaml.safe_load(file)
            self.camera_matrix = calibration_data['camera_matrix']
            self.dist_coeffs = calibration_data['distortion_coefficients']

        self.new_camera_matrix, _ = cv2.getOptimalNewCameraMatrix(
            self.camera_matrix, self.dist_coeffs, (self.width, self.height), 1, (self.width, self.height)
        )
        print('Calibration data loaded successfully.')

    def undistort_frame(self, frame):
        """Applies the calibration to undistort the frame."""
        if self.camera_matrix is not None and self.dist_coeffs is not None:
            undistorted_frame = cv2.undistort(frame, self.camera_matrix, self.dist_coeffs, None, self.new_camera_matrix)
            print('Frame is undistorted')
            return undistorted_frame
        print('Frame is not undistorted')
        return frame

    def get_frame(self):
        """Reads a frame from the camera and applies undistortion if calibration is available."""
        ret, frame = self.cap.read()
        if ret:
            return self.undistort_frame(frame)
        return None

    def release(self):
        """Releases the camera."""
        self.cap.release()

    def __del__(self):
        """Called when the object is destroyed to release the camera."""
        self.release()