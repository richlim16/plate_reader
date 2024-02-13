# this program just detects cars and then plates, but does not read them
#currently plate reader only exists to put a plate and to show that a plate exists in the frame
# because the frame passed is not a crop of the plate, but a crop of the car

import cv2
from paddleocr import PaddleOCR
from time import time
from glob import glob
import numpy as np

car_detector = cv2.CascadeClassifier("model/cars2.xml")
plate_detector = cv2.CascadeClassifier("model/haarcascade_russian_plate_number.xml")
reader = PaddleOCR(lang='en', show_log=False, use_angle_cls=True)

cap = cv2.VideoCapture("video_3_30fps.mp4")
# cap = cv2.VideoCapture(0)
min_size = 000
count = len(glob("plates/*"))

it_started = False
ot_started = False
car_found = False
in_time = 0
out_time = 0
ot_timeout = 3
it_timeout = 1
timeout = 5

known_plates = [["", 0]]

# change parameters, will now pass output instead of the reader itself
def capture_plate(plate_count, img_roi, output):
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
                            for x in o: #out[0][1][0]
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
                                                    cv2.putText(img_roi, str1, (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                                                    cv2.imshow("img roi", img_roi)
                                                    cv2.imwrite("plates/scanned_img_" + str(plate_count) + ".jpg", img_roi)
                                                else:
                                                    print("Plate "+str1+" IGNORED")
                                                    break
                                            else:
                                                index += 1

                                        if index == len(known_plates):
                                            known_plates.append([str1, time()])
                                            print("appending "+str1)
                                            cv2.putText(img_roi, str1, (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                                            cv2.imshow("img roi", img_roi)
                                            cv2.imwrite("plates/scanned_img_" + str(plate_count) + ".jpg", img_roi)
                                            break

while True:
    ret, frame = cap.read()

    try:    
        cars = car_detector.detectMultiScale(image=frame, scaleFactor=1.1, minNeighbors=8, minSize=(150,150))

        if not it_started and (len(cars) > 0):
            in_time = time()
            it_started = True

        elif not ot_started:
            out_time = time()
            ot_started = True

        elif it_started and (time() - in_time >= it_timeout) and (len(cars) > 0):
            for (x, y, w, h) in cars:
                if w*h >= min_size:
                    # cv2.putText(frame, str(w*h), (x,y-5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 255), 2)
                    cv2.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0), 2)
                    car_frame = frame[y:y+h, x:x+w] # Cropped frame of the car

                    plates = plate_detector.detectMultiScale(car_frame, 1.05, 4)

                    if (len(plates) > 0):
                        for (a, b, c, d) in plates:
                            a = x+a
                            b = y+b
                            # cv2.putText(frame, "Plate", (a,b-5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 255), 2)
                            cv2.rectangle(frame, (a, b), (a+c, b+d), (255, 0, 0), 1) 
                            output = reader.ocr(car_frame)
                            capture_plate(count, car_frame, output)
                            count+=1

                

        cv2.imshow("Frame", frame)

        if cv2.waitKey(1) & 0xFF == ord('x'):
            break

    except:
        break

print(known_plates)
cap.release()
cv2.destroyAllWindows()