import cv2
import datetime
import math
from time import sleep
import numpy as np

# gradX = 2.84 # take from cal_image_corrected
# gradY = 2.44 # take from cal_image_corrected
angle_deg = 0 # take from cal_image_corrected, add minus sign
tl_X, tl_Y = 284, 318 # take from cal_image_corrected
tr_X, tr_Y = 1268, 318
bl_X, bl_Y = 284, 807
br_X, br_Y = 1268, 807

Y_len = 200
X_len = 100

gradX = X_len / (tr_X - tl_X)
gradY = Y_len / (bl_Y - tl_Y)

print("gradX", gradX)
print("gradY", gradX)

def calculateXY(xc, yc):
    xc = xc - tl_X # top left X pixel
    yc = yc - tl_Y # top left Y pixel
    calc_wx = -550 + round( yc * gradY, 2) # Y robot is x pixel
    calc_wy = 50 + round( xc * gradX, 2) # X robot is y pixel 
    return calc_wx, calc_wy

px1, py1 = (1465, 302) # blue button pixel
px2, py2 = (74, 271)
px3, py3 = (1268,319)

wx1, wy1 = calculateXY(px1,py1)
wx2, wy2 = calculateXY(px2,py2)
wx3, wy3 = calculateXY(px3,py3)

print(wx1, wy1)
print(wx2, wy2)
print(wx3, wy3)

actual_x1, actual_y1 = (-528.546, 276.747)
actual_x2, actual_y2 = (-559.394, 144.089)
actual_x3, actual_y3 = (-550, 250)

print("Gap blue button", (actual_x1 - wx1, actual_y1 - wy1) )
print("Gap knob ", (actual_x2 - wx2, actual_y2 - wy2) )
print("Gap 3 ", (actual_x3 - wx3, actual_y3 - wy3) )
