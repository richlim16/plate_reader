# # this program detects the car then reads anything from the given picture

# import cv2
# from paddleocr import PaddleOCR
# from IPython.display import Image
# from time import time
# from glob import glob

# car_detector = cv2.CascadeClassifier("model/cars.xml")

# cap = cv2.VideoCapture(1)
# cap.set(3, 640)  # height
# cap.set(4, 480) # height
# min_area = 800

# plate_count = len(glob("plates/*"))
# car_count = len(glob("cars/*"))

# it_started = False
# ot_started = False
# car_found = False
# in_time = 0
# out_time = 0
# ot_timeout = 3
# it_timeout = 1
# timeout = 5

# known_plates = [["VX9153", 0]]

# reader = PaddleOCR(lang='en', show_log=False)

# # change parameters, will now pass output instead of the reader itself
# def capture_plate(plate_count, img_roi, output):
#     for out in output:
#         if out is None:
#             pass
#         else:
#             for ou in out:
#                 if ou is None:
#                     pass
#                 else:
#                     for o in ou:
#                         if o is None:
#                             pass
#                         else:
#                             for x in o: #out[0][1][0]
#                                 if isinstance(x, str):
#                                     str1 = x
#                                     str1 = str1.replace(" ","") #remove spaces
#                                     str1 = str1.upper()

#                                     index = 0

#                                     while index < len(known_plates):
#                                         if known_plates[index][0] == str1:
#                                             if time() - known_plates[index][1] > timeout:
#                                                 known_plates[index][1] = time()
#                                                 print("Plate "+str1+" recorded")
#                                             else:
#                                                 print("Plate "+str1+" IGNORED")
#                                                 break
#                                         else:
#                                             index += 1

#                                     if index == len(known_plates):
#                                         print("appending "+str1)
#                                         known_plates.append([str1, time()])
#                                         break
#                                     # if len(str1) >= 6:
#                                     #     print("PLATE : "+str1)
#                                     #     cv2.putText(img_roi, str1, (10, 10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 0), 2)
#                                     #     cv2.imshow("img roi", img_roi)
#                                     #     cv2.imwrite("plates/scanned_img_" + str(plate_count) + ".jpg", img_roi)

# while True:
#     ret, frame = cap.read()

#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     threshold_img = cv2.threshold(gray, 0, 255, cv2.THRESH_TOZERO)[1]
#     cars = car_detector.detectMultiScale(threshold_img, 1.1, 8)


#     if(len(cars) > 0):
#         cars = cars[0]
#         car_found = True
#         x,y,w,h = cars
#         cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 255), 2)

#     else:
#         car_found = False

#     if car_found and not it_started:
#         in_time = time()
#         it_started = True

#     elif not car_found and not ot_started:
#         out_time = time()
#         ot_started = True
    
#     elif car_found and it_started:
#         if time() - in_time >= it_timeout:
#             img_roi = threshold_img[y: y+h, x: x+w]
#             output = reader.ocr(img_roi)
#             capture_plate(plate_count, img_roi, output)
#             plate_count += 1
#             it_started = False
#             ot_started = False
#             in_time = time()
#             ot_time = time()

#     elif ot_started and time() - out_time >= ot_timeout:
#         it_started = False
#         ot_started = False

#     cv2.imshow("Camera", frame)

#     if cv2.waitKey(1) & 0xFF == ord('x'):
#         break

# cap.release()
# cv2.destroyAllWindows()

# print(known_plates)

import cv2
from pyzbar.pyzbar import decode
import time

cam = cv2.VideoCapture(0)
cam.set(3, 640)
cam.set(4, 480)

camera = True
while camera == True:
    success, frame = cam.read()

    for i in decode(frame):
        print(i.type)
        print(i.data.decode('utf-8'))
        time.sleep(5)

        cv2.imshow("QR Scanner", frame)
        cv2.waitKey(3)