<<<<<<< HEAD
# from util_dst_cs_M import corner_selector
from houghlines_blackboard import *
=======
from util_dst_cs_M import corner_selector
<<<<<<< HEAD
from perspective_transform import perspective_transform

# print(corner_selector())
corner_selector()
=======
from crop_blackboard import *
>>>>>>> b618ffbf91f6293872cd36fa63bd58265a1a432a


# print(corner_selector())

<<<<<<< HEAD


file_name = "FFC01EC6-E6F4-4FFF-BBD8-DFC4D0E0A6E1-16.9"
img_to_houghlines = cv.imread("developing_images\\" + f'{file_name}' + ".jpg", 1)
result_img = houghlines_blackboard(img_to_houghlines)
cv2.imshow("result_img", result_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
=======
# file_name = "FFC01EC6-E6F4-4FFF-BBD8-DFC4D0E0A6E1-16.9"
# crop_blackboard(file_name)
>>>>>>> f05c32838bba837277698a1e043c83d3a10b5b8d
>>>>>>> b618ffbf91f6293872cd36fa63bd58265a1a432a
