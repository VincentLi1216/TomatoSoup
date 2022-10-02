import time
import cv2

def save_img(img, file_name = ""):
    t = time.localtime()
    name = file_name + time.strftime("_%m-%d-%Y_%H:%M:%S.jpg", t)
    cv2.imwrite(name, img)
    print(name, "saved")
    return name


