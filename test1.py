import cv2
from time import sleep
import numpy as np
from Settings import gripper
from SendToEpson import sendToEpson # connect to EPSON Robot and send command via TCP/IP
from map_coord import get_coord
from slider_task import *

# ----------
# remember to open the camera throughout the session for faster response!
# ---------

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
    if(vid.isOpened()):
            print("=======Ready to capture=======")  
            ret, img = vid.read() # take a sample frame
            return vid

# --- click M5 button
def m5():
    gripper(80)
    sendToEpson("go_click_m5")

# --- press blue button
def bb():
    gripper(80)
    sendToEpson("go_press_blue_button")
    sleep(1)
    
# --- move sliders
def slide(cam):
    sendToEpson("go_check_display")
    # take picture here to get slider value
    if (cam.isOpened()):
        print("Capturing slider's target1")
        for capture in range(0,5):
            ret, img1 = cam.read()
            sleep(0.25)
    else:
        print("Camera error")
        exit(1)
    target1 = get_target(img1, None)
    target1 = 15.5
    target1 = round(target1,0)
    print("First arrow distance = {:.2f} mm".format(target1))
    if (target1 > 2):
        # then grab the slider and move it accordingly
        print("Sliding to target1")
        sleep(1)
        gripper(50)
        sendToEpson("go_approach_slider 0") # start location 0
        sleep(1) # important
        gripper(70)
        sleep(0.5)
        # #sendToEpson("go_slide 16")
        sendToEpson("go_slide " + str(target1))
        sleep(1)
        gripper(50)
        sleep(1)
        sendToEpson("go_tool_up")
        sendToEpson("go_check_display")
        # take picture here to get slider value
        if (cam.isOpened()):
            print("Capturing slider's target2")
            for capture in range(0,5):
                ret, img2 = cam.read()
                sleep(0.5)
        else:
            print("Camera error")
            exit(1)
        target2 = get_target(img2, img1)
        target2 = round(target2,2)
        print("Second arrow distance = {:.2f} mm".format(target2))  
        if (target2>0):  
            # then grab the slider and move it accordingly
            sleep(1)
            gripper(50)
            sendToEpson("go_approach_slider " + str(target1)) # start location
            sleep(1)
            gripper(70)
            sleep(2)
            # #sendToEpson("go_slide 16")
            sendToEpson("go_slide " + str(target2))
            sleep(2)
            # # gripper will go back to Slider_start position
            gripper(50)
            sleep(1)
            sendToEpson("go_tool_up")
        else:
            print("target2 is not detected!")
    else:
        print("Target1 is not detected")

# --- open the door            
def door():
    gripper(80)
    sendToEpson("go_open_door")
    
# --- move the probe's plug
def plug():
    gripper(50)
    sendToEpson("go_approach_plug1")
    sleep(1.5)
    gripper(80)
    sleep(0.8)
    sendToEpson("go_approach_plug2")
    sleep(1.5)
    gripper(50)
    sleep(0.5)
    sendToEpson("go_approach_plug3")

# --- take probe, probe in, drop probe
def probe():
    #probing sequence here
    gripper(50)
    sleep(1)
    sendToEpson("go_probe1")
    sleep(1)
    gripper(100)
    sendToEpson("go_probe2")
    sleep(1)
    gripper(50)
    sleep(1)
    sendToEpson("go_probedrop")
    
# --- wind cable
def cable():
    sendToEpson("go_approach_cable")
    gripper(100)
    sleep(1)
    sendToEpson("go_wind_cable")
    sleep(1)
    gripper(0)
    sendToEpson("go_catch_probe")
    gripper(100)

# --- stow
def stow():
    gripper(100)
    sendToEpson("go_stow")
    sleep(1)
    gripper(50)
    sendToEpson("go_stow_finished")
    gripper(100)
    
# --- press red button
def rb():
    sendToEpson("go_press_red_button")
    
# ==== main actions

cam = ConnectCamera()
sendToEpson("m Camera_Pos")
gripper(80)
# get world coordinates here
x1,y1,x2,y2 = get_coord(cam) #test coord was: x1,y1,x2,y2 = 1464,302,741,271
print(x1,y1,x2,y2)
sendToEpson("local " + str(x1) + " " + str(y1) + " " + str(x2) + " " + str(y2) )

m5()
bb()
slide(cam)
plug()
door()
probe()
cable()
stow()
rb()
sendToEpson("M Camera_Pos ")