import cv2
from time import sleep
import numpy as np
from Settings import gripper
from SendToEpson import sendToEpson # connect to EPSON Robot and send command via TCP/IP

# --- click M5 button
def m5():
    sendToEpson("go_click_m5")

# --- press blue button
def bb():
    sendToEpson("go_press_blue_button")
    
# --- move sliders
def slider():
    sendToEpson("go_check_display")
    # take picture here to get slider value
    # then grab the slider and move it accordingly
    sendToEpson("go_approach_slider")
    gripper(90)
    sendToEpson("go_slide(16)")
    gripper(50)
    sendToEpson("go_check_display")
    # take picture again to get slider value
    # then grab the slider and move it accordingly
    sendToEpson("go_approach_slider")
    gripper(90)
    sendToEpson("go_slide(5)")
    gripper(50)

# --- open the door            
def door():
    gripper(50)
    sendToEpson("go_open_door")
    
# --- move the probe's plug
    gripper(50)
    sendToEpson("go_approach_plug1")
    gripper(90)
    sendToEpson("go_approach_plug2")
    gripper(50)
    sendToEpson("go_approach_plug3")

# ==== main actions
sendToEpson("m Camera_Pos")
gripper(80)
# get world coordinates here
sendToEpson("local -528.546 276.747 -558.129 134.783")

bb()
