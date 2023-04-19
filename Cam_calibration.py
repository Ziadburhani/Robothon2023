# EPSON VT6 webcam calibration script
# by Judhi Prasetyo April 2023
# EPSON_code_main.prg must be running on VT6 before running this code
# this code will move VT6 arm from (Xmin, Ymin) to (Xmax, Ymax) with the gap interval

import cv2
from time import sleep
import numpy as np
# from TalkToServo import talkToServo # connect to servo gripper and send command via USB serial
from SendToEpson import sendToEpson # connect to EPSON Robot and send command via TCP/IP

Xmax = -350
Xmin = -550
Ymax = 350
Ymin = -50
Zmin = 500 # change this value, find it out by jogging the arm so the gripper is about 5mm above the surface
gap = 200

# format of the coordinate is "x y z u" where u is the wrist rotation angle
camera_pos = "-450 150 900 -90"

sendToEpson("GO "+camera_pos)

# for Ypos in range(Ymin,Ymax+1,gap):
#     for Xpos in range(Xmin,Xmax+1,gap):
#         command = "GO " + str(Xpos) + " " + str(Ypos) + " " + str(Zmin+100) + " 0" # go to 100mm above the calibration point
#         sendToEpson(command)
#         print("Open gripper") # open gripper
#         sleep(1)
#         command = "GO " + str(Xpos) + " " + str(Ypos) + " " + str(Zmin) + " 0"  # go to the calibration point
#         sendToEpson(command)
#         print("Close gripper") # close gripper
#         sleep(0.5)
#         print("Open gripper") # open gripper
#         command = "GO " + str(Xpos) + " " + str(Ypos) + " " + str(Zmin+100) + " 0" # go to 100mm above the calibration point again
#         sendToEpson(command)

sendToEpson("GO "+camera_pos)
sleep(1)
sendToEpson("M Click_M5")

# define a video capture object
cap = cv2.VideoCapture(2)
# take a picture, show and save it to a file
ret, frame = cap.read()
cimg = 'images/calibration_image.png'
print("Capturing image")
#cv2.imshow('calibration image',frame)
cv2.imwrite(cimg, frame)
#cv2.destroyAllWindows()
cap.release()
print("Calibration image saved as " + cimg)

# center of circle detection can be added below for automatic conversion to world coordinate

