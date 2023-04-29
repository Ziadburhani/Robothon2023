import cv2
from slider_task import *

DEBUG_MODE = False

images_folder = 'Saturday_images/'
first_image = 'REDBOX_20230429_162941.png'
second_image = 'REDBOX_20230429_162958.png'

first_arrow = cv2.imread(images_folder + first_image)
first_arrow_distance = get_target(first_arrow, None, DEBUG_MODE)
print("First arrow distance = {:.2f} mm".format(first_arrow_distance))

second_arrow = cv2.imread(images_folder + second_image)
second_arrow_distance = get_target(second_arrow, first_arrow, DEBUG_MODE)
print("Second arrow distance = {:.2f} mm".format(second_arrow_distance))
