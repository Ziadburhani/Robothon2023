import cv2
from slider_task import *

DEBUG_MODE = True
LIVE_MODE = False

if LIVE_MODE is False:
    images_folder = 'Saturday_images/'
    first_image = 'WIN_20230430_00_39_36_Pro.jpg'
    second_image = 'WIN_20230430_00_39_52_Pro.jpg'
    first_image = cv2.imread(images_folder + first_image)
else:
    vid = cv2.VideoCapture(0)
    while(vid.isOpened()):
        ret, img = vid.read()
        cv2.imshow('i', img)
        k = cv2.waitKey(20)
        if k == ord('q'):
            first_image = img
            break

first_arrow_distance = get_target(first_image, None, DEBUG_MODE)
print("First arrow distance = {:.2f} mm".format(first_arrow_distance))

if LIVE_MODE is False:
    second_image = cv2.imread(images_folder + second_image)   
else:
    while(vid.isOpened()):
        ret, img = vid.read()
        cv2.imshow('i', img)
        k = cv2.waitKey(20)
        if k == ord('q'):
            second_image = img
            break

second_arrow_distance = get_target(second_image, first_image, DEBUG_MODE)
print("Second arrow distance = {:.2f} mm".format(second_arrow_distance))
