import cv2
from util_json import *
from util_server_communicator import *
import time
import glob
import os

def cam_cap():
    cv2.namedWindow("TomatoSoup - Press \"Q\" to capture")
    cv2.setWindowProperty("TomatoSoup - Press \"Q\" to capture", cv2.WND_PROP_TOPMOST, 1) ##永遠置頂窗口

    default_cam = get_json_data("user_pref.json", "last_used_camera")

    use_default_cam = None

    if default_cam != None:
        while use_default_cam != "y" and use_default_cam != "n" and use_default_cam != "d":
            use_default_cam = input("Would you like to use cam " + str(default_cam) + " again(y/n)?")
        if use_default_cam == "y":
            input_camera = default_cam
        elif use_default_cam == "d":
            t = time.localtime()
            date = str(time.strftime("%m-%d-%Y", t))

            list_of_files = glob.glob("imgs/" + date + "/*.jpg")  #取得當天資料夾中所有的.jpg
            latest_file = max(list_of_files, key=os.path.getctime)  #取得資料夾中最新的檔案

            img = cv2.imread(latest_file)
            cv2.imshow("TomatoSoup - Press \"Q\" to confirm the deletion", img)
            cv2.setWindowProperty("TomatoSoup - Press \"Q\" to confirm the deletion", cv2.WND_PROP_TOPMOST, 1)  ##永遠置頂窗口
            cv2.waitKey(0)
            cv2.destroyAllWindows()

            os.remove(latest_file)  #刪除本機端檔案
            latest_file = os.path.basename(latest_file)  #取得檔案名稱就好，不需要路徑

            remove("/home/ubuntu/static/" + date + "/" + latest_file)  #刪除伺服器端檔案

            os._exit(0)

            return
        else:
            input_camera = None  # user enter camera index
            while input_camera == None or int(input_camera) > 3 or int(input_camera) < 0:
                input_camera = int(input("Please enter the camera you would like to use(0~3):"))
    else:
        input_camera = None  # user enter camera index
        while input_camera == None or int(input_camera) > 3 or int(input_camera) < 0:
            input_camera = int(input("Please enter the camera you would like to use(0~3):"))

    put_json_data("user_pref.json", ["last_used_camera", input_camera])


    vc = cv2.VideoCapture(input_camera)

    vc.set(cv2.CAP_PROP_FRAME_WIDTH, 3840)
    vc.set(cv2.CAP_PROP_FRAME_HEIGHT, 2160)

    rval, frame = vc.read()

    while True:

        if frame is not None:
            cv2.imshow("TomatoSoup - Press \"Q\" to capture", frame)
        rval, frame = vc.read()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


    vc.release()
    cv2.destroyAllWindows()

    return frame