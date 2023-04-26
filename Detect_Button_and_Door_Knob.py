import cv2
import datetime
import math
from time import sleep
import numpy as np
import arduino_communication
#from SendToEpson import sendToEpson # connect to EPSON Robot and send command via TCP/IP

#sendToEpson("M Camera_Pos")
sleep(1.5)

def calculateXY(xc, yc):
    yc = yc - 192
    xc = xc - 481
    angle_rad = math.radians(-3.622)
    cos_val = math.cos(angle_rad)
    sin_val = math.sin(angle_rad)
    new_x = xc * cos_val - yc * sin_val
    new_y = xc * sin_val + yc * cos_val
    #new_x = round(new_x + 481,2)
    #new_y = round(new_y + 192,2)
    gradX = 3.335
    gradY = 3.33
    calc_wx = round(-550 + new_y/gradY,2) # Y robot is x pixel
    calc_wy = round(50 + new_x/gradX,2) # X robot is y pixel
    return calc_wx, calc_wy
               
#define a video capture object
print("Starting camera")
#cam_device = 3 # on Judhi's laptop
cam_device = 0 # on lab's desktop
#vid = cv2.VideoCapture(cam_device,cv2.CAP_DSHOW) # activate Windows Direct Show for faster camera setup
vid = cv2.VideoCapture(0) # for other systems

print("Setting video resolution")
vid.set(cv2.CAP_PROP_FRAME_WIDTH, 1920) # max 3840 for 4K, 1920 for FHD
vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080) # max 2160 for 4K, 1080 for FHD

# Capture the video frame
ret, img = vid.read()

n_frame = 1 # frame counter

while(vid.isOpened()):
    print("=======Ready to capture=======")   
    # Capture the video frame by frame
    print("Capturing frame")
    ret, img = vid.read()
    # now = datetime.datetime.now()
    # filename = now.strftime("BOARD_%Y%m%d_%H%M%S.png")
    # cv2.imwrite(filename, img)
    # img = cv2.imread('images/board1.jpg')

    # convert to HSV for color detection
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # ----------------- daylight --------------
    #lower_blue = np.array([75, 56, 56])
    #higher_blue = np.array([115, 255, 205])
    #lower_bright = np.array([75, 72, 129])  
    #higher_b = np.array([115, 253, 245])

    # # --------------- most reliable params so far (29-05-2022) --------------
    # lower_blue = np.array([70, 108, 88])
    # higher_blue = np.array([136, 255, 255])
    # lower_bright = np.array([0, 0, 0])
    # higher_bright = np.array([180, 255, 114])
    
    # --------------- new params (25-04-2023) --------------
    lower_blue = np.array([70, 108, 88])
    higher_blue = np.array([136, 255, 255])
    lower_bright = np.array([0, 0, 100])
    higher_bright = np.array([228, 60, 200])

