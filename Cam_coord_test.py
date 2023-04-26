import cv2
import math
from time import sleep
import numpy as np
import arduino_communication
from SendToEpson import sendToEpson # connect to EPSON Robot and send command via TCP/IP

world_points = [x for x in range(12)]

#port = "COM5" # Judhi's PC
port = "COM8" # desktop PC
baudrate = 9600
# Create an instance of the ArduinoCommunication class
print("Opening connection with Arduino")
arduino = arduino_communication.ArduinoCommunication(port, baudrate)
sleep(1)


# world coordinate parameter
Xmax = -350
Xmin = -550
Ymax = 350
Ymin = 50
Zmin = 523
gap = 100

gradX = 3.72667 # take from cal_image_corrected
gradY = 3.745 # take from cal_image_corrected
angle_deg = -2.7939 # take from cal_image_corrected, add minus sign
top_leftX = 254 # take from cal_image_corrected
top_leftY = 132 # take from cal_image_corrected
    

def calculateXY(xc, yc):
    xc = xc - top_leftX # top left X pixel
    yc = yc - top_leftY # top left Y pixel
    angle_rad = math.radians(angle_deg)
    cos_val = math.cos(angle_rad)
    sin_val = math.sin(angle_rad)
    new_x = xc * cos_val - yc * sin_val
    new_y = xc * sin_val + yc * cos_val
    calc_wx = round(-550 + new_y/gradY,2) # Y robot is x pixel
    calc_wy = round(50 + new_x/gradX,2) # X robot is y pixel
    return calc_wx, calc_wy

# Read image.
# img = cv2.imread('cal_image_original.png', cv2.IMREAD_COLOR)

sendToEpson("M Camera_Pos")
sleep(1)
        
# define a video capture object
print("Connecting to camera...")
vid = cv2.VideoCapture(0)
vid.set(cv2.CAP_PROP_FRAME_WIDTH, 1920) # max 3840 for 4K, 1920 for FHD
# vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080) # max 2160 for 4K, 1080 for FHD
#     # Capture the video frame
#     # by frame
ret, img = vid.read()
  
# Convert to grayscale.
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  
# Blur using 3 * 3 kernel.
gray_blurred = cv2.blur(gray, (6, 6))
  
# Display the resulting frame
cv2.imshow('frame', img)
cv2.imwrite('coord_test.png', img)
# cv2.imshow('gray',gray_blurred)
cv2.waitKey(0)
cv2.destroyAllWindows()
   
# Apply Hough transform on the blurred image.
detected_circles = cv2.HoughCircles(gray_blurred, 
                  cv2.HOUGH_GRADIENT, 1, 20, param1 = 200,
              param2 = 50, minRadius = 20, maxRadius = 155)
  
# Draw circles that are detected.
if detected_circles is not None:
    print(detected_circles)
    print("---")
    
    circles = detected_circles
    # convert the list of circles to a set to remove duplicates
    unique_circles = set((int(circle[0]), int(circle[1]), int(circle[2])) for circle in circles[0])

    # sort the circles based on their coordinates
    sorted_circles = sorted(unique_circles,  key=lambda circle: (circle[1], circle[0]))

    # print the sorted circles
    for circle in sorted_circles:
        print(circle)
        
    #detected_circles = np.uint16(np.around(detected_circles))
    
    i = 0
    column = 0
    #for pt in detected_circles[0, :]:
    for pt in sorted_circles:
        a, b, r = pt[0], pt[1], pt[2]
        calc_wx, calc_wy = calculateXY(a,b)
        world_points[i] = [calc_wx, calc_wy]
        i = i+1
      # Draw the circumference of the circle.
        cv2.circle(img, (a, b), r, (0, 255, 0), 2)
        # Draw a small circle (of radius 1) to show the center.
        cv2.circle(img, (a, b), 1, (0, 0, 255), 3)
        cv2.putText(img, str(i) + ":[" + str(a) + ","+ str(b) + "] r=" + str(r), (a-r-20,b+r+30), cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,0),1 )
        cv2.putText(img, "(" + str(calc_wx) + ","+ str(calc_wy) + ")", (a - 100, b + 20), cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,240),1 )
        cv2.putText(img, "GradX="+ str(gradX) +",  GradY=" + str(gradY), (10,40), cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,255,255),1 )
        
    
    cv2.imshow("Corrected Circle", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows
    response = arduino.communicate("g50")
    print(response)
    sleep(0.7)
                
    for pt in world_points:
        Xpos, Ypos = pt[0], pt[1]
        command = "GO " + str(Xpos) + " " + str(Ypos) + " " + str(Zmin+100) + " 0" # go to 100mm above the detected point
        sendToEpson(command)
        sleep(0.2)
        command = "GO " + str(Xpos) + " " + str(Ypos) + " " + str(Zmin) + " 0" # go to detection point
        sendToEpson(command)
        sleep(0.2)
        response = arduino.communicate("g80") # close gripper
        print(response)
        sleep(0.5)
        command = "GO " + str(Xpos) + " " + str(Ypos) + " " + str(Zmin+100) + " 0" # lift up
        sendToEpson(command)
        sleep(0.5)
        command = "GO " + str(Xpos) + " " + str(Ypos) + " " + str(Zmin) + " 0" # put it down
        sendToEpson(command)
        sleep(0.2)
        response = arduino.communicate("g50") # half open gripper
        print(response)
        sleep(0.5)
        command = "GO " + str(Xpos) + " " + str(Ypos) + " " + str(Zmin+100) + " 0" # go to 100mm above the calibration point
        sendToEpson(command)        
        k = input("Press enter to conitune..")
        if k == " ":
            break
        
else:
    print("no circles detected!")

