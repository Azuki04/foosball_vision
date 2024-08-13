import cv2
import numpy as np
import sys
import argparse


def initialize_trackbar(window_name: str) -> None:
    """Initialize trackbars for HSV calibration."""
    cv2.createTrackbar('HMin', window_name, 0, 179, lambda x: None)
    cv2.createTrackbar('SMin', window_name, 0, 255, lambda x: None)
    cv2.createTrackbar('VMin', window_name, 0, 255, lambda x: None)
    cv2.createTrackbar('HMax', window_name, 179, 179, lambda x: None)
    cv2.createTrackbar('SMax', window_name, 255, 255, lambda x: None)
    cv2.createTrackbar('VMax', window_name, 255, 255, lambda x: None)


def get_trackbar_values(window_name: str) -> tuple:
    """Retrieve the current positions of the HSV trackbars."""
    h_min: int = cv2.getTrackbarPos('HMin', window_name)
    s_min: int = cv2.getTrackbarPos('SMin', window_name)
    v_min: int = cv2.getTrackbarPos('VMin', window_name)
    h_max: int = cv2.getTrackbarPos('HMax', window_name)
    s_max: int = cv2.getTrackbarPos('SMax', window_name)
    v_max: int = cv2.getTrackbarPos('VMax', window_name)
    return h_min, s_min, v_min, h_max, s_max, v_max


def display_hsv_values(h_min: int, s_min: int, v_min: int, h_max: int, s_max: int, v_max: int, previous_values: tuple) -> tuple:
    """Display the HSV values if they have changed."""
    if (h_min, s_min, v_min, h_max, s_max, v_max) != previous_values:
        print(f"(hMin = {h_min}, sMin = {s_min}, vMin = {v_min}), "
              f"(hMax = {h_max}, sMax = {s_max}, vMax = {v_max})")
        return h_min, s_min, v_min, h_max, s_max, v_max
    return previous_values


def process_frame(frame, window_name: str, previous_values: tuple) -> tuple:
    """Process the given frame, apply HSV mask and show the result."""
    h_min, s_min, v_min, h_max, s_max, v_max = get_trackbar_values(window_name)

    lower_hsv = np.array([h_min, s_min, v_min])
    upper_hsv = np.array([h_max, s_max, v_max])
    hsv_img = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv_img, lower_hsv, upper_hsv)
    output_img = cv2.bitwise_and(frame, frame, mask=mask)

    previous_values = display_hsv_values(h_min, s_min, v_min, h_max, s_max, v_max, previous_values)

    cv2.imshow(window_name, output_img)
    return previous_values


def main(video_path: str=None, image_path: str=None) -> None:
    window_name:str = 'HSV-Calibration'
    cv2.namedWindow(window_name)
    initialize_trackbar(window_name)

    previous_values: tuple = (0, 0, 0, 179, 255, 255)

    if i is not None:
        try:
            video_path = int(video_path)
        except ValueError:
            pass 

        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print("Error: Could not open video file or webcam.")
            sys.exit()

        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not read frame.")
                break

            previous_values: tuple = process_frame(frame, window_name, previous_values)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()

    elif image_path:
        img = cv2.imread(image_path)
        if img is None:
            print("Error: Could not open image file.")
            sys.exit()

        while True:
            previous_values: tuple = process_frame(img, window_name, previous_values)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='HSV Calibration Tool')
    parser.add_argument('--video', type=str, help='Path to the video file or "0" for webcam')

    parser.add_argument('--image', type=str, help='Path to the image file')
    args = parser.parse_args()

    if args.video:
        main(video_path=args.video)
    elif args.image:
        main(image_path=args.image)
    else:
        print("Error: Please provide either a video path or an image path.")
        sys.exit()
