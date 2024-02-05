import cv2

import cv2
from paddleocr import PaddleOCR
from IPython.display import Image
from time import time

car_detector = cv2.CascadeClassifier("model/cars.xml")
plate_detector = cv2.CascadeClassifier("model/haarcascade_russian_plate_number.xml")

cap = cv2.VideoCapture("sample_vid_1.mp4")
reader = PaddleOCR(lang='en')

in_time = 0
it_started = False
out_time = 0
ot_started = False
plate_found = False
ot_timeout = 3
it_timeout = 1
cars_count = 0
plate_count = 0

def capture_plate(plate_count, img_roi, reader):
    output = reader.ocr(img_roi)

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
                                        print("PLATE : "+str1)
                                        cv2.putText(img_roi, str1, (20, 20), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 0), 2)
                                        cv2.imwrite("plates/scanned_img_" + str(plate_count) + ".jpg", img_roi)

while True:
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cars = car_detector.detectMultiScale(gray, 1.1, 8)

    if(len(cars) > 0):
        plate_found = True
        for(x,y,w,h) in cars:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 255), 2)

    else:
        plate_found = False

    #Timer Started
    if plate_found and not it_started:
        in_time = time()
        it_started = True
    
    elif not plate_found and not ot_started:
        out_time = time()
        ot_started = True

    elif plate_found and it_started:
        if time() - in_time >= it_timeout:

            for(x,y,w,h) in cars:
                cv2.putText(frame, "Car", (x, y-5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 255), 2)
                car_frame = frame[y: y+h, x:x+w]
                cv2.imwrite("cars/sample_img_"+str(cars_count)+".jpg", car_frame)
                cars_count += 1
                cv2.imshow("CAR", car_frame)

                threshold_img = cv2.threshold(car_frame, 0, 255, cv2.THRESH_TOZERO)[1]
                plates = plate_detector.detectMultiScale(threshold_img, 1.05, 4)

                for (a, b, c, d) in plates:
                    cv2.putText(car_frame, "Plate", (a,b-5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 255), 2)
                    cv2.rectangle(car_frame, (a, b), (a+c, b+d), (0, 255, 0), 2)
                    img_roi = threshold_img[b:b+d, a:a+c]
                    capture_plate(plate_count, img_roi, reader)
                    plate_count += 1

    elif ot_started and time() - out_time >= ot_timeout:
        it_started = False
        ot_started = False

    cv2.imshow("Camera", frame)

    if cv2.waitKey(1) & 0xFF == ord('x'):
        break

cap.release()
cv2.destroyAllWindows()