#    # --------------- using magnet (25-04-2023) --------------
#     lower_blue = np.array([70, 108, 88])
#     higher_blue = np.array([136, 255, 255])
#     lower_bright = np.array([22, 80, 51])
#     higher_bright = np.array([130, 143, 89])
    
    # getting the range of blue color in frame
    blue_range = cv2.inRange(hsv, lower_blue, higher_blue)
    bright_range = cv2.inRange(hsv, lower_bright, higher_bright)
    res_blue = cv2.bitwise_and(img,img, mask=blue_range)
    res_bright = cv2.bitwise_and(img,img, mask=bright_range)

    # Convert to grayscale and 
    # Blur using 3 * 3 kernel.
    print("Converting to grayscale")
    gray_blue = cv2.cvtColor(res_blue, cv2.COLOR_BGR2GRAY)
    gray_blue_blurred = cv2.blur(gray_blue, (3, 3))
    gray_bright = cv2.cvtColor(res_bright, cv2.COLOR_BGR2GRAY)
    gray_bright_blurred = cv2.blur(gray_bright, (3,3))

    # Apply Hough transform on the blurred image. One for the blue button, one for the keyhole
    print("Detecting circles")
    detected_blue_circles = cv2.HoughCircles(gray_blue_blurred, 
                    cv2.HOUGH_GRADIENT, 0.5, 1000, param1 = 45, #55
                param2 = 10, minRadius = 19, maxRadius = 55)

    detected_bright_circles = cv2.HoughCircles(gray_bright_blurred, 
                    cv2.HOUGH_GRADIENT, 0.5, 1000, param1 = 95, #55
                param2 = 10, minRadius = 25, maxRadius = 35)

    # Draw circles if detected.
    print("Drawing circles")
    if detected_blue_circles is not None and detected_bright_circles is not None:
        # Convert the circle parameters a, b and r to integers.
        detected_blue_circles = np.uint16(np.around(detected_blue_circles))
        detected_bright_circles = np.uint16(np.around(detected_bright_circles))

        for pt in detected_blue_circles[0]:
            a1, b1, r1 = pt[0], pt[1], pt[2]
            x1, y1 = calculateXY(a1, b1)
            # Draw the circle
            cv2.circle(img, (a1, b1), r1, (0, 255, 0), 2)
            # Draw the center of the circle
            cv2.circle(img, (a1, b1), 1, (0, 0, 255), 3)
            # add text label
            cv2.putText(img, "Blue (" + str(a1) + ","+ str(b1) + ") r=" + str(r1), (a1+10,b1+r1+2), cv2.FONT_HERSHEY_SIMPLEX,1,(255,100,0),2 )
            cv2.putText(img, "World [" + str(x1) + ","+ str(y1)+ "]", (a1+10,b1+r1+50), cv2.FONT_HERSHEY_SIMPLEX,1,(255,100,100),2 )

        for pt2 in detected_bright_circles[0]:
            a2, b2, r2 = pt2[0], pt2[1], pt2[2]
            pixel_distance = np.sqrt((int(a2)-int(a1))**2 + (int(b2)-int(b1))**2)
            if pixel_distance > 00 and pixel_distance < 800:
                print("Pixel distance : " + str(round(pixel_distance,0)) ) 
                x2, y2 = calculateXY(a2, b2)
                # Draw the circle
                cv2.circle(img, (a2, b2), r2, (0, 255, 0), 2)
                # Draw the center of the circle 
                cv2.circle(img, (a2, b2), 1, (0, 0, 255), 3)
                # add text label
                cv2.putText(img, "Bright (" + str(a2) + ","+ str(b2) + ") r=" + str(r2), (a2+r2+2,b2+10), cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2 )
                cv2.putText(img, "World [" + str(x2) + ","+ str(y2)+ "]", (a2+10,b2+r2+50), cv2.FONT_HERSHEY_SIMPLEX,1,(50,200,200),2 )
        
        # add label for human input to start the robot OR quit OR recapture image
        cv2.putText(img, "Press 'g' = start robot, 'q' = quit, other key = recapture", (50,100), cv2.FONT_HERSHEY_SIMPLEX,1.5,(0,255,255),2)
        
        # check the distance between the Blue button and the Keyhole
        pixel_distance = np.sqrt((int(a2)-int(a1))**2 + (int(b2)-int(b1))**2)
        print("Pixel distance : " + str(round(pixel_distance,0)) ) 
        # resize the image to show
        img_r = cv2.resize(img,(860,540))
        cv2.imshow("Detected Circle", img_r)

        # points only valid if the distance above is more than 550 pixels (FHD) 
        # if (pixel_distance > 450) :
        #     print("Blue Button:")
        #     print("Pixel is at x=" + str(a1) + "  y="+ str(b1) + " r=" + str(r1))
        #     x, y = calculateXY(a1, b1)
        #     print("World coordinate is at x mm= " + str(x) + "  y mm= "+ str(y))
        #     print("-----")
        #     print("Keyhole:")
        #     print("Pixel is at x=" + str(a2) + "  y="+ str(b2) + " r=" + str(r2))
        #     x1, y1 = calculateXY(a2, b2)
        #     print("World coordinate is at x mm= " + str(x1) + "  y mm= "+ str(y1))
        #     print("MAKE SURE ROBOT IS READY!")
        #     print("Press 'g' to start robot")
        #     print("Press 'q' to quit")
        #     print("Any other key to re-capture image")
        # waiting for human's input
        k = cv2.waitKey(0)
        # if human selected to quit
        if k == ord('q'):
            break
