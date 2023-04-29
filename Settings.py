import arduino_communication
import cv2
import datetime
import math
from time import sleep
import numpy as np

port = "COM3" # Judhi's PC
#port = "COM8" # desktop PC
baudrate = 9600
# Create an instance of the ArduinoCommunication class
print("Opening connection with Arduino")
arduino = arduino_communication.ArduinoCommunication(port, baudrate)
sleep(1)

def gripper(n):
    arduino.communicate("g"+str(n))
    print("Gripper ",n)
    return(n)

def calculateXY(xc, yc):
    # take values from calibration result
    gradX = 4.21 
    gradY = 4.185
    angle_deg = 0 # 0 for no rotation, camera y-axis perfectly aligned with robot y-axis
    top_leftX = 333
    top_leftY = 108

    xc = xc - top_leftX # top left X pixel
    yc = yc - top_leftY # top left Y pixel
    angle_rad = math.radians(angle_deg)
    cos_val = math.cos(angle_rad)
    
    sin_val = math.sin(angle_rad)
    new_x = xc * cos_val - yc * sin_val
    new_y = xc * sin_val + yc * cos_val
    calc_wx = round(-550 + new_y/gradY,2) # Y robot is x pixel
    calc_wy = round(50 + new_x/gradX,2) # X robot is y pixel
    
    return calc_wx, calc_wy
