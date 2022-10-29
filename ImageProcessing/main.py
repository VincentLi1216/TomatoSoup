from util_camera_capture import *
from util_distortion_correction import *
from util_manual_corner_select import *
from util_save_img import *
from util_houghlines_blackboard import *
from util_server_communicator import *


file_name = save_img(corner_selector(), "final")
server_path = "/home/ubuntu/static/" + date + "/" + file_name
put("imgs/" + date + "/" + file_name, server_path)




