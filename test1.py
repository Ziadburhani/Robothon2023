import cv2
from time import sleep
import numpy as np
from Settings import gripper
from SendToEpson import sendToEpson # connect to EPSON Robot and send command via TCP/IP
from map_coord import get_coord
from slider_task import *

# --- click M5 button
def m5():
    gripper(80)
    sendToEpson("go_click_m5")

# --- press blue button
def bb():
    gripper(80)
    sendToEpson("go_press_blue_button")
    
# --- move sliders
def slide():
    sendToEpson("go_check_display")
    # take picture here to get slider value
    # then grab the slider and move it accordingly
    # distance = get_target(current_image=img, None)
    sleep(1)
    gripper(50)
    sendToEpson("go_approach_slider")
    sleep(1)
    gripper(90)
    sleep(1)
    sendToEpson("go_slide 16")
    gripper(50)


# --- open the door            
def door():
    gripper(50)
    sendToEpson("go_open_door")
    
# --- move the probe's plug
def plug():
    gripper(50)
    sleep(1.5)
    sendToEpson("go_approach_plug1")
    gripper(90)
    sleep(1.5)
    sendToEpson("go_approach_plug2")
    sleep(1.5)
    gripper(50)
    sleep(0.5)
    sendToEpson("go_approach_plug3")

# --- take probe, probe in, drop probe
def probe():
    #probing sequence here
    sendToEpson("go_probe1")
    
# --- wind cable
def cable():
    sendToEpson("go_wind_cable")
    
# --- stow
def stow():
    sendToEpson("go_stow")
    
# --- press red button
def rb():
    sendToEpson("go_press_red_button")
    
# ==== main actions
#sendToEpson("m Camera_Pos")
#gripper(80)
# get world coordinates here

x1,y1,x2,y2 = get_coord()

#x1,y1,x2,y2 = 1464,302,741,271

print(x1,y1,x2,y2)
#sendToEpson("local " + str(x1) + " " + str(y1) + " " + str(x2) + " " + str(y2) )

# m5()
# bb()
# slide()
# door()
# plug()
# probe()
# cable()
# stow()
# rb()
