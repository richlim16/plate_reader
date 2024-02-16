# License Plate Reader

### How to Get Started
1. Install Conda
2. *in this path*\
 `conda env create -f env.yml`\
 `conda activate sampleenv`
3. python ***filename.py***
    - num_plate_ocr.py
    - plate_detector2.py
    - cars_detector2.py

## num_plate_ocr.py

### Explanation of Code
1. Program captures input feed from webcam
2. feed is given to the plate detector ( using YOLOv8 ) to detect the plates in a given frame
3. the coordinates for the plate/s detected are used to create a rectangle around the detected plate/s
4. if time elapsed for detection exceeds timeout then the frame a frame is taken and given to the ocr ( using PaddleOCR ) to be read and checked against *known_plates*
5. If plate is recognized the program prints **Plate Recognized!**

## plate_detector2.py

### Explanation of Code
1. Program captures input feed from webcam
2. feed is turned to grayscale, then gray frames are given to the plate detector ( using HaarCascade ) to detect the plates in a given frame
    - turing to gray scale can be adjusted ( in case want more aggressive bordering of details)
    - Plate detection can be adjusted also via nearest neighbors (4), and scale (1.05)
3. the coordinates for the plate/s detected are used to create a rectangle around the detected plate/s
4. if time elapsed for detection exceeds timeout then the frame a frame is taken and given to the ocr ( using PaddleOCR ) to be read and checked against *known_plates*
5. If plate is recognized the program prints **Plate Recognized!**

## cars_detector2.py

### Explanation of Code
1. Program captures input feed from webcam
2. feed is turned to grayscale, then gray frames are given to the vehicle detector ( using HaarCascade ) to detect the vehicles in a given frame
    - turing to gray scale can be adjusted ( in case want more aggressive bordering of details)
    - Vehicle detection can be adjusted also via nearest neighbors (4), and scale (1.05)
3. the coordinates for the vehicle/s detected are used to create a rectangle around the detected vehicle/s
4. if time elapsed for detection exceeds timeout then the frame a frame is taken and given to the ocr ( using PaddleOCR ) to be read and checked against *known_plates*
5. If plate is recognized the program prints **Plate Recognized!**
