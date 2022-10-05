import cv2
from util_json import *

def cam_cap():
    cv2.namedWindow("TomatoSoup - Press \"Q\" to capture")
    cv2.setWindowProperty("TomatoSoup - Press \"Q\" to capture", cv2.WND_PROP_TOPMOST, 1) ##永遠置頂窗口

    default_cam = get_json_data("user_pref.json", "last_used_camera")

    use_default_cam = None

    if default_cam != None:
        while use_default_cam == None and use_default_cam != "y" and use_default_cam != "n":
            use_default_cam = input("Would you like to use cam " + str(default_cam) + " again(y/n)?")
        if use_default_cam == "y":
            input_camera = default_cam
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