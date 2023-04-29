import cv2
from slider_task import *

images_folder = 'Latest Photos/'
first_image = 'WIN_20230419_15_26_58_Pro.jpg'
second_image = 'WIN_20230419_15_27_38_Pro.jpg'

first_arrow = cv2.imread(images_folder + first_image)
first_arrow_distance = get_target(first_arrow)
print("First arrow distance = {} mm".format(first_arrow_distance))

second_arrow = cv2.imread(images_folder + second_image)
second_arrow_distance = get_target(second_arrow, first_arrow)
print("Second arrow distance = {} mm".format(second_arrow_distance))