import cv2
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from ultralytics import YOLO

from computer_vision.utils.camera_setup import CameraSetup
from computer_vision.utils.path_manager import get_weight, get_config


class BallTracker:
    def __init__(self, weight_path='best.pt'):
        self.model = YOLO(weight_path)
        self.model.fuse()

        self.ball_class_index = 0

        self.pos_list_x, self.pos_list_y = [], []
        self.max_positions = 5

        self.last_position = None

    def detect_frames(self, frame):
        results = self.model(frame)[0]
        detections = results.boxes

        ball_detections = [d for d in detections if int(d.cls[0]) == self.ball_class_index]

        if ball_detections:
            if self.last_position is not None:
                max_distance = np.hypot(frame.shape[1], frame.shape[0])

                min_combined_score = float('inf')
                selected_ball = None
                for ball in ball_detections:
                    x1, y1, x2, y2 = ball.xyxy[0].cpu().numpy()
                    center_x = int((x1 + x2) / 2)
                    center_y = int((y1 + y2) / 2)
                    distance = np.hypot(center_x - self.last_position[0], center_y - self.last_position[1])
                    normalized_distance = distance / max_distance

                    confidence = ball.conf[0].item()

                    alpha = 0.5
                    beta = 0.5
                    score = alpha * normalized_distance - beta * confidence

                    if score < min_combined_score:
                        min_combined_score = score
                        selected_ball = ball
            else:
                selected_ball = max(ball_detections, key=lambda x: x.conf[0])

            x1, y1, x2, y2 = selected_ball.xyxy[0].cpu().numpy()
            center_x = int((x1 + x2) / 2)
            center_y = int((y1 + y2) / 2)
            self.last_position = (center_x, center_y)

            self.pos_list_x.append(center_x)
            self.pos_list_y.append(center_y)

            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 0), 2)
            cv2.circle(frame, (center_x, center_y), 5, (0, 255, 0), cv2.FILLED)
        else:
            print("FEHLER: Ball nicht gefunden!")
            self.interpolate_missing_values()
            self.last_position = None

        if len(self.pos_list_x) > self.max_positions:
            self.pos_list_x.pop(0)
            self.pos_list_y.pop(0)

        if len(self.pos_list_x) >= 3:
            self.calculate_shot_direction(frame)

        self.draw_ball_path(frame)

        return frame

    def interpolate_missing_values(self):
        if self.pos_list_x:
            data = {'x': self.pos_list_x, 'y': self.pos_list_y}
            df = pd.DataFrame(data)
            df = df.interpolate(method='linear').bfill().ffill()
            self.pos_list_x, self.pos_list_y = df['x'].tolist(), df['y'].tolist()

    @staticmethod
    def weighted_linear_regression(time_steps, ball_positions) -> LinearRegression:
        weights = np.exp(np.linspace(0, 1, len(time_steps)))
        model = LinearRegression()
        model.fit(time_steps, ball_positions, sample_weight=weights)
        return model

    def calculate_shot_direction(self, frame) -> None:
        time_steps = np.array(range(len(self.pos_list_x))).reshape(-1, 1)
        ball_positions_x = np.array(self.pos_list_x).reshape(-1, 1)
        ball_positions_y = np.array(self.pos_list_y).reshape(-1, 1)

        reg_x = self.weighted_linear_regression(time_steps, ball_positions_x)
        reg_y = self.weighted_linear_regression(time_steps, ball_positions_y)

        direction_slope_x = reg_x.coef_[0][0]
        direction_slope_y = reg_y.coef_[0][0]

        future_position_x = int(self.pos_list_x[-1] + direction_slope_x * 10)
        future_position_y = int(self.pos_list_y[-1] + direction_slope_y * 10)

        current_position = (self.pos_list_x[-1], self.pos_list_y[-1])
        future_position = (future_position_x, future_position_y)
        cv2.arrowedLine(frame, current_position, future_position, (0, 0, 255), 3)

        print(f"Direction vector: ({direction_slope_x}, {direction_slope_y})")

    def draw_ball_path(self, frame):
        if self.pos_list_x and self.pos_list_y:
            for i, (posX, posY) in enumerate(zip(self.pos_list_x, self.pos_list_y)):
                pos = (posX, posY)
                cv2.circle(frame, pos, 5, (0, 255, 0), cv2.FILLED)
                if i >= 1:
                    cv2.line(frame, pos, (self.pos_list_x[i - 1], self.pos_list_y[i - 1]), (0, 255, 0), 2)


if __name__ == "__main__":

    print(get_config("camera_calibration.yaml"))
    ball_tracker_camera_setup = CameraSetup(0, 640, 480, 60, calibration_file=get_config("camera_calibration.yaml"))

    ball_tracker_test = BallTracker(weight_path=get_weight("yolo11n-best.pt"))

    while True:
        ball_tracker_frame = ball_tracker_camera_setup.get_frame()
        if ball_tracker_frame is None:
            break

        processed_frame = ball_tracker_test.detect_frames(ball_tracker_frame)

        cv2.imshow("Ball Tracker", processed_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    ball_tracker_camera_setup.release()
    cv2.destroyAllWindows()
