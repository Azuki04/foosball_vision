import cv2
import numpy as np

class CourtLineDetector:
    def __init__(self):
        ...
  
    def apply_perspective_transform(frame, src_pts):
        width, height = frame.shape[1], frame.shape[0]
        dst_pts = np.array([
            [0, 0],
            [width - 1, 0],
            [width - 1, height - 1],
            [0, height - 1]
        ], dtype='float32')
        matrix = cv2.getPerspectiveTransform(src_pts, dst_pts)
        warped_frame = cv2.warpPerspective(frame, matrix, (width, height))
        return warped_frame


    def preprocess_frame(frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_green = np.array([35, 40, 40])
        upper_green = np.array([85, 255, 255])
        mask = cv2.inRange(hsv, lower_green, upper_green)
        kernel = np.ones((30, 30), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        return mask


    def find_largest_contour(mask):
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            contours = sorted(contours, key=cv2.contourArea, reverse=True)
            for contour in contours:
                epsilon = 0.02 * cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, epsilon, True)
                if len(approx) == 4 and cv2.contourArea(approx) > 5000:
                    return np.array(approx, dtype='float32')
        return None


    def draw_contours(frame, pts):
        for i in range(len(pts)):
            p1 = tuple(map(int, pts[i][0]))
            p2 = tuple(map(int, pts[(i + 1) % len(pts)][0]))
            cv2.line(frame, p1, p2, (0, 255, 0), 3)


    def draw_key_points(frame, pts):
        for i, point in enumerate(pts):
            x, y = map(int, point[0])
            cv2.circle(frame, (x, y), 10, (0, 0, 255), -1)
            cv2.putText(frame, f'P{i + 1}', (x + 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)


    # Öffne das Video
    video = cv2.VideoCapture('../../../data/raw/input_videos/foosball.mp4')

    if not video.isOpened():
        print("Error: Could not open video.")
        exit()

    # Variablen für das Tracking
    last_pts = None

    while True:
        ret, frame = video.read()

        if not ret:
            break

        mask = preprocess_frame(frame)
        cv2.imshow('Mask', mask)

        pts = find_largest_contour(mask)

        if pts is not None:
            last_pts = pts

        if last_pts is not None:
            draw_contours(frame, last_pts)
            draw_key_points(frame, last_pts)
            warped_frame = apply_perspective_transform(frame, last_pts)
            cv2.imshow('Warped Foosball Court', warped_frame)

        cv2.imshow('Foosball Court Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video.release()
    cv2.destroyAllWindows()
    

if __name__ == "__main__":
    CourtLineDetector()


