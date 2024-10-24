import cv2
import cvzone

from computer_vision.court_line_detector import CourtLineDetector
from computer_vision.trackers.yolo_ball_tracker import BallTracker
from computer_vision.utils.camera_setup import CameraSetup
from computer_vision.utils.court_position_mapper import CourtPositionMapper
from computer_vision.utils.path_manager import get_config, get_weight
from computer_vision.utils.serial_sender import SerialSender
from constants import (CAMERA_ID, FPS, CAMERA_WIDTH, CAMERA_HEIGHT, COURT_HEIGHT, COURT_WIDTH, COURT_HSV_VALS, SERIAL_URL, BAUD_RATE)


def main():
    # Initialize camera, ball tracker, court detector, and court mapper
    camera_setup = CameraSetup(
        CAMERA_ID, CAMERA_WIDTH, CAMERA_HEIGHT, FPS,
        calibration_file=get_config("camera_calibration.yaml"))

    ball_tracker = BallTracker(weight_path=get_weight("yolo11n-best.pt"))
    court_detector = CourtLineDetector(COURT_HSV_VALS)
    court_mapper = CourtPositionMapper(COURT_WIDTH, COURT_HEIGHT)
    sender = SerialSender(SERIAL_URL, BAUD_RATE)

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

        if ball_tracker.current_x and ball_tracker.current_y:
            ball_court_x, ball_court_y = court_mapper.map_ball_position_to_court_coordinates(ball_tracker.current_x, ball_tracker.current_y)
            if ball_court_x is not None and ball_court_y is not None:
                sender.send_current_coordinate(ball_court_x, ball_court_y)
                print(f"Ball position in court coordinates: ({ball_court_x:.2f}, {ball_court_y:.2f})")
        else:
            print("ERROR: Ball not detected.")

        # Display images
        img_stack = cvzone.stackImages([frame, img_colour, mask, img_contours], 2, 1)
        cv2.imshow("Ball tracking and court detection", img_stack)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    sender.close()
    camera_setup.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
