import cv2
import numpy as np

def __show_image__(title, file):
    cv2.imshow(title, file)
    cv2.waitKey(0)
    cv2.destroyWindow(title)
    cv2.waitKey(1)
def __order_points__(pts):
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

def __four_point_transform__(image, pts):
	# obtain a consistent order of the points and unpack them
	# individually
	rect = __order_points__(pts)
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
	return M, warped

image = cv2.imread('original_cal.png')
half = cv2.resize(image, (0, 0), fx = 0.1, fy = 0.1)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
t, thresh = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY_INV)
# circles = cv2.HoughCircles(thresh, cv2.HOUGH_GRADIENT, 1, 400, param1=80, param2=10,minRadius=50, maxRadius = 200)
    
# if circles is not None:
#     circles = np.uint16(np.around(circles))
#     for i in circles[0, :]:
#         center = (i[0], i[1])
#         radius = i[2]
#         cv2.circle(image, center, radius, (0, 255, 0), 3)

contours, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
#cv2.drawContours(image, contours, -1, (0, 255, 0), 3)

sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)

pts = []
for i in range(0,4):
    cv2.drawContours(image, sorted_contours, i, (255, 0, 0), 3)
    M = cv2.moments(sorted_contours[i])
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
    cv2.circle(image, (cX, cY), 3, (0, 0, 255), 3)
    pts.append([cX, cY])
__show_image__('i', image)
print(pts)
contours = np.array(pts).reshape((-1,1,2)).astype(np.int32)
rect = cv2.minAreaRect(contours)
box = cv2.boxPoints(rect)
box = np.int0(box)
matrix, warped = __four_point_transform__(image, box)
x_offset= 283
y_offset= 316
f = np.zeros(image.shape, dtype=np.uint8)
f[y_offset:y_offset+warped.shape[0], x_offset:x_offset+warped.shape[1]] = warped
print(x_offset, y_offset)
print(x_offset, y_offset + warped.shape[0])
print(x_offset+warped.shape[1], y_offset)
print(x_offset+warped.shape[1], y_offset + warped.shape[0])
__show_image__('wa', warped)
__show_image__('overlaid', f)



