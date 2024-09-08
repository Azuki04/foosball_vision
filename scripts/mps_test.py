from ultralytics import YOLO
import torch

def main():

    print(torch.backends.mps.is_available())

    model = YOLO('yolov10n.pt')

    source = 0
    model.predict(source=source, imgsz=640, save=False, show=True, device="mps")

if __name__ == '__main__':
    main()



