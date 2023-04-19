# EPSON VT6 webcam calibration script
# by Judhi Prasetyo April 2023
# EPSON_code_main.prg must be running on VT6 before running this code
# this code will move VT6 arm from (Xmin, Ymin) to (Xmax, Ymax) with the gap interval
# How to calibrate:
# 1. Run this code and notice the positions on the surface every time the gripper closes
# 2. Place a calibration token roughly on each of the positions above
# 3. Run the program again and let the gripper align the tokens 
# 4. Take a picture of the surface with tokens
# 5. Run circle detection program to determine the pixel coordinates of the tokens

import cv2
from time import sleep
import numpy as np
import arduino_communication
from SendToEpson import sendToEpson # connect to EPSON Robot and send command via TCP/IP

port = "COM3"
baudrate = 9600
# Create an instance of the ArduinoCommunication class
print("Opening connection with Arduino")
arduino = arduino_communication.ArduinoCommunication(port, baudrate)
sleep(1)

Xmax = -350
Xmin = -550
Ymax = 350
Ymin = 0
Zmin = 500 # change this value, find it out by jogging the arm so the gripper is about 5mm above the surface
gap = 200

# define a video capture object
print("Connecting to camera...")
camera_device = 2
cap = cv2.VideoCapture(camera_device)
print("Camera connected")

# format of the coordinate is "x y z u" where u is the wrist rotation angle
camera_pos = "-450 150 900 -90"
# sendToEpson("GO "+camera_pos)

print("Open gripper") # open gripper
response = arduino.communicate("g0")
print(response)
sleep(1)
        
for Ypos in range(Ymin,Ymax+1,gap):
    for Xpos in range(Xmin,Xmax+1,gap):
        command = "GO " + str(Xpos) + " " + str(Ypos) + " " + str(Zmin+100) + " 0" # go to 100mm above the calibration point
        sendToEpson(command)
        
        command = "GO " + str(Xpos) + " " + str(Ypos) + " " + str(Zmin) + " 0"  # go to the calibration point
        sendToEpson(command)
        print("Close gripper") # close gripper to align token
        response = arduino.communicate("g100")
        print(response)
        sleep(1)
        print("Open gripper") # open gripper again
        response = arduino.communicate("g0")
        print(response)
        sleep(1)

        command = "GO " + str(Xpos) + " " + str(Ypos) + " " + str(Zmin+100) + " 0" # go to 100mm above the calibration point again
        sendToEpson(command)

sendToEpson("GO "+camera_pos)
sleep(1)

# take a picture, show and save it to a file
ret, frame = cap.read()
cimg = 'images/calibration_image.png'
print("Capturing image")
#cv2.imshow('calibration image',frame)
#cv2.imwrite(cimg, frame)
#cv2.destroyAllWindows()
cap.release()
print("Calibration image saved as " + cimg)

# center of circle detection can be added below for automatic conversion to world coordinate

