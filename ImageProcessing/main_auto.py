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
