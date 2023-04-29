# An example Python code to send command to EPSON VT6
# by Judhi Prasetyo April 2023
# EPSON_code_main.prg must be running on VT6 before running this code

#import socket
from time import sleep
import numpy as np
# from TalkToServo import talkToServo # connect to servo gripper and send command via USB serial
from SendToEpson import sendToEpson # connect to EPSON Robot and send command via TCP/IP

## Create a client socket
# clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
# ## Connect to the EPSON robot
# # clientSocket.connect(("192.168.150.2",2001)); # change this according to your robot address
# clientSocket.connect(("127.0.0.1",2001)); # this is the EPSON RC7+ simulator on localhost

# format of the coordinate is "x y z u" where u is the wrist rotation angle
places = ["100 400 600 0", "0 500 500 0", "-100 600 400 0"]

# for data in places:
#     # Send data to robot
#     sendToEpson("JUMP3 " + data)
#     # then do something else, like open gripper:
#     # talkToServo("g0")  # servo fully opened
#     # talkToServo("g100") # servo fully closed
#     # then move Z down
#     # close the gripper according to the object size
#     # then jump to the container position
#     # and release the item
#     #etc
    
#     sleep(1)


sendToEpson("e " + "open_door")