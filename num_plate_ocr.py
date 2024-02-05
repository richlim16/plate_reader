import cv2
from paddleocr import PaddleOCR
from IPython.display import Image
from time import time

detector = cv2.CascadeClassifier("model/haarcascade_russian_plate_number.xml")

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
it_timeout = 2
plate_count = 0

reader = PaddleOCR(lang='en')
known_plates = ["Y10477", "GAP3520"]

def capture_plate(plate_count, img_roi, reader):
    cv2.imwrite("plates/scanned_img_" + str(plate_count) + ".jpg", img_roi)
    output = reader.ocr('plates/scanned_img_' + str(plate_count) + '.jpg')

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
                                    str1 = str1.replace(" ","")
                                    str1 = str1.upper()
                                    if str1 in known_plates:
                                        print(" Plate Recognized! "+str1)


while True:
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    threshold_img = cv2.threshold(gray, 0, 255, cv2.THRESH_TOZERO)[1]
    plates = detector.detectMultiScale(threshold_img, 1.05, 4)

    if(len(plates) > 0):
        plate_found = True
        for (x, y, w, h) in plates:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 255), 2)
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
                    cv2.putText(frame, "License Plate", (x, y-5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 255), 2)
                    img_roi = gray[y: y+h, x: x+w]
                    cv2.imshow("License Plate", img_roi)
                    capture_plate(plate_count, img_roi, reader)
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
   