import numpy as np
import cv2

# define a video capture object
# vid = cv2.VideoCapture(0)
# vid.set(cv2.CAP_PROP_FRAME_WIDTH, 1920) # max 3840 for 4K, 1920 for FHD
# vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080) # max 2160 for 4K, 1080 for FHD

# # Capture the video frame
# # by frame
# ret, image = vid.read()
image = cv2.imread('images/board1.jpg')
cv2.imshow('image',image)
cv2.waitKey(0)
original = image.copy()
image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
lower = np.array([50, 40, 90], dtype="uint8") # blue values detected by https://imagecolorpicker.com/en
upper = np.array([200, 250, 250], dtype="uint8") # blue
#lower = np.array([130, 18, 23], dtype="uint8") # red values detected by https://imagecolorpicker.com/en
#upper = np.array([142, 20, 29], dtype="uint8") # red

mask = cv2.inRange(image, lower, upper)

# Find contours
cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# Extract contours depending on OpenCV version
cnts = cnts[0] if len(cnts) == 2 else cnts[1]

# Iterate through contours and filter by the number of vertices 
for c in cnts:
    perimeter = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.04 * perimeter, True)
    if len(approx) > 5:
        # cv2.putText(img, "(" + str(a) + ","+ str(b) + ") r=" + str(r), (a+r+2,b+10), cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,255,0),2 )
        cv2.drawContours(original, [c], -1, (36, 255, 12), -1)

cv2.imshow('mask', mask)
cv2.imshow('image', image)
cv2.imshow('original', original)
cv2.waitKey()