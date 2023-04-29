import cv2
import datetime
import math
from time import sleep
import numpy as np

# gradX = 2.84 # take from cal_image_corrected
# gradY = 2.44 # take from cal_image_corrected
angle_deg = 0 # take from cal_image_corrected, add minus sign
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

def calculateXY(xc, yc):
    xc = xc - tl_x # top left X pixel
    yc = yc - tl_y # top left Y pixel
    calc_wx = -550 + round( yc / gradY, 2) # Y robot is x pixel
    calc_wy = 50 + round( xc / gradX, 2) # X robot is y pixel 
    return calc_wx, calc_wy

px1, py1 = (1465, 302) # blue button pixel
px2, py2 = (741, 271) # blue button pixel

wX1, wY1 = calculateXY(px1,py1)
wX2, wY2 = calculateXY(px2,py2)

print(wX1, wY1)

actual_X1, actual_Y1 = (-554.315, 291.638)
actual_X2, actual_Y2 = (-559.394, 44.089)

print("Gap blue button", (actual_X1 - wX1, actual_Y1 - wY1) )

