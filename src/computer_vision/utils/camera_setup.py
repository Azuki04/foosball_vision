import cv2
import numpy as np
import yaml


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
        if calibration_file:
            self.load_calibration(calibration_file)

    def load_calibration(self, calibration_file):
        """Loads the calibration data from a YAML file."""
        with open(calibration_file, 'r') as file:
            calibration_data = yaml.safe_load(file)
            self.camera_matrix = np.array(calibration_data['camera_matrix']['data']).reshape(3, 3)
            self.dist_coeffs = np.array(calibration_data['dist_coeff']['data']).reshape(1, 5)

    def undistort_frame(self, frame):
        """Applies the calibration to undistort the frame."""
        if self.camera_matrix is not None and self.dist_coeffs is not None:
            h, w = frame.shape[:2]
            new_camera_matrix, roi = cv2.getOptimalNewCameraMatrix(self.camera_matrix, self.dist_coeffs, (w, h), 1,
                                                                   (w, h))
            undistorted_frame = cv2.undistort(frame, self.camera_matrix, self.dist_coeffs, None, new_camera_matrix)
            x, y, w, h = roi
            undistorted_frame = undistorted_frame[y:y + h, x:x + w]
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
        """Called when the object is destroyed to release the camera"""
        self.release()
