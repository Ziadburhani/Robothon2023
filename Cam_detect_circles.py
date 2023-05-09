import cv2
import numpy as np
import math
from time import sleep
from SendToEpson import sendToEpson # connect to EPSON Robot and send command via TCP/IP

# world coordinate parameter
Xmax = -450
Xmin = -550
Ymax = 275
Ymin = 75
gapX = 100
gapY = 200

gradX = 4.21 # take from cal_image_corrected
gradY = 4.185# take from cal_image_corrected
angle_deg = 0 # take from cal_image_corrected, add minus sign
top_leftX = 333 # take from cal_image_corrected
top_leftY = 108 # take from cal_image_corrected

world_points = [x for x in range(4)]
pixel_points = [x for x in range(4)]

def get_rotation_angle(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    return math.degrees(math.atan2(dy, dx))

def rotate_point(x, y, angle_deg):
    angle_rad = math.radians(angle_deg)
    cos_val = math.cos(angle_rad)
    sin_val = math.sin(angle_rad)
    new_x = x * cos_val - y * sin_val
    new_y = x * sin_val + y * cos_val
    return new_x, new_y


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

# sending robot to Camera position
sendToEpson("M Camera_Pos")
sleep(2)
cam_point = sendToEpson("P")
#print(cam_point)

# Read image.
# img = cv2.imread('original_cal.png', cv2.IMREAD_COLOR)

#define a video capture object
print("Starting camera")
#cam_device = 3 # on Judhi's laptop
cam_device = 0 # on lab's desktop
vid = cv2.VideoCapture(cam_device,cv2.CAP_DSHOW) # activate Windows Direct Show for faster camera setup
#vid = cv2.VideoCapture(cam_device) # for other systems
print("Camera connected")
print("Setting video resolution")
vid.set(cv2.CAP_PROP_FRAME_WIDTH, 1920) # max 3840 for 4K, 1920 for FHD
vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080) # max 2160 for 4K, 1080 for FHD
sleep(3)


# Capture the video frame
ret, img = vid.read()
  
# Convert to grayscale.
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  
# Blur using 3 * 3 kernel.
gray_blurred = cv2.blur(gray, (6, 6))
  
# Display the resulting frame
cv2.imshow('frame', img)
cv2.imwrite('original_cal.png', img)
# cv2.imshow('gray',gray_blurred)
cv2.waitKey(0)
   
# Apply Hough transform on the blurred image.
detected_circles = cv2.HoughCircles(gray_blurred, 
                  cv2.HOUGH_GRADIENT, 1, 20, param1 = 200,
              param2 = 50, minRadius = 20, maxRadius = 155)
  
# Draw circles that are detected.
if detected_circles is not None:
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
    wx = Xmin
    wy = Ymin
    for pt in sorted_circles:
        a, b, r = pt[0], pt[1], pt[2]
  
        i=i+1
        column = column + 1
        world_points[i-1] = [wx,wy]
        pixel_points[i-1] = [a,b]
      # Draw the circumference of the circle.
        cv2.circle(img, (a, b), r, (0, 255, 0), 2)
        # Draw a small circle (of radius 1) to show the center.
        cv2.circle(img, (a, b), 1, (0, 0, 255), 3)
        cv2.putText(img, str(i) + ":[" + str(a) + ","+ str(b) + "] r=" + str(r), (a-r-20,b+r+30), cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,255,0),2 )
        cv2.putText(img, "(" + str(wx) + ","+ str(wy) + ")", (a-r-80,b+r-50), cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,255),2 )
        print(str(i) + ": " + str(a) + "\t\t"+ str(b) + "\t\t" + str(wx) + "\t\t" + str(wy) )

        wy = wy + gapY
        if column > 3:
            column = 0
            wy = Ymin
            wx = wx + gapX

    origin_x = pixel_points[0][0]
    origin_y = pixel_points[0][1]
    
    #rot = get_rotation_angle(origin_x,origin_y,pixel_points[3][0],pixel_points[3][1])
    rot = get_rotation_angle(pixel_points[0][0],pixel_points[0][1],pixel_points[1][0],pixel_points[1][1])
    print("Rotation angle ",rot," degree")
    cv2.putText(img, "Rotation angle "+ str(rot) +" degree", (10,20), cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,255,255),2 )
    #img = cv2.resize(img, (1280,768))  
    #gradX = 3.3333
    #gradY = 3.3333
    ref_x1, ref_y1 = rotate_point(pixel_points[1][0] - origin_x, pixel_points[1][1] - origin_y, -rot)
    ref_x2, ref_y2 = rotate_point(pixel_points[2][0] - origin_x, pixel_points[2][1] - origin_y, -rot)
    gradX = abs(pixel_points[1][0] - origin_x) / abs(Xmax-Xmin)
    gradY = abs(pixel_points[2][1] - origin_y) / abs(Ymax-Ymin)
        
    for p in range(0,4):
        c_px = pixel_points[p][0] 
        c_py = pixel_points[p][1] 
        c_wx = world_points[p][0]
        c_wy = world_points[p][1]
        new_x, new_y = rotate_point(c_px - origin_x, c_py - origin_y, -rot)
        new_x = int(round(new_x + origin_x))
        new_y = int(round(new_y + origin_y))
        #gradX = abs(c_px - origin_x) / abs(Ymax-Ymin)
        #gradY = abs(c_py - origin_y) / abs(Xmax - Xmin)
        calc_wx, calc_wy =calculateXY(c_px, c_py)
        #calc_wx = round(Xmin + (new_y - origin_y)/gradX,2) # Y robot is x pixel
        #calc_wy = round(Ymin + (new_x - origin_x)/gradY,2) # X robot is y pixel
        print(str(c_wx) + "," + str(c_wy) + "," + str(c_px) + "," + str(c_py) + " " + str(new_x) + "," + str(new_y) + " " + str(calc_wx) + "," +str(calc_wy))
        cv2.circle(img, (new_x, new_y), 5, (255, 0, 0), 3)
        cv2.putText(img, "[" + str(new_x) + ","+ str(new_y) + "]", (new_x - 40, new_y - 10), cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,0,0),2 )
        cv2.putText(img, "(" + str(calc_wx) + ","+ str(calc_wy) + ")", (c_px - 100, c_py + 40), cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,255,240),2 )
        cv2.putText(img, "GradX="+ str(gradX) +",  GradY=" + str(gradY), (10,40), cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),2 )
        cv2.putText(img, "Camera position="+ str(cam_point), (10,60), cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),2 )
    cv2.imshow("Corrected Circle", img)
    cimg = 'cal_image_corrected.png'
    cv2.imwrite(cimg, img)
    print("Image saved as "+cimg)
    cv2.waitKey(0)
    
else:
    print("no circles detected!")

