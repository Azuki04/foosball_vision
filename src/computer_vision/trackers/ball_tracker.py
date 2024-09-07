import cv2
import cvzone
from cvzone.ColorModule import ColorFinder
import numpy as np
from sklearn.linear_model import LinearRegression
import pandas as pd


class BallTracker:
    def __init__(self):
        # Initialize the Video
        self.cap = cv2.VideoCapture(0)

        # Create the color Finder object
        self.my_color_finder = ColorFinder(False)
        self.hsv_vals = {'hmin': 24, 'smin': 107, 'vmin': 127, 'hmax': 179, 'smax': 255, 'vmax': 255}

        # Variables to store ball positions
        self.pos_list_x, self.pos_list_y = [], []
        self.max_positions = 5  # Number of positions to track for regression and interpolation

    def detect_frames(self):
        while True:
            success, img = self.cap.read()
            img = img[0:900, :]

            # Display
            img = cv2.resize(img, (0, 0), None, 0.7, 0.7)

            # Process the image using the ColorFinder update method
            img_color, mask = self.my_color_finder.update(img, self.hsv_vals)

            # Find contours
            img_contours, contours = cvzone.findContours(img, mask, minArea=500,maxArea=600, filter=[8])

            # Track the ball if contours are found
            if contours:
                self.pos_list_x.append(contours[0]['center'][0])
                self.pos_list_y.append(contours[0]['center'][1])
            else:
                # If no contours, use previous positions for interpolation
                print("Ball not found!")
                self.interpolate_missing_values()

            # Keep only the last 'max_positions' positions for the regression
            if len(self.pos_list_x) > self.max_positions:
                self.pos_list_x.pop(0)
                self.pos_list_y.pop(0)

            # Calculate the direction of the ball using linear regression
            if len(self.pos_list_x) >= 3:
                self.calculate_shot_direction(img_contours)

            # Draw the tracked points and lines
            self.draw_ball_path(img_contours)

            # Stack the images
            img_stack = cvzone.stackImages([img, img_color, mask, img_contours], 2, 1)

            # Display the image with contours
            cv2.imshow("Image", img_stack)

            # Break the loop if the 'q' key is pressed
            if cv2.waitKey(85) & 0xFF == ord('q'):
                break

        # Release the video capture and close all windows
        self.cap.release()
        cv2.destroyAllWindows()

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
        # Prepare data for weighted linear regression
        time_steps = np.array(range(len(self.pos_list_x))).reshape(-1, 1)  # Time step (independent variable)
        ball_positions_x = np.array(self.pos_list_x).reshape(-1, 1)  # X positions
        ball_positions_y = np.array(self.pos_list_y).reshape(-1, 1)  # Y positions

        # Apply weighted linear regression to both X and Y coordinates
        reg_x = self.weighted_linear_regression(time_steps, ball_positions_x)
        reg_y = self.weighted_linear_regression(time_steps, ball_positions_y)

        # Calculate the direction vector (slope of the regression line)
        direction_slope_x = reg_x.coef_[0][0]  # Slope for X coordinate (delta X per time unit)
        direction_slope_y = reg_y.coef_[0][0]  # Slope for Y coordinate (delta Y per time unit)

        # Calculate future position (for visualization purposes)
        future_position_x = int(self.pos_list_x[-1] + direction_slope_x * 10)  # Predicting 10 steps ahead in X
        future_position_y = int(self.pos_list_y[-1] + direction_slope_y * 10)  # Predicting 10 steps ahead in Y

        # Draw a line showing the predicted direction
        current_position = (self.pos_list_x[-1], self.pos_list_y[-1])
        future_position = (future_position_x, future_position_y)
        cv2.arrowedLine(img, current_position, future_position, (0, 0, 255), 3)

        # Print the slope (direction vector)
        print(f"Direction vector: ({direction_slope_x}, {direction_slope_y})")

    def draw_ball_path(self, img_contours):
        if self.pos_list_x and self.pos_list_y:
            for i, (posX, posY) in enumerate(zip(self.pos_list_x, self.pos_list_y)):
                pos = (posX, posY)
                # Draw a circle at each point
                cv2.circle(img_contours, pos, 5, (0, 255, 0), cv2.FILLED)
                # Draw lines between points
                if i >= 1:
                    cv2.line(img_contours, pos, (self.pos_list_x[i - 1], self.pos_list_y[i - 1]), (0, 255, 0), 2)


if __name__ == "__main__":
    BallTracker().detect_frames()
