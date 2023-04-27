import cv2
import numpy as np
import math
from time import sleep
from SendToEpson import sendToEpson # connect to EPSON Robot and send command via TCP/IP

sendToEpson("m Display_Pic")
sleep(1)

#define a video capture object
print("Starting camera")
#cam_device = 3 # on Judhi's laptop
cam_device = 0 # on lab's desktop
#vid = cv2.VideoCapture(cam_device,cv2.CAP_DSHOW) # activate Windows Direct Show for faster camera setup
vid = cv2.VideoCapture(0) # for other systems

print("Setting video resolution")
vid.set(cv2.CAP_PROP_FRAME_WIDTH, 1920) # max 3840 for 4K, 1920 for FHD
vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080) # max 2160 for 4K, 1080 for FHD



#images_folder = 'Latest Photos/'
#image = 'WIN_20230419_15_26_58_Pro.jpg'
#image2 = 'WIN_20230419_15_27_38_Pro.jpg'


current_slider_position = 0

# Step 1: Detect the red-box
### Use HSV color space to detect the red-box
### Warp the resulting contour to have the box flat in 2-D
        
def load_image(str):
    return cv2.imread(str)

def show_image(title, file):
    cv2.imshow(title, file)
    cv2.waitKey(0)
    cv2.destroyWindow(title)
    cv2.waitKey(1)

def order_points(pts):
	# initialzie a list of coordinates that will be ordered
	# such that the first entry in the list is the top-left,
	# the second entry is the top-right, the third is the
	# bottom-right, and the fourth is the bottom-left
	rect = np.zeros((4, 2), dtype = "float32")
	# the top-left point will have the smallest sum, whereas
	# the bottom-right point will have the largest sum
	s = pts.sum(axis = 1)
	rect[0] = pts[np.argmin(s)]
	rect[2] = pts[np.argmax(s)]
	# now, compute the difference between the points, the
	# top-right point will have the smallest difference,
	# whereas the bottom-left will have the largest difference
	diff = np.diff(pts, axis = 1)
	rect[1] = pts[np.argmin(diff)]
	rect[3] = pts[np.argmax(diff)]
	# return the ordered coordinates
	return rect

def four_point_transform(image, pts):
	# obtain a consistent order of the points and unpack them
	# individually
	rect = order_points(pts)
	(tl, tr, br, bl) = rect
	# compute the width of the new image, which will be the
	# maximum distance between bottom-right and bottom-left
	# x-coordiates or the top-right and top-left x-coordinates
	widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
	widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
	maxWidth = max(int(widthA), int(widthB))
	# compute the height of the new image, which will be the
	# maximum distance between the top-right and bottom-right
	# y-coordinates or the top-left and bottom-left y-coordinates
	heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
	heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
	maxHeight = max(int(heightA), int(heightB))
	# now that we have the dimensions of the new image, construct
	# the set of destination points to obtain a "birds eye view",
	# (i.e. top-down view) of the image, again specifying points
	# in the top-left, top-right, bottom-right, and bottom-left
	# order
	dst = np.array([
		[0, 0],
		[maxWidth - 1, 0],
		[maxWidth - 1, maxHeight - 1],
		[0, maxHeight - 1]], dtype = "float32")
	# compute the perspective transform matrix and then apply it
	M = cv2.getPerspectiveTransform(rect, dst)
	warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
	# return the warped image
	return warped

def hsv_object_detector(image, low_hsv, high_hsv, kSize = 3, opening = True, canny = True, return_max_contour = True, find_contours = True):
    kernel_size = (kSize, kSize)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, kernel_size)
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    thresh = cv2.inRange(hsv_image, low_hsv, high_hsv)
    opening_img = thresh
    if opening is True:
        opening_img = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    canny_img = opening_img
    if canny is True:
        canny_img = cv2.Canny(opening_img, 100, 200)
    if find_contours is True:
        contours, hierarchy = cv2.findContours(canny_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        c = contours
        if return_max_contour is True:
            c = max(contours, key=cv2.contourArea)
        return c
    else:
        return canny_img
     

def detect_red_box(image, showImage = False):
    # Crop to the relevant bottom-right corner to focus on the red-box
    image = image[470:900, 900:1200]
    low_hsv = (0, 82, 142)
    high_hsv = (180, 255, 255)
    c = hsv_object_detector(image, low_hsv, high_hsv, 3, True, False, True)
    rect = cv2.minAreaRect(c)
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    warped = four_point_transform(image, box)
    if showImage is True:
        show_image('RedBox', warped)
    return warped

# Step 2: Detect the screen within the red-box
### Relative dimensions of the screen w.r.t. the red box are fixed
def detect_screen(image, showImage = False):
    low_hsv = (53, 0, 102)
    high_hsv = (154, 255, 255)
    c = hsv_object_detector(image, low_hsv, high_hsv, 3, True, False, True)
    rect = cv2.minAreaRect(c)
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    warped = four_point_transform(image, box)
    if showImage is True:
        show_image('Screen', warped)
    return warped


def calculate_distance(slider_arrow_y, target_arrow_y, total_length, margin = 15, slider_length = 31):
    total_length_of_slider = total_length - (margin * 2)
    start = margin
    end = margin + total_length_of_slider
    current_position_of_slider = slider_arrow_y/end
    target_position = target_arrow_y/end
    percent_to_move = (target_position - current_position_of_slider)
    distance = percent_to_move * slider_length
    distance_to_move = target_position + distance
    return current_position_of_slider, target_position, percent_to_move, distance_to_move

# Step 3: Detect the arrows and calculate the relative movement: ArrowPosition (0.0 - 1.0)
### Within the screen, use the HSV colour space to detect the arrows
### The length of the slider is the same as the screen length (Convenient)

# Step 4: Go to the slider and move accordingly
### Dimensions of the slider are known
### Starting position of the slider is known
### Move the slider according to ArrowPosition * TotalSliderLength
### E.g.: If TotalSliderLength = 4.5cm and ArrowPosition = 0.5 -> Move slider 2.25cm
### Remember new slider position
# 31MM IS THE LENGTH OF THE SLIDER

def calculate_first_arrow_position(image):
    slider_arrow_y = -1
    target_arrow_y = -1
    low_hsv = (0, 0, 221)
    high_hsv = (180, 100, 255)
    image = image[0:image.shape[0],int(image.shape[1]/2):image.shape[1]]
    contours = hsv_object_detector(image, low_hsv, high_hsv, 3, True, False, False)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    arrow1 = contours[0]
    arrow2 = contours[1]
    M1 = cv2.moments(arrow1)
    cx1 = int(M1['m10']/M1['m00'])
    cy1 = int(M1['m01']/M1['m00'])
    M2 = cv2.moments(arrow2)
    cx2 = int(M2['m10']/M2['m00'])
    cy2 = int(M2['m01']/M2['m00'])
    # Lower X value is for the left arrow
    if cx1 < cx2:
        # Arrow 1 is the left arrow
        slider_arrow_y = cy1
        target_arrow_y = cy2
    else:
        slider_arrow_y = cy2
        target_arrow_y = cy1
    
    current_position_of_slider, target_position, percent_to_move, distance_to_move = calculate_distance(slider_arrow_y, target_arrow_y, image.shape[0])
    print("Current position of slider = {:.2f}, Target position = {:.2f}, % to move slider = {:.2f}".format(current_position_of_slider, target_position, percent_to_move))
    return distance_to_move, target_arrow_y, percent_to_move

# Step 5: Detect the second arrow and calculate the relative movement: ArrowPosition (0.0 - 1.0)
### Within the screen, use the HSV colour space to detect the arrows
### The length of the slider is the same as the screen length (Convenient)
def calculate_second_arrow_position(current_slider_p, orig,image):
    slider_arrow_y = current_slider_position
    target_arrow_y = -1
    low_hsv = (0, 0, 221)
    high_hsv = (180, 100, 255)
    
    orig = orig[0:orig.shape[0],int(orig.shape[1]/2):orig.shape[1]]
    image = image[0:image.shape[0],int(image.shape[1]/2):image.shape[1]] 
    image = image[0:orig.shape[0],0:orig.shape[1]]
    backup_image = image
    orig = hsv_object_detector(orig, low_hsv, high_hsv, 3, True, False, False, False)
    image = hsv_object_detector(image, low_hsv, high_hsv, 3, True, False, False, False)
    final = cv2.subtract(image, orig) 
    contours, hierarchy = cv2.findContours(final, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    c = max(contours, key=cv2.contourArea)
    M = cv2.moments(c)
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])
    slider_arrow_y = current_slider_p
    target_arrow_y = cy
    current_position_of_slider, target_position, percent_to_move, distance_to_move = calculate_distance(slider_arrow_y, target_arrow_y, image.shape[0])
    print("Current position of slider = {:.2f}, Target position = {:.2f}, % to move slider = {:.2f}".format(current_position_of_slider, target_position, percent_to_move))
    print("Distance to move the slider (in mm): {:.2f}".format(distance_to_move))
    
#image = load_image(images_folder+image)
# Capture the video frame
ret, image = vid.read()
red_box = detect_red_box(image, True)
screen = detect_screen(red_box, True)
distance_to_move, current_slider_position, arrow_position = calculate_first_arrow_position(screen)
print("Distance to move the slider (in mm): {:.2f}".format(distance_to_move))
# image2 = load_image(images_folder+image2)
# Capture the video frame
ret, image2 = vid.read()
red_box2 = detect_red_box(image2, True)
screen2 = detect_screen(red_box2, True)
calculate_second_arrow_position(current_slider_position, screen, screen2)