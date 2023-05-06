import cv2
from time import sleep
import numpy as np
from slider_task import get_target

def ConnectCamera():
    print("Connecting to camera...")
    #cam_device = 3 # on Judhi's laptop
    cam_device = 0 # on lab's desktop
    vid = cv2.VideoCapture(cam_device,cv2.CAP_DSHOW) # activate Windows Direct Show for faster camera setup
    #vid = cv2.VideoCapture(cam_device) # for other systems
    print("Camera connected")
    print("Setting video resolution")
    vid.set(cv2.CAP_PROP_FRAME_WIDTH, 1920) # max 3840 for 4K, 1920 for FHD
    vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080) # max 2160 for 4K, 1080 for FHD
    sleep(1)
    return vid

vid = ConnectCamera()
while(vid.isOpened()):
    ret, img = vid.read()
    cv2.imshow('i', img)
    k = cv2.waitKey(20)
    if k == ord('q'):
        first_image = img
        first_arrow_distance = get_target(first_image, None, DEBUG_MODE=True)
        if first_arrow_distance != -1:
            print("First arrow distance = {:.2f} mm".format(first_arrow_distance))
        else:
            print("Error occured with the first target. Press any key to try again, or 'c' to continue.")
            k = cv2.waitKey(0)
            if k == ord('c'):
                break
    if k == ord('c'):
        break


cv2.destroyAllWindows()
cv2.waitKey(1)

while(vid.isOpened()):
    ret, img = vid.read()
    cv2.imshow('i', img)
    k = cv2.waitKey(20)
    if k == ord('q'):
        second_image = img
        second_arrow_distance = get_target(second_image, first_image, DEBUG_MODE=True)
        if second_arrow_distance != -1:
            print("Second arrow distance = {:.2f} mm".format(second_arrow_distance))
        else:
            print("Error occured with the second target. Press any key to try again, or 'c' to continue.")
            k = cv2.waitKey(0)
            if k == ord('c'):
                break
    if k == ord('c'):
        break
