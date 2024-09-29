from computer_vision.utils.camera_setup import CameraSetup
from computer_vision.trackers.ball_tracker import BallTracker
from constants import (CAMERA_ID, FPS, CAMERA_WIDTH, CAMERA_HEIGHT)
from computer_vision.utils.path_manager import get_config
import cv2
import cvzone


def main():
    camera_setup = CameraSetup(CAMERA_ID, CAMERA_WIDTH, CAMERA_HEIGHT, FPS, calibration_file=get_config("camera_calibration.yml"))

    ball_tracker = BallTracker()

    while True:
        frame = camera_setup.get_frame()
        if frame is None:
            break

        img_color, mask, img_contours = ball_tracker.detect_frames(frame)


        img_stack = cvzone.stackImages([frame, img_color, mask, img_contours], 2, 1)
        cv2.imshow("Ball tracking", img_stack)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    camera_setup.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
