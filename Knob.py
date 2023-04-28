import cv2
import numpy as np

images_folder = 'Friday_images/'
images = (
    'BOARD_20230428_205304.png',
    'BOARD_20230428_205307.png',
    'BOARD_20230428_205312.png',
    'BOARD_20230428_205314.png',
    'BOARD_20230428_205315.png',
    'BOARD_20230428_205319.png',
    'BOARD_20230428_205324.png',
    'BOARD_20230428_205329.png',
    'BOARD_20230428_205333.png',
    'BOARD_20230428_205338.png',
    'BOARD_20230428_205343.png',
    'BOARD_20230428_205348.png',
    'BOARD_20230428_205358.png',
    'BOARD_20230428_205404.png',
    'BOARD_20230428_205413.png',
    'BOARD_20230428_205419.png',
    'BOARD_20230428_205427.png',
    'BOARD_20230428_205434.png',
    'BOARD_20230428_205439.png',
    'BOARD_20230428_205443.png',
    'BOARD_20230428_205450.png',
    'BOARD_20230428_205455.png',
    'BOARD_20230428_205459.png',
    'BOARD_20230428_205507.png',
    'BOARD_20230428_205511.png',
    'BOARD_20230428_205516.png',
    'BOARD_20230428_205524.png'
)

def show_image(title,file):
    cv2.imshow(title,file)
    cv2.waitKey(0)
    cv2.destroyWindow(title)
    cv2.waitKey(1)

def increase_contrast(img, clipLimit = 2.0, tileGridSize=(120,12)):
    lab= cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l_channel, a, b = cv2.split(lab)

    # Applying CLAHE to L-channel
    clahe = cv2.createCLAHE(clipLimit, tileGridSize)
    cl = clahe.apply(l_channel)
    
    # merge the CLAHE enhanced L-channel with the a and b channel
    limg = cv2.merge((cl,a,b))
    
    # Converting image from LAB Color model to BGR color spcae
    enhanced_img = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
    
    return enhanced_img

def detect_door(image):
    x = y = w = h = 0
    
    # Step 1: Preprocessing
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur
    blurred = cv2.GaussianBlur(gray, (15, 15), 0)

    # Threshold with an optimal value
    t,thresh = cv2.threshold(blurred, 128, 255, cv2.THRESH_BINARY)

    # Step 2: Morphological operations
    kernel = np.ones((5, 5), np.uint8)
    eroded = cv2.erode(thresh, kernel, iterations=1)
    dilated = cv2.dilate(eroded, kernel, iterations=1)

    # Step 3: Contour detection
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Step 4: Bounding box and filtering based on area and aspect ratio
    # Since our door is roughly a square
    for contour in contours:
        area = cv2.contourArea(contour)
        t_x, t_y, t_w, t_h = cv2.boundingRect(contour)
        aspect_ratio = float(t_w)/t_h  
        if 140000 < area < 240000 and 0.75 < aspect_ratio < 1.5:
            cv2.drawContours(image, [contour], -1, (0, 255, 0), 3)
            x = t_x
            y = t_y
            w = t_w
            h = t_h
    #show_image('i', image)
    return x, y, w, h

def detect_knob(image, x, y, w, h):
    # Set center and radius to 0
    center = radius = 0
    
    # Create an image of the same size as the original
    # Set it to all black, and just replace the door in the
    # correct position.
    # This is done so that the coordinates match the original image
    size = image.shape[0], image.shape[1], 3
    final = np.zeros(size, np.uint8)
    final[y:y+h, x:x+w] = contr[y:y+h, x:x+w]
    #final = increase_contrast(final, 1.5)
    
    # Convert to grayscale, apply a bilateral filter
    f_gray = cv2.cvtColor(final, cv2.COLOR_BGR2GRAY)
    f_blur = cv2.bilateralFilter(f_gray, 9, 150, 150)
    
    # Find circles. Parameters here ensure that the circles are far apart
    # Of a certain size, and use the correct Canny thresholds
    rows = f_blur.shape[0]
    circles = cv2.HoughCircles(f_blur, cv2.HOUGH_GRADIENT, 1, rows, param1=100, param2=10,minRadius=20, maxRadius=60)
    
    # If we've found even one circle, that's our guy.
    # Just look at the first and return the center and radius.
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            center = (i[0], i[1])
            radius = i[2]
            break
    return center, radius


#define a video capture object
#print("Starting camera")
#cam_device = 3 # on Judhi's laptop
#cam_device = 0 # on lab's desktop
#vid = cv2.VideoCapture(cam_device,cv2.CAP_DSHOW) # activate Windows Direct Show for faster camera setup
#vid = cv2.VideoCapture(0) # for other systems

#print("Setting video resolution")
#vid.set(cv2.CAP_PROP_FRAME_WIDTH, 1920) # max 3840 for 4K, 1920 for FHD
#vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080) # max 2160 for 4K, 1080 for FHD

# Capture the video frame
#ret, img = vid.read()

for i in range(0, len(images)):
    print("Opening image: {} - {} of {}".format(images[i],i+1, len(images)))
    img = cv2.imread(images_folder + images[i])
    
    # Increase contrast
    #contr = increase_contrast(img)
    contr = img
    # Find the door first
    x, y, w, h = detect_door(contr)

    # If a door is found, detect the knob and draw it on the original
    if x != 0:
        # knob_center and knob_readius are your pixel values for the door-knob
        # Maybe the radius isn't as important, but the center should be useful
        knob_center, knob_radius  = detect_knob(img, x, y, w, h)
        
        # Draw both and show the image, just for fun.
        if knob_radius != 0:
            cv2.circle(img, knob_center, 5, (255, 0, 0), -1)
            cv2.circle(img, knob_center, knob_radius, (0, 255, 0), 3)
            show_image(str(images[i]),img)
    else:
        print("Door not found.")