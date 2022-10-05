import time
import cv2
import os

t = time.localtime()
date = str(time.strftime("%m-%d-%Y", t))

def save_img(img, file_name = ""):

    name = file_name + time.strftime("_%m-%d-%Y_%H:%M:%S.jpg", t)

    folder_path = "imgs/" + date + "/"

    #如果沒有當天的資料夾的話，就自己創一個
    if not os.path.isdir(folder_path):
        os.mkdir(folder_path)

    cv2.imwrite(folder_path + name, img)
    print(name, "saved")
    return name

if __name__ == "__main__":
    # t = time.localtime()
    # folder_name = time.strftime("imgs/%m-%d-%Y/", t)
    # print(folder_name)
    print("hi")
