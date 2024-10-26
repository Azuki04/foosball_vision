import cv2
import cvzone
import numpy as np
from cvzone.ColorModule import ColorFinder

from computer_vision.constants import COURT_HSV_VALS
from computer_vision.utils.camera_setup import CameraSetup
from computer_vision.utils.path_manager import get_config


class CourtLineDetector:
    def __init__(self, hsv_vals, debug=False):
        self.my_color_finder = ColorFinder(debug)
        self.hsv_vals = hsv_vals
        self.last_pts = None
        self.court_pts = None

    def get_mask(self, frame):
        img_color, mask = self.my_color_finder.update(frame, self.hsv_vals)
        mask = cv2.GaussianBlur(mask, (5, 5), 0)
        kernel = np.ones((40, 40), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        return img_color, mask

    def find_largest_contour(self, mask):
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            contours = sorted(contours, key=cv2.contourArea, reverse=True)
            for contour in contours:
                epsilon = 0.02 * cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, epsilon, True)
                if len(approx) == 4 and cv2.contourArea(approx) > 5000:
                    return np.array(approx, dtype='float32')
        return None

    def draw_contours(self, frame, pts):
        for i in range(len(pts)):
            p1 = tuple(map(int, pts[i]))
            p2 = tuple(map(int, pts[(i + 1) % len(pts)]))
            cv2.line(frame, p1, p2, (0, 255, 0), 3)

    def draw_key_points(self, frame, pts):
        for i, point in enumerate(pts):
            x, y = map(int, point)
            cv2.circle(frame, (x, y), 10, (0, 0, 255), -1)
            cv2.putText(frame, f'P{i + 1}', (x + 10, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    def order_points(self, pts):
        rect = np.zeros((4, 2), dtype="float32")
        s = pts.sum(axis=1)
        rect[1] = pts[np.argmin(s)]
        rect[3] = pts[np.argmax(s)]
        diff = np.diff(pts, axis=1)
        rect[0] = pts[np.argmin(diff)]
        rect[2] = pts[np.argmax(diff)]
        return rect

    def detect_frames(self, frame, update_court_pts=True):
        img_colour, mask = self.get_mask(frame)

        if update_court_pts:
            pts = self.find_largest_contour(mask)
            if pts is not None:
                pts = self.order_points(pts.reshape(4, 2))
                self.last_pts = pts
                self.court_pts = pts

        if self.last_pts is not None:
            self.draw_contours(frame, self.last_pts)
            self.draw_key_points(frame, self.last_pts)

        return img_colour, mask, frame


if __name__ == "__main__":
    use_camera = False

    video_path = '../../../data/raw/input_videos/foosball_1_phone.mp4'

    court_line_detector = CourtLineDetector(COURT_HSV_VALS)

    if use_camera:
        print(get_config("camera_calibration.yaml"))
        court_line_detector_camera_setup = CameraSetup(0, 640, 480, 60, calibration_file=get_config("camera_calibration.yaml"))

        while True:
            court_line_detector_frame = court_line_detector_camera_setup.get_frame()
            if court_line_detector_frame is None:
                break

            court_line_detector_mask, court_line_detector_img_contours, court_line_detector_output_frame = court_line_detector.detect_frames(court_line_detector_frame)

            img_stack = cvzone.stackImages([court_line_detector_frame, court_line_detector_mask, court_line_detector_img_contours], 2, 1)
            cv2.imshow("Court detection", img_stack)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        court_line_detector_camera_setup.release()
    else:
        cap = cv2.VideoCapture(video_path)

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            court_line_detector_mask, court_line_detector_img_contours, court_line_detector_output_frame = court_line_detector.detect_frames(frame)

            img_stack = cvzone.stackImages([frame, court_line_detector_mask, court_line_detector_img_contours], 2, 1)
            cv2.imshow("Court detection", img_stack)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()

    cv2.destroyAllWindows()