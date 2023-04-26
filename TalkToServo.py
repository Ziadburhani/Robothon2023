# TalkToServo Library for Python

import serial
import time
SERVO_PORT = "COM8" # where the Arduino is connected to

arduino = serial.Serial(port=SERVO_PORT, timeout=0, baudrate=9600)

def talkToServo(command):
    time.sleep(1)
    print(f"Talking to arduino: {command}")    
    arduino.write(str.encode(command + "\n\r" ))
    time.sleep(0.5)
    data = arduino.readline()
    print("Received: ", data)
    return data
    # if arduino.in_waiting > 0:  # check if there's data in the serial buffer
    #     data = arduino.readline().decode().strip()  # read the data from the serial port and decode it as a string
    #     print("Received:", data)  # print the received data
    #     return data
    
    
