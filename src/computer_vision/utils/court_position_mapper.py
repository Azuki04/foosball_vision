import numpy as np
import cv2


class CourtPositionMapper:
    def __init__(self, court_width, court_height):
        self.court_width = court_width
        self.court_height = court_height
        self.homography_matrix = None

    def update_homography(self, court_pts):

        if court_pts is not None:
            dst_pts = np.array([[0, 0],
                                [self.court_width, 0],
                                [self.court_width, self.court_height],
                                [0, self.court_height]], dtype='float32')
            self.homography_matrix, _ = cv2.findHomography(court_pts, dst_pts)
        else:
            self.homography_matrix = None

    def map_ball_position_to_court_coordinates(self, ball_pos_x, ball_pos_y):

        if self.homography_matrix is not None:
            ball_pos_image = np.array([[ball_pos_x, ball_pos_y]], dtype='float32').reshape(-1, 1, 2)
            ball_pos_court = cv2.perspectiveTransform(ball_pos_image, self.homography_matrix)
            ball_court_x, ball_court_y = ball_pos_court[0][0]
            return ball_court_x, ball_court_y
        else:
            print("Homography not available, cannot map ball position to court coordinates")
            return None, None
