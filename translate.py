import cv2
import datetime
import math
from time import sleep
import numpy as np

#from Settings import calculateXY


def calculateXY(xc, yc):
    # take values from calibration result
    tl_x, tl_y = 380, 333 # take from cal_image_corrected
    tr_x, tr_y = 1360, 330
    bl_x, bl_y = 379, 823
    br_x, br_y = 1364, 820
    
    x_ctr = int(1920/2)
    y_ctr = int(1080/2)
    
    dx = (xc - x_ctr)/100
    dy = (yc - y_ctr)/170
    
    xc = xc + dx
    yc = yc + dy
    
    print("dx,dy=",dx,dy)

    Y_len = 200
    X_len = 100

    gradX = (tr_x - tl_x) / Y_len
    gradY = (bl_y - tl_y) / X_len

    # print("gradX", gradX)
    # print("gradY", gradY)

    xc = xc - tl_x # top left X pixel
    yc = yc - tl_y # top left Y pixel
    calc_wx = -550 + round( yc / gradY, 2) # Y robot is x pixel
    calc_wy = 75 + round( xc / gradX, 2) # X robot is y pixel 
    return calc_wx, calc_wy

px1, py1 = (1465, 302) # blue button pixel
px2, py2 = (741, 271) # blue button pixel

wX1, wY1 = calculateXY(px1,py1)
wX2, wY2 = calculateXY(px2,py2)

# print("go here :x("+wX1+") :y("+wY1+") :z(550)")
# print("go here :x("+wX2+") :y("+wY2+") :z(550)")

actual_X1, actual_Y1 = (-554.315, 291.638)
actual_X2, actual_Y2 = (-559.394, 144.089)

print("Gap:", (actual_X1 - wX1, actual_Y1 - wY1) )
print("Gap:", (actual_X2 - wX2, actual_Y2 - wY2) )
