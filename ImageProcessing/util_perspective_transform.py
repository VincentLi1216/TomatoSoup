import cv2
import numpy as np
from util_json import *

def perspective_transform(img, dots):
    img_size = (3700, 1000)  #轉換至的黑板大小

    # 將四個點依照象限排列
    dots.sort(key=lambda s: s[1])
    sorted_dots = []

    if dots[1][0] <= dots[0][0]:
        sorted_dots.append(dots[0])
        sorted_dots.append(dots[1])
    else:
        sorted_dots.append(dots[1])
        sorted_dots.append(dots[0])
    if dots[2][0] <= dots[3][0]:
        sorted_dots.append(dots[2])
        sorted_dots.append(dots[3])
    else:
        sorted_dots.append(dots[3])
        sorted_dots.append(dots[2])
    print("sorted:", sorted_dots)

    put_json_data("user_pref.json", ["corners", sorted_dots])

    points1 = np.float32([sorted_dots[0], sorted_dots[1], sorted_dots[2], sorted_dots[3]])  #黑板四個角落點
    # points2 = np.float32([[img_size[0], 0], [img_size[0], img_size[1]], [0, img_size[1]], [0,0]])  #轉換至的黑板大小
    points2 = np.float32([[sorted_dots[0][0] - sorted_dots[1][0], 0],
                          [0, 0],
                            [0, sorted_dots[2][1] - sorted_dots[1][1]],
                            [sorted_dots[0][0] - sorted_dots[1][0], sorted_dots[2][1] - sorted_dots[1][1]]])  ##自動比例調整

    M = cv2.getPerspectiveTransform(points1, points2)  #取得轉換矩陣
    warped = cv2.warpPerspective(img, M, (sorted_dots[0][0] - sorted_dots[1][0], sorted_dots[2][1] - sorted_dots[1][1]))  #透視轉換

    cv2.imshow("TomatoSoup - All Set! Press \"Q\" to upload", warped)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return warped



if __name__ == "__main__":
    perspective_transform(cv2.imread("IMG_2918.JPG"), [[3804, 1184], [3817, 2161], [213, 2031], [272, 1156]])