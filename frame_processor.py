from ultralytics import YOLO
import cv2
import math
import cvzone

class FrameProcess:
    def __init__(self):
        self.model = YOLO('best.pt')
        self.classnames = ['fire', 'smoke']
        self.informations = []

    def process_frame(self, frame):
        result = self.model(frame, stream=True)

        


        for info in result:
            boxes = info.boxes
            for box in boxes:
                confidence = box.conf[0]
                confidence = math.ceil(confidence * 100)
                Class = int(box.cls[0])
                if confidence > 50:
                    x1, y1, x2, y2 = box.xyxy[0]
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 5)
                    cvzone.putTextRect(frame, f'{self.classnames[Class]} {confidence}%', [x1 + 8, y1 + 100],scale=1.5, thickness=2)
                    self.informations.append([confidence, frame])

        return frame
