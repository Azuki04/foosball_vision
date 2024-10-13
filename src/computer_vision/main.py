import cv2
import cvzone

from computer_vision.court_line_detector import CourtLineDetector
from computer_vision.trackers.yolo_ball_tracker import BallTracker
from computer_vision.utils.camera_setup import CameraSetup
from computer_vision.utils.court_position_mapper import CourtPositionMapper
from computer_vision.utils.path_manager import get_config, get_weight
from constants import (CAMERA_ID, FPS, CAMERA_WIDTH, CAMERA_HEIGHT, COURT_HEIGHT, COURT_WIDTH, COURT_HSV_VALS)


def main():
    # Initialize camera, ball tracker, court detector, and court mapper
    camera_setup = CameraSetup(
        CAMERA_ID, CAMERA_WIDTH, CAMERA_HEIGHT, FPS,
        calibration_file=get_config("camera_calibration.yaml"))

    ball_tracker = BallTracker(weight_path=get_weight("yolo11n-best.pt"))
    court_detector = CourtLineDetector(COURT_HSV_VALS)
    court_mapper = CourtPositionMapper(COURT_WIDTH, COURT_HEIGHT)

    while True:
        frame = camera_setup.get_frame()
        if frame is None:
            break

        # Detect court
        img_colour, mask, img_contours = court_detector.detect_frames(frame)
        court_pts = court_detector.court_pts
        court_mapper.update_homography(court_pts)

        # Detect ball
        img_contours = ball_tracker.detect_frames(frame)

        if ball_tracker.pos_list_x and ball_tracker.pos_list_y:
            ball_x, ball_y = ball_tracker.pos_list_x[-1], ball_tracker.pos_list_y[-1]

            ball_court_x, ball_court_y = court_mapper.map_ball_position_to_court_coordinates(ball_x, ball_y)
            if ball_court_x is not None and ball_court_y is not None:
                # TODO: send ball position to arduino
                print(f"Ball position in court coordinates: ({ball_court_x:.2f}, {ball_court_y:.2f})")
        else:
            print("Ball not detected.")

        # Display images
        img_stack = cvzone.stackImages([frame, img_colour, mask, img_contours], 2, 1)
        cv2.imshow("Ball tracking and court detection", img_stack)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    camera_setup.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
