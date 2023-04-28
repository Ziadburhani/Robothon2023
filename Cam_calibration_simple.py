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

#port = "COM5" # Judhi's PC
port = "COM9" # desktop PC
baudrate = 9600
# Create an instance of the ArduinoCommunication class
print("Opening connection with Arduino")
arduino = arduino_communication.ArduinoCommunication(port, baudrate)


Xmax = -350
Xmin = -550
Ymax = 250
Ymin = 50
Zmin = 523 # change this value, find it out by jogging the arm so the gripper is about 5mm above the surface
gap = 200

# define a video capture object
print("Connecting to camera...")
#cam_device = 3 # on Judhi's laptop
cam_device = 0 # on lab's desktop
cap = cv2.VideoCapture(cam_device)
print("Camera connected")

sendToEpson("m Camera_Pos")
sleep(1)

print("Open gripper") # open gripper halfway
response = arduino.communicate("g50")
print(response)
sleep(1)
        
for Xpos in range(Xmax,Xmin-1,-gap):
    for Ypos in range(Ymax,Ymin-1,-gap):
        command = "GO " + str(Xpos) + " " + str(Ypos) + " " + str(Zmin+100) + " 0" # go to 100mm above the calibration point
        sendToEpson(command)
        command = "GO " + str(Xpos) + " " + str(Ypos) + " " + str(Zmin) + " 0"  # go to the calibration point
        sendToEpson(command)
        while True:
            key = input("Place a token under the gripper, press ENTER to align token or other key to move to the next point")        
            if key == "":
                print("Close gripper") # close gripper to align token
                response = arduino.communicate("g90")
                print(response)
                sleep(0.7)
                print("Open gripper") # open gripper halfway again
                response = arduino.communicate("g50")
                print(response)
                sleep(0.5)    
            else:
                break
        command = "GO " + str(Xpos) + " " + str(Ypos) + " " + str(Zmin+100) + " 0" # go to 100mm above the calibration point again
        sendToEpson(command)

sendToEpson("M Camera_Pos")
sleep(1)

# take a picture, show and save it to a file
ret, frame = cap.read()
cimg = 'calibration_image.png'
print("Capturing image")
#cv2.imshow('calibration image',frame)
cv2.imwrite(cimg, frame)
#cv2.destroyAllWindows()
cap.release()
print("Calibration image saved as " + cimg)

# center of circle detection can be added below for automatic conversion to world coordinate

