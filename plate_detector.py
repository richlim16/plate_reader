# this program atttemps to detect plates then read them after a certain timeout period

import cv2
import cvzone
from paddleocr import PaddleOCR
from IPython.display import Image
from time import time

car_detector = cv2.CascadeClassifier("model/cars.xml")
plate_detector = cv2.CascadeClassifier("model/haarcascade_russian_plate_number.xml")

cap = cv2.VideoCapture(1)
cap.set(3, 640)  # height
cap.set(4, 480) # height
min_area = 0

in_time = 0
it_started = False
out_time = 0
ot_started = False
plate_found = False
ot_timeout = 3
it_timeout = 1
plate_count = 0

reader = PaddleOCR(lang='en')
known_plates = ["Y10477", "GAP3520"]

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
                            for x in o: #out[0][1][0]
                                if isinstance(x, str):
                                    str1 = x
                                    str1 = str1.replace(" ","") #remove spaces
                                    str1 = str1.upper()
                                    if len(str1) >= 6:
                                        print("PLATE : "+str1)
                                        plate_str = str1
                                        return plate_str
                                        # cv2.putText(img_roi, str1, (10, 10), cv2.FONT_HERSHEY_COMPLEX_SMALL, .5, (255, 0, 0), 2)
                                        # cv2.imshow("img roi", img_roi)
                                        # cv2.imwrite("plates/scanned_img_" + str(plate_count) + ".jpg", img_roi)
                                        


while True:
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    threshold_img = cv2.threshold(gray, 0, 255, cv2.THRESH_TOZERO)[1]
    plates = plate_detector.detectMultiScale(threshold_img, 1.05, 4)

    if(len(plates) > 0):
        plate_found = True
        for (x, y, w, h) in plates:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 255), 2)
            car_frame = frame[y:y+h, x:x+w]
            output = reader.ocr(car_frame)
            plate_str = capture_plate(output)
            cvzone.putTextRect(frame, f'{plate_str}', [x + 8, y - 12], thickness=1, scale=1)
    else:
        plate_found = False

    # Timer Started
    if plate_found and not it_started:
        in_time = time()
        it_started = True

    elif not plate_found and not ot_started:
        out_time = time()
        ot_started = True

    elif plate_found and it_started:
        # if plate found longer than timeout
        if time() - in_time >= it_timeout:

            for (x, y, w, h) in plates:
                area = w * h

                if area > min_area:
                    img_roi = threshold_img[y: y+h, x: x+w]
                    # cv2.imshow("License Plate", img_roi)
                    # capture_plate(plate_count, img_roi, reader)
                    plate_count += 1
                    ot_started = False
                    it_started = False

    # timed out
    elif ot_started and time() - out_time >= ot_timeout:
        it_started = False
        ot_started = False

    cv2.imshow("Camera", frame)

    if cv2.waitKey(1) & 0xFF == ord('x'):
        break

cap.release()
cv2.destroyAllWindows()
   
