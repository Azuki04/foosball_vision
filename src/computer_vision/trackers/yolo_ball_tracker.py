import cv2
import numpy as np
from ultralytics import YOLO

from computer_vision.prediction.ball_shot_predictor import BallPredictor
from computer_vision.utils.camera_setup import CameraSetup
from computer_vision.utils.path_manager import get_weight, get_config


class BallTracker:
    def __init__(self, weight_path='best.pt'):
        self.model = YOLO(weight_path)
        self.model.fuse()

        self.ball_class_index = 0

        self.predictor = BallPredictor()

        self.current_x = None
        self.current_y = None

        self.last_position = None

    def detect_frames(self, frame):
        results = self.model(frame)[0]
        detections = results.boxes

        ball_detections = [d for d in detections if int(d.cls[0]) == self.ball_class_index]

        if ball_detections:
            centers, confidences = self.extract_ball_info(ball_detections)

            if self.last_position is not None:
                selected_index = self.select_best_ball(centers, confidences, frame)
            else:
                selected_index = np.argmax(confidences)

            selected_ball = ball_detections[selected_index]
            center_x, center_y = centers[selected_index]


            self.last_position = (center_x, center_y)
            self.current_x = int(center_x)
            self.current_y = int(center_y)


            self.predictor.add_position(self.current_x, self.current_y)

            self.draw_selected_ball(frame, selected_ball, self.current_x, self.current_y)
        else:
            print("Ball not detected")
            self.predictor.interpolate_missing_values()
            self.last_position = None
            self.current_x = self.predictor.pos_list_x[-1] if self.predictor.pos_list_x else None
            self.current_y = self.predictor.pos_list_y[-1] if self.predictor.pos_list_y else None

        self.predictor.calculate_shot_direction(frame)
        self.predictor.draw_ball_path(frame)
        return frame


    def extract_ball_info(self, ball_detections):
        centers = []
        confidences = []
        for ball in ball_detections:
            x1, y1, x2, y2 = ball.xyxy[0].cpu().numpy()
            center_x = (x1 + x2) / 2
            center_y = (y1 + y2) / 2
            centers.append((center_x, center_y))
            confidences.append(ball.conf[0].item())
        centers = np.array(centers)
        confidences = np.array(confidences)
        return centers, confidences

    def select_best_ball(self, centers, confidences, frame):
        last_pos_array = np.array(self.last_position)
        distances = np.linalg.norm(centers - last_pos_array, axis=1)
        max_distance = np.hypot(frame.shape[1], frame.shape[0])
        normalized_distances = distances / max_distance

        alpha = 0.5
        beta = 0.5
        scores = alpha * normalized_distances - beta * confidences

        min_index = np.argmin(scores)
        return min_index

    def draw_selected_ball(self, frame, selected_ball, center_x, center_y):
        x1, y1, x2, y2 = selected_ball.xyxy[0].cpu().numpy()
        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 0), 2)
        cv2.circle(frame, (center_x, center_y), 5, (0, 255, 0), cv2.FILLED)

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
