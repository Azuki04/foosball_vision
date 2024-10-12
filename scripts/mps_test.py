from ultralytics import YOLO
import torch

def main():

    print(torch.backends.mps.is_available())

    model = YOLO('../data/processed/model/yolo11n-best.pt')

    source = 0
    #device="mps"
    model.predict(source=source, imgsz=640, save=False, show=True)

if __name__ == '__main__':
    main()



