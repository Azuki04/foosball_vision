import cv2
import cvzone
import numpy as np
import pandas as pd
from cvzone.ColorModule import ColorFinder
from sklearn.linear_model import LinearRegression

from computer_vision.constants import BALL_HSV_VALS
from computer_vision.utils.camera_setup import CameraSetup
from computer_vision.utils.path_manager import get_config


class BallTracker:
    def __init__(self, hsv_vals, debug=False):
        self.my_color_finder = ColorFinder(debug)
        self.hsv_vals =  hsv_vals
        self.pos_list_x, self.pos_list_y = [], []
        self.max_positions = 5

    def detect_frames(self, frame):
        img_color, mask = self.get_mask(frame)

        img_contours, contours = cvzone.findContours(frame, mask, minArea=300, maxArea=6000, filter=[8,9,10])

        if contours:
            self.pos_list_x.append(contours[0]['center'][0])
            self.pos_list_y.append(contours[0]['center'][1])
        else:
            print("ERROR: Ball not found!")
            self.interpolate_missing_values()

        if len(self.pos_list_x) > self.max_positions:
            self.pos_list_x.pop(0)
            self.pos_list_y.pop(0)

        if len(self.pos_list_x) >= 3:
            self.calculate_shot_direction(img_contours)

        self.draw_ball_path(img_contours)

        return img_color, mask, img_contours

    def get_mask(self, frame):
        img_color, mask = self.my_color_finder.update(frame, self.hsv_vals)
        mask = cv2.GaussianBlur(mask, (3, 3), 0)
        kernel = np.ones((3, 3), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        return img_color, mask

    def interpolate_missing_values(self):
        if self.pos_list_x:
            data = {'x': self.pos_list_x, 'y': self.pos_list_y}
            df = pd.DataFrame(data)
            df = df.interpolate(method='linear').bfill().ffill()
            self.pos_list_x, self.pos_list_y = df['x'].tolist(), df['y'].tolist()

    @staticmethod
    def weighted_linear_regression(time_steps, ball_positions) -> LinearRegression:
        weights = np.exp(np.linspace(0, 1, len(time_steps)))  # Weight from 1 to e (exponential increase)
        # weights = np.linspace(1, 2, len(x))  # Weight from 1 to 2 (linear increase)
        model = LinearRegression()
        model.fit(time_steps, ball_positions, sample_weight=weights)
        return model

    def calculate_shot_direction(self, img) -> None:
        time_steps = np.array(range(len(self.pos_list_x))).reshape(-1, 1)
        ball_positions_x = np.array(self.pos_list_x).reshape(-1, 1)
        ball_positions_y = np.array(self.pos_list_y).reshape(-1, 1)

        reg_x = self.weighted_linear_regression(time_steps, ball_positions_x)
        reg_y = self.weighted_linear_regression(time_steps, ball_positions_y)

        direction_slope_x = reg_x.coef_[0][0]  # Slope for X coordinate (delta X per time unit)
        direction_slope_y = reg_y.coef_[0][0]  # Slope for Y coordinate (delta Y per time unit)

        future_position_x = int(self.pos_list_x[-1] + direction_slope_x * 10)  # Predicting 10 steps ahead in X
        future_position_y = int(self.pos_list_y[-1] + direction_slope_y * 10)  # Predicting 10 steps ahead in Y

        current_position = (self.pos_list_x[-1], self.pos_list_y[-1])
        future_position = (future_position_x, future_position_y)
        cv2.arrowedLine(img, current_position, future_position, (0, 0, 255), 3)

        print(f"Direction vector: ({direction_slope_x}, {direction_slope_y})")

    def draw_ball_path(self, img_contours):
        if self.pos_list_x and self.pos_list_y:
            for i, (posX, posY) in enumerate(zip(self.pos_list_x, self.pos_list_y)):
                pos = (posX, posY)
                cv2.circle(img_contours, pos, 5, (0, 255, 0), cv2.FILLED)
                if i >= 1:
                    cv2.line(img_contours, pos, (self.pos_list_x[i - 1], self.pos_list_y[i - 1]), (0, 255, 0), 2)


if __name__ == "__main__":

    print(get_config("camera_calibration.yaml"))
    ball_tracker_camera_setup = CameraSetup(0, 640, 480, 60, calibration_file=get_config("camera_calibration.yaml"))

    ball_tracker_test = BallTracker(BALL_HSV_VALS)

    while True:
        ball_tracker_frame = ball_tracker_camera_setup.get_frame()
        if ball_tracker_frame is None:
            break

        ball_tracker_img_color, ball_tracker_mask, ball_tracker_img_contours = ball_tracker_test.detect_frames(ball_tracker_frame)

        img_stack = cvzone.stackImages([ball_tracker_frame, ball_tracker_img_color, ball_tracker_mask, ball_tracker_img_contours], 2, 1)
        cv2.imshow("Ball tracking", img_stack)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    ball_tracker_camera_setup.release()
    cv2.destroyAllWindows()
