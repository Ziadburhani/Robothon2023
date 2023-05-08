import cv2
from time import *
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
    return vid
    # if(vid.isOpened()):
    #         print("=======Ready to capture=======")  
    #         ret, img = vid.read() # take a sample frame
    #        return vid

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
    sleep(1)
    # take picture here to get slider value
    print("Capturing slider's target1")
    while(cam.isOpened()):
        t_end = time() + 4
        while time() < t_end:
            ret, img = cam.read()
            cv2.waitKey(20)    
        ret, img = cam.read()
        cv2.imshow('i', img)
        cv2.waitKey(500)
        cv2.destroyAllWindows()
        k = ord('q')
        if k == ord('q'):
            first_image = img
            first_arrow_distance = get_target(first_image, None, DEBUG_MODE=True)
            if first_arrow_distance != -1:
                print("First arrow distance = {:.2f} mm".format(first_arrow_distance))
                break
            else:
                print("Error occured with the first target.")
                break
        if k == ord('c'):
            break
    else:
        print("Camera error")
        exit(1)
    #target1 = get_target(img1, None)
    #target1 = 15.5
    target1 = round(first_arrow_distance,1)
    print("First arrow distance = {:.1f} mm".format(target1))
    if (29 > target1 > 2 ):
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
        cv2.destroyAllWindows()
        cv2.waitKey(1)
        #print("Manual slider movement NOW!")
        sleep(1)
        print("Capturing slider's target2")
        while(cam.isOpened()):
            t_end = time() + 3
            while time() < t_end:
                ret, img = cam.read()
                cv2.waitKey(20)
            ret, img2 = cam.read()
            cv2.imshow('i', img)
            cv2.waitKey(200)
            cv2.destroyAllWindows()
            k = ord('q')
            if k == ord('q'):
                second_image = img
                second_arrow_distance = get_target(second_image, first_image, DEBUG_MODE=True)
                if second_arrow_distance != -1:
                    print("Second arrow distance = {:.2f} mm".format(second_arrow_distance))
                    break
                else:
                    print("Second target not detected. Moving on.")
                    break
            if k == ord('c'):
                break
        else:
            print("Camera error")
            exit(1)
        
        target2 = round(second_arrow_distance,1)
        print("Second arrow distance = {:.1f} mm".format(target2))  
        if (29 > target2 > 2):  
            # then grab the slider and move it accordingly
            sleep(1)
            gripper(50)
            sendToEpson("go_approach_slider " + str(target1)) # start location
            sleep(1)
            gripper(70)
            sleep(1)
            # #sendToEpson("go_slide 16")
            sendToEpson("go_slide " + str(target2))
            sleep(1)
            gripper(50)
            sleep(1)
            sendToEpson("go_tool_up")
        else:
            print("target2 is not detected!")

# --- open the door            
def door():
    gripper(80)
    sendToEpson("go_open_door")
    
# --- move the probe's plug
def plug():
    gripper(50)
    sendToEpson("go_approach_plug1")
    sleep(1)
    gripper(80)
    sleep(0.5)
    sendToEpson("go_approach_plug2")
    sleep(1)
    gripper(50)
    sleep(0.5)
    sendToEpson("go_approach_plug3")

# --- take probe, probe in, drop probe
def probe():
    #probing sequence here
    gripper(50)
    sleep(0.5)
    sendToEpson("go_probe1")
    sleep(1)
    gripper(100)
    sleep(1)
    sendToEpson("go_probe2")
    sleep(0.5)
    gripper(50)
    sleep(0.5)
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
    sleep(0.5)
    gripper(50)
    sendToEpson("go_stow_finished")
    gripper(100)
    
# --- press red button
def rb():
    gripper(80)
    sendToEpson("M Stow_Finished")
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