<<<<<<< HEAD
# from util_manual_corner_select import corner_selector
from util_houghlines_blackboard import *


houghlines_blackboard()
=======
from util_houghlines_blackboard import *

file_name = "FFC01EC6-E6F4-4FFF-BBD8-DFC4D0E0A6E1-16.9"
img_to_houghlines = cv.imread("developing_images\\" + f'{file_name}' + ".jpg", 1)
result_img = houghlines_blackboard(img_to_houghlines)
cv2.imshow("result_img", result_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
>>>>>>> 39d8538237697d7fbfc2d5be3dd871bdffd5ebf7
