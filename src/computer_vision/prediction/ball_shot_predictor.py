import cv2
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

class BallPredictor:
    def __init__(self, max_positions=5):
        self.pos_list_x = []
        self.pos_list_y = []
        self.max_positions = max_positions

    def add_position(self, x, y):
        self.pos_list_x.append(x)
        self.pos_list_y.append(y)

        if len(self.pos_list_x) > self.max_positions:
            self.pos_list_x.pop(0)
            self.pos_list_y.pop(0)

    def interpolate_missing_values(self):
        if self.pos_list_x:
            data = {'x': self.pos_list_x, 'y': self.pos_list_y}
            df = pd.DataFrame(data)
            df = df.interpolate(method='linear').bfill().ffill()
            self.pos_list_x, self.pos_list_y = df['x'].tolist(), df['y'].tolist()

    @staticmethod
    def weighted_linear_regression(time_steps, ball_positions) -> LinearRegression:
        weights = np.exp(np.linspace(0, 1, len(time_steps)))
        # weights = np.linspace(1, 2, len(x))  # Weight from 1 to 2 (linear increase)
        model = LinearRegression()
        model.fit(time_steps, ball_positions, sample_weight=weights)
        return model

    def calculate_shot_direction(self, frame):
        if len(self.pos_list_x) >= 3:
            time_steps = np.array(range(len(self.pos_list_x))).reshape(-1, 1)
            ball_positions_x = np.array(self.pos_list_x).reshape(-1, 1)
            ball_positions_y = np.array(self.pos_list_y).reshape(-1, 1)

            reg_x = self.weighted_linear_regression(time_steps, ball_positions_x)
            reg_y = self.weighted_linear_regression(time_steps, ball_positions_y)

            direction_slope_x = reg_x.coef_[0][0]
            direction_slope_y = reg_y.coef_[0][0]

            future_position_x = int(self.pos_list_x[-1] + direction_slope_x * 10)
            future_position_y = int(self.pos_list_y[-1] + direction_slope_y * 10)

            current_position = (int(self.pos_list_x[-1]), int(self.pos_list_y[-1]))
            future_position = (future_position_x, future_position_y)
            cv2.arrowedLine(frame, current_position, future_position, (0, 0, 255), 3)

            #print(f"Direction: ({direction_slope_x}, {direction_slope_y})")

    def draw_ball_path(self, frame):
        if self.pos_list_x and self.pos_list_y:
            for i, (posX, posY) in enumerate(zip(self.pos_list_x, self.pos_list_y)):
                pos = (int(posX), int(posY))
                cv2.circle(frame, pos, 5, (0, 255, 0), cv2.FILLED)
                if i >= 1:
                    cv2.line(frame, pos, (int(self.pos_list_x[i - 1]), int(self.pos_list_y[i - 1])), (0, 255, 0), 2)
