import arduino_communication
import cv2
import datetime
import math
from time import sleep
import numpy as np
from SendToEpson import sendToEpson # connect to EPSON Robot and send command via TCP/IP

#port = "COM3" # Judhi's PC
port = "COM9" # desktop PC
baudrate = 9600
# Create an instance of the ArduinoCommunication class
print("Opening connection with Arduino")
arduino = arduino_communication.ArduinoCommunication(port, baudrate)
sleep(1)

def gripper(n):
    arduino.communicate("g"+str(n))
    print("Gripper ",n)
    sleep(2)    
    return(n)

def calculateXY(xc, yc):
    # take values from calibration result
    tl_x, tl_y = 284, 318 # take from cal_image_corrected
    tr_x, tr_y = 1268, 317
    bl_x, bl_y = 284, 807
    br_x, br_y = 1270, 808

    Y_len = 200
    X_len = 100

    gradX = (tr_x - tl_x) / Y_len
    gradY = (bl_y - tl_y) / X_len

    print("gradX", gradX)
    print("gradY", gradX)

    xc = xc - tl_x # top left X pixel
    yc = yc - tl_y # top left Y pixel
    calc_wx = -550.3 + round( yc / gradY, 2) # Y robot is x pixel
    calc_wy = 51.2 + round( xc / gradX, 2) # X robot is y pixel 
    return calc_wx, calc_wy

