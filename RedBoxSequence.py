import cv2
import numpy as np

images_folder = 'images/'
image = 'img9.jpg'

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

def detect_red_box(image, showImage = False):
    kernel_size = (3, 3)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, kernel_size)
    image = cv2.blur(image, kernel_size)
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    LowH = 0
    HighH = 180
    LowS = 82
    HighS = 255
    LowV = 142
    HighV = 255
    thresh = cv2.inRange(hsv_image, (LowH, LowS, LowV), (HighH, HighS, HighV))
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    canny = cv2.Canny(opening, 100, 200)
    contours, hierarchy = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    c = max(contours, key=cv2.contourArea)
    rect = cv2.minAreaRect(c)
    box = cv2.boxPoints(rect)
    print(box)
    box = np.int0(box)
    cv2.drawContours(image, [box], 0, (0, 255, 0), 3)

    if showImage is True:
        show_image('RedBox', image)
    
image = load_image(images_folder+image)
detect_red_box(image,showImage=True)


# Step 2: Detect the screen within the red-box
### Relative dimensions of the screen w.r.t. the red box are fixed

# Step 3: Detect the arrows and calculate the relative movement: ArrowPosition (0.0 - 1.0)
### Within the screen, use the HSV colour space to detect the arrows
### The length of the slider is the same as the screen length (Convenient)

# Step 4: Go to the slider and move accordingly
### Dimensions of the slider are known
### Starting position of the slider is known
### Move the slider according to ArrowPosition * TotalSliderLength
### E.g.: If TotalSliderLength = 4.5cm and ArrowPosition = 0.5 -> Move slider 2.25cm
### Remember new slider position

