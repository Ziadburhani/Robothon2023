import cv2
import numpy as np

images_folder = 'Latest Photos/'
image = 'WIN_20230419_15_26_55_Pro.jpg'

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

def hsv_object_detector(image, low_hsv, high_hsv, kSize = 3, opening = True, canny = True):
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
    contours, hierarchy = cv2.findContours(canny_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    c = max(contours, key=cv2.contourArea)
    return c
     

def detect_red_box(image, showImage = False):
    low_hsv = (0, 82, 142)
    high_hsv = (180, 255, 255)
    c = hsv_object_detector(image, low_hsv, high_hsv, 3, True, True)
    rect = cv2.minAreaRect(c)
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    warped = four_point_transform(image, box)
    print(warped.shape)
    if showImage is True:
        show_image('RedBox', warped)
    return warped

# Step 2: Detect the screen within the red-box
### Relative dimensions of the screen w.r.t. the red box are fixed
def detect_screen(image, showImage = False):
    low_hsv = (53, 0, 102)
    high_hsv = (154, 255, 255)
    c = hsv_object_detector(image, low_hsv, high_hsv, 3, True, True)
    rect = cv2.minAreaRect(c)
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    warped = four_point_transform(image, box)
    print(warped.shape)
    if showImage is True:
        show_image('Screen', warped)
    return warped

# Step 3: Detect the arrows and calculate the relative movement: ArrowPosition (0.0 - 1.0)
### Within the screen, use the HSV colour space to detect the arrows
### The length of the slider is the same as the screen length (Convenient)
def detect_relative_arrow_position(image, showImage = False):
    

# Step 4: Go to the slider and move accordingly
### Dimensions of the slider are known
### Starting position of the slider is known
### Move the slider according to ArrowPosition * TotalSliderLength
### E.g.: If TotalSliderLength = 4.5cm and ArrowPosition = 0.5 -> Move slider 2.25cm
### Remember new slider position

    
image = load_image(images_folder+image)
red_box = detect_red_box(image,showImage=True)
screen = detect_screen(red_box, showImage=True)