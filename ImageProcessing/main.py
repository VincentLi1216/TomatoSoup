from camera_capture import *
from util_distortion_correction import *
from util_manual_corner_select import *
from util_save_img import *
from util_houghlines_blackboard import *

result_img = houghlines_blackboard("auto", cv2.imread("IMG_2918.JPG"))

cv2.imshow("auto", result_img)
cv2.waitKey(0)
cv2.destroyAllWindows()





corner_selector()
