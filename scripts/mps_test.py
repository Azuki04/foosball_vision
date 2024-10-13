from ultralytics import YOLO
import torch


def main():
    print(torch.backends.mps.is_available())
    # yolov5su, yolov8x, yolov10x, yolov10s, yolov11n, yolov11s, yolov11m, yolov11l, yolov11x
    model = YOLO('../weights/yolo11n-best.pt')

    source = 0
    # device="mps"
    model.predict(source=source, imgsz=640, save=False, show=True)


if __name__ == '__main__':
    main()
