# TalkToServo Library for Python

import serial
import time
SERVO_PORT = "COM3" # where the Arduino is connected to

arduino = serial.Serial(port=SERVO_PORT, timeout=0, baudrate=9600)

def talkToServo(command):
    time.sleep(2)
    arduino.write(str.encode(command + "\n" ))
    print(str.encode(command+ "\n") )
    # arduino.write(str.encode("\n"))
    print(f"Communicating with arduino: {command}")
    if arduino.in_waiting > 0:  # check if there's data in the serial buffer
        data = arduino.readline().decode().strip()  # read the data from the serial port and decode it as a string
        print("Received:", data)  # print the received data
        return data
    
    
