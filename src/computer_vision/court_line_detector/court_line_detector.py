import cv2
import numpy as np
import cvzone
from computer_vision.utils.camera_setup import CameraSetup
from computer_vision.utils.path_manager import get_config
from cvzone.ColorModule import ColorFinder

class CourtLineDetector:
    def __init__(self):
        # Create the color finder object
        self.my_color_finder = ColorFinder(False)
        self.hsv_vals = {'hmin': 35, 'smin': 40, 'vmin': 40, 'hmax': 85, 'smax': 255, 'vmax': 255}
        self.last_pts = None

    def get_mask(self, frame):
        img_color, mask = self.my_color_finder.update(frame, self.hsv_vals)
        mask = cv2.GaussianBlur(mask, (5, 5), 0)
        kernel = np.ones((40, 40), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        return img_color, mask

    def find_largest_contour(self, mask):
        # Find contours in the mask
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            contours = sorted(contours, key=cv2.contourArea, reverse=True)
            for contour in contours:
                epsilon = 0.02 * cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, epsilon, True)
                # We are looking for a quadrilateral (a rectangle or trapezoid)
                if len(approx) == 4 and cv2.contourArea(approx) > 5000:
                    return np.array(approx, dtype='float32')
        return None

    def draw_contours(self, frame, pts):
        # Draw contours as lines connecting the points
        for i in range(len(pts)):
            p1 = tuple(map(int, pts[i][0]))
            p2 = tuple(map(int, pts[(i + 1) % len(pts)][0]))
            cv2.line(frame, p1, p2, (0, 255, 0), 3)

    def draw_key_points(self, frame, pts):
        # Draw key points as circles with labels
        for i, point in enumerate(pts):
            x, y = map(int, point[0])
            cv2.circle(frame, (x, y), 10, (0, 0, 255), -1)
            cv2.putText(frame, f'P{i + 1}', (x + 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    def detect_frames(self, frame):
        img_colour, mask = self.get_mask(frame)

        pts = self.find_largest_contour(mask)
        if pts is not None:
            self.last_pts = pts

        if self.last_pts is not None:
            self.draw_contours(frame, self.last_pts)
            self.draw_key_points(frame, self.last_pts)

        return img_colour, mask, frame



if __name__ == "__main__":
    # Option to choose video or camera
    use_camera = False  # Set to True to use the camera, False to use a video

    # If using a video file
    video_path = '../../../data/raw/input_videos/foosball_1_phone.mp4'  # Replace with your video path

    court_line_detector = CourtLineDetector()  # Instance of CourtLineDetector

    if use_camera:
        # Setup for live camera
        print(get_config("camera_calibration.yml"))
        court_line_detector_camera_setup = CameraSetup(0, 640, 480, 60, calibration_file=get_config("camera_calibration.yml"))

        while True:
            court_line_detector_frame = court_line_detector_camera_setup.get_frame()  # Get frame from camera
            if court_line_detector_frame is None:
                break

            # Call detect_frames using the CourtLineDetector instance and pass the frame
            court_line_detector_mask, court_line_detector_img_contours, court_line_detector_output_frame = court_line_detector.detect_frames(court_line_detector_frame)

            img_stack = cvzone.stackImages([court_line_detector_frame, court_line_detector_mask, court_line_detector_img_contours], 2, 1)
            cv2.imshow("Court detection", img_stack)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        court_line_detector_camera_setup.release()
    else:
        # Setup for video file
        cap = cv2.VideoCapture(video_path)

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Call detect_frames using the CourtLineDetector instance and pass the frame
            court_line_detector_mask, court_line_detector_img_contours, court_line_detector_output_frame = court_line_detector.detect_frames(frame)

            img_stack = cvzone.stackImages([frame, court_line_detector_mask, court_line_detector_img_contours], 2, 1)
            cv2.imshow("Court detection", img_stack)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()

    cv2.destroyAllWindows()