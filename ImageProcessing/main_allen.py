# from util_distortion_correction import *
# from util_houghlines_blackboard import *

# file_name = return_time()
# file_name = "FFC01EC6-E6F4-4FFF-BBD8-DFC4D0E0A6E1-16.9"
# img_to_houghlines = cv.imread("developing_images\\" + f'{file_name}' + ".jpg", 1)


# frame = distorion_correction()
# result_img = houghlines_blackboard(file_name, frame)



# vc.release()
# # cv2.destroyWindow("window1")
# cv2.destroyAllWindows()
# print("window destoried")





# cv2.imshow("result_img", frame)
# cv2.waitKey(0)
# cv2.destroyAllWindows()





# from firebase_communicator import *

# print("stopped")



# # sander 1013
#
# from util_camera_capture import *
# from util_distortion_correction import *
# from util_manual_corner_select import *
# from util_save_img import *
# from util_houghlines_blackboard import *
# from util_server_communicator import *
#
#
#
#
# file_name = save_img(corner_selector(), "final")
# server_path = "/home/ubuntu/static/" + date + "/" + file_name
# put("imgs/" + date + "/" + file_name, server_path)







# mine

from allen_return_time import *
from util_camera_capture import *
from util_distortion_correction import *
# from util_manual_corner_select import *
from util_houghlines_blackboard import *
from util_save_img import *
from util_server_communicator import *
from util_manual_corner_select import *

c_time = allen_return_time()

return_img = None
four_corners = None

# try:
#     return_img, four_corners = houghlines_blackboard(c_time, distorion_correction())
#     print(four_corners)
#     cv2.imshow("imshow", return_img)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()
#     return_img = corner_selector(img=return_img, input_dots=four_corners)
# except:
#     print("iam here")
#     return_img = cv2.imread("imgs/IMG_5433.JPG")
#     corner_selector(img=return_img)

# corner_selector(houghlines_blackboard(c_time, distorion_correction()))

return_value = houghlines_blackboard(c_time, distorion_correction())


if len(return_value) != 2120:  #got the corners successfully
    img = return_value[0]
    corners = return_value[1]
    return_img = corner_selector(img, corners)
elif len(return_value) == 2120:  #did not got the corners
    return_img = corner_selector(return_value)


file_name = save_img(return_img , "final" )
server_path = "/home/ubuntu/static/" + date + "/" + file_name
put("imgs/" + date + "/" + file_name, server_path)
