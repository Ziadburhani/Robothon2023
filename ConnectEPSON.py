# An example Python code to send command to EPSON VT6
# by Judhi Prasetyo April 2023
# EPSON_code_main.prg must be running on VT6 before running this code

import socket
from time import sleep
import numpy as np
from TalkToServo import talkToServo # connect to servo gripper via USB serial

## Create a client socket
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
## Connect to the EPSON robot
# clientSocket.connect(("192.168.150.2",2001)); # change this according to your robot address
clientSocket.connect(("127.0.0.1",2001)); # this is the EPSON RC7+ simulator on localhost

# format of the coordinate is "x y z u" where u is the wrist rotation angle
places = ["100 400 600 0", "0 500 500 0", "-100 600 400 0"]

for data in places:
    # Send data to robot
    msg_tx = "JUMP3 " + data + "\r\n"
    print("Sending: " + msg_tx)
    clientSocket.send(msg_tx.encode())
    msg_rx = clientSocket.recv(1023) # waiting for confirmation from robot
    print("result:", msg_rx)
    # do something else, like open gripper
    # talkToServo("g0")  # servo fully opened
    # talkToServo("g100") $ servo fully closed
    # then move Z down
    # close the gripper according to the object size
    # then jump to the container position
    # and release the item
    #etc
    
    sleep(1)

clientSocket.close # close the connection
