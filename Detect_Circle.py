import cv2
import numpy as np
  
# Read image.
img = cv2.imread('calibration.jpg', cv2.IMREAD_COLOR)

# define a video capture object
#vid = cv2.VideoCapture(0)

    # Capture the video frame
    # by frame
#ret, img = vid.read()
  

# Convert to grayscale.
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  
# Blur using 3 * 3 kernel.
gray_blurred = cv2.blur(gray, (6, 6))
  
# Display the resulting frame
# cv2.imshow('frame', img)
# cv2.imshow('gray',gray_blurred)
# cv2.waitKey(0)
   
# Apply Hough transform on the blurred image.
detected_circles = cv2.HoughCircles(gray_blurred, 
                  cv2.HOUGH_GRADIENT, 1, 20, param1 = 200,
              param2 = 50, minRadius = 40, maxRadius = 55)
  
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
    
    i = 1
    #for pt in detected_circles[0, :]:
    for pt in sorted_circles:
        a, b, r = pt[0], pt[1], pt[2]
  
        # Draw the circumference of the circle.
        cv2.circle(img, (a, b), r, (0, 255, 0), 2)
        print( str(i) + ": (" + str(a) + ","+ str(b) + ") r=" + str(r) )
        # Draw a small circle (of radius 1) to show the center.
        cv2.circle(img, (a, b), 1, (0, 0, 255), 3)
        cv2.putText(img, str(i) + ": (" + str(a) + ","+ str(b) + ") r=" + str(r), (a-r-10,b+r+30), cv2.FONT_HERSHEY_SIMPLEX,0.8,(0,255,0),2 )
        i=i+1
    img = cv2.resize(img, (1280,768))  
    cv2.imshow("Detected Circle", img)
    cv2.waitKey(0)
        
else:
    print("no circles detected!")
