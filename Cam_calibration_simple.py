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
import datetime
from SendToEpson import sendToEpson # connect to EPSON Robot and send command via TCP/IP
from time import sleep
import numpy as np
from Settings import gripper

Xmax = -450
Xmin = -550
Ymax = 275
Ymin = 75
Zmin = 523 # change this value, find it out by jogging the arm so the gripper is about 5mm above the surface
gapY = 200
gapX = 100

sendToEpson("m Camera_Pos")
sleep(1)

print("Open gripper") # open gripper halfway
gripper(50)
sleep(1)
        
for Xpos in range(Xmax,Xmin-1,-gapX):
    for Ypos in range(Ymax,Ymin-1,-gapY):
        command = "GO " + str(Xpos) + " " + str(Ypos) + " " + str(Zmin+100) + " 0" # go to 100mm above the calibration point
        sendToEpson(command)
        command = "GO " + str(Xpos) + " " + str(Ypos) + " " + str(Zmin) + " 0"  # go to the calibration point
        sendToEpson(command)
        while True:
            print("Current position is ", Xpos,  ",", Ypos)
            key = input("Place a token under the gripper, press ENTER to align token or other key to move to the next point")        
            if key == "":
                print("Close gripper") # close gripper to align token
                gripper(100)
                print("Open gripper") # open gripper halfway again
                gripper(50)
                sleep(0.5)    
            else:
                break
        command = "GO " + str(Xpos) + " " + str(Ypos) + " " + str(Zmin+100) + " 0" # go to 100mm above the calibration point again
        sendToEpson(command)

sendToEpson("M Camera_Pos")
sleep(1)

