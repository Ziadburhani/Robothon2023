import cv2
from slider_task import *

DEBUG_MODE = False
LIVE_MODE = False

if LIVE_MODE is False:
    images_folder = 'Sunday_images/'
    first_image = 'WIN_20230430_00_39_36_Pro.jpg'
    second_image = 'WIN_20230430_00_39_52_Pro.jpg'
    first_image = cv2.imread(images_folder + first_image)
    first_arrow_distance = get_target(first_image, None, DEBUG_MODE)
    if first_arrow_distance != -1:
        print("First arrow distance = {:.2f} mm".format(first_arrow_distance))
    else:
        print("Error occured with the first target.")
else:
    vid = cv2.VideoCapture(0)
    while(vid.isOpened()):
        ret, img = vid.read()
        cv2.imshow('i', img)
        k = cv2.waitKey(20)
        if k == ord('q'):
            first_image = img
            first_arrow_distance = get_target(first_image, None, DEBUG_MODE)
            if first_arrow_distance != -1:
                print("First arrow distance = {:.2f} mm".format(first_arrow_distance))
            else:
                print("Error occured with the first target. Press any key to try again, or 'c' to continue.")
                k = cv2.waitKey(0)
                if k == ord('c'):
                    break

if LIVE_MODE is False:
    second_image = cv2.imread(images_folder + second_image)
    second_arrow_distance = get_target(second_image, first_image, DEBUG_MODE)
    if second_arrow_distance != -1:
        print("Second arrow distance = {:.2f} mm".format(second_arrow_distance))
    else:
        print("Error occured with the second target.")
else:
    while(vid.isOpened()):
        ret, img = vid.read()
        cv2.imshow('i', img)
        k = cv2.waitKey(20)
        if k == ord('q'):
            second_image = img
            second_arrow_distance = get_target(second_image, first_image, DEBUG_MODE)
            if second_arrow_distance != -1:
                print("Second arrow distance = {:.2f} mm".format(second_arrow_distance))
            else:
                print("Error occured with the second target. Press any key to try again, or 'c' to continue.")
                k = cv2.waitKey(0)
                if k == ord('c'):
                    break
