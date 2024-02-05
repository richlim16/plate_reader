# How to get Started
1. Install Conda
2. *in this path*\
 `conda env create -f env.yml`\
 `conda activate sampleenv`
3. python num_plate_ocr.py

# Explanation of Code
1. Program captures input feed from webcam
2. feed is turned to grayscale, then gray frames are given to plate detector ( using HaarCascade ) to detect the plates in a given frame
    - turing to gray scale can be adjusted ( in case want more aggressive bordering of details)
    - Plate detection can be adjusted also via nearest neighbors (4), and scale (1.05)

3. the coordinates for the plate/s detected are used to create a rectangle around the detected plate/s
4. if time elapsed for detection exceeds timeout then the frame a frame is taken and given to ocr to be read and checked against *known_plates*
5. If plate is recognized the program prints **Plate Recognized!**