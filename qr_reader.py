import cv2
from qrtools import QR

cap = cv2.VideoCapture(1)

while True:
    ret, frame = cap.read()

    my_qr = QR(frame)
    my_qr.decode()
    print(my_qr.data)

    if cv2.waitKey(1) & 0xFF == ord('x'):
        break

cap.release()