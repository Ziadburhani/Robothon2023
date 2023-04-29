import cv2
import datetime
import math
from time import sleep
import numpy as np
              
#define a video capture object
print("Starting camera")
#cam_device = 3 # on Judhi's laptop
cam_device = 0 # on lab's desktop
#vid = cv2.VideoCapture(cam_device,cv2.CAP_DSHOW) # activate Windows Direct Show for faster camera setup
vid = cv2.VideoCapture(0) # for other systems

print("Setting video resolution")
vid.set(cv2.CAP_PROP_FRAME_WIDTH, 1920) # max 3840 for 4K, 1920 for FHD
vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080) # max 2160 for 4K, 1080 for FHD
sleep(1)

while(vid.isOpened()):
    print("=======Ready to capture=======")   
    # Capture the video frame by frame
    print("Capturing frame")
    ret, img = vid.read()
    now = datetime.datetime.now()
    filename = now.strftime("REDBOX_%Y%m%d_%H%M%S.png")
    cv2.imwrite(filename, img)
    img_r = cv2.resize(img,(860,540))
    cv2.imshow("Detected Circle", img_r)
    k = cv2.waitKey(0)
    # if human selected to quit
    if k == ord('q'):
        break