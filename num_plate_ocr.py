from time import time
import math
from ultralytics import YOLO
from paddleocr import PaddleOCR
import cv2
import cvzone

cap = cv2.VideoCapture('video_60fps.mp4')

model = YOLO('./model/another.pt')
classnames = ['license-plate','vehicle']
reader = PaddleOCR(lang='en', show_log=False, use_angle_cls=True)

it_started = False
ot_started = False
car_found = False
in_time = 0
out_time = 0
ot_timeout = 3
it_timeout = 1
timeout = 5
plate_num = ''
known_plates=[]

def capture_plate(output):
    for out in output:
        if out is None:
            pass
        else:
            for ou in out:
                if ou is None:
                    pass
                else:
                    for o in ou:
                        if o is None:
                            pass
                        else:
                            for x in o:
                                if isinstance(x, str):
                                    str1 = x
                                    str1 = str1.replace(" ","") #remove spaces
                                    str1 = str1.upper()
                                    if len(str1) >= 6:
                                        index = 0

                                        while index < len(known_plates):
                                            if known_plates[index][0] == str1:
                                                if time() - known_plates[index][1] > timeout:
                                                    known_plates[index][1] = time()
                                                    print("Plate "+str1+" recorded")
                                                    return str1
                                                else:
                                                    print("Plate "+str1+" IGNORED")
                                                    return str1
                                            else:
                                                index += 1

                                        if index == len(known_plates):
                                            known_plates.append([str1, time()])
                                            print("appending "+str1)
                                            return str1

while True:
    ret, frame = cap.read()
    frame = cv2.resize(frame, (1080,720))
    results = model(frame)

    for info in results:
        parameters = info.boxes
        for box in parameters:
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            confidence = box.conf[0]
            class_detect = box.cls[0]
            class_detect = int(class_detect)
            class_detect = classnames[class_detect]
            conf = math.ceil(confidence * 100)
            if conf > 50 and class_detect == 'license-plate':
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                car_frame = frame[y1:y2, x1:x2]
                output = reader.ocr(car_frame)
                plate_num = capture_plate(output)
                cvzone.putTextRect(frame, f'{plate_num}', [x1 + 8, y1 - 12], thickness=1, scale=1)

    cv2.imshow('video', frame)
    if cv2.waitKey(1) & 0xFF == ord('x'):
        break

cap.release()
cv2.destroyAllWindows()