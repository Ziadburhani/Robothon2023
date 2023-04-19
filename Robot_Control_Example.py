# Python script example to control VT6 via TCP/IP
# and to control Gripper via serial port
# by Judhi Prasetyo April 2023
# EPSON_code_main.prg must be running on VT6 before running this code

# Valid EPSON commands:
# GO <x y z u>
# M <point_label>

import cv2
import serial
from time import sleep
import numpy as np
from SendToEpson import sendToEpson # connect to EPSON Robot and send command via TCP/IP
import arduino_communication

port = "COM3"
baudrate = 9600
# Create an instance of the ArduinoCommunication class
print("Opening connection with Arduino")
arduino = arduino_communication.ArduinoCommunication(port, baudrate)
sleep(3)   

# format of the coordinate is "x y z u" where u is the wrist rotation angle
pos1 = "-450 150 900 -90"
sendToEpson("GO "+ pos1)
sleep(2)

# opening gripper
print("Open gripper")
response = arduino.communicate("g0")
print(response)
sleep(1)

# closing gripper
print("Close gripper")
response = arduino.communicate("g100")
print(response)
sleep(2)

# opening gripper halfway
print("Open gripper halfway")
response = arduino.communicate("g50")
print(response)
sleep(2)

# closing gripper 70%
print("Closing gripper 70%")
response = arduino.communicate("g70")
print(response)
sleep(2)

# trying invalid gripper command
print("Sending g110")
response = arduino.communicate("g110")
print(response)
sleep(2)

#sendToEpson("M Click_M5")
sleep(2)

# closing connection to Arduino
print("Disconnecting from Arduino")
arduino.close()
