import math
import glob
# from PIL import Image
import time
import cv2 as cv
import numpy as np
from util_histogram_equalization import *
from util_convolution import *
from util_crop import *

file_name = None
filter_size = 0
images, gray_normalized, result = [], [], []
horizontal_lines, vertical_lines, intersection_points, corner_each_quadrant = [], [], [], []
quadrant_1_corner, quadrant_2_corner, quadrant_3_corner, quadrant_4_corner = [], [], [], []
gray_normalized_kernel_horizontal, gray_normalized_kernel_vertical = None, None
nr, nc = 0, 0
hough_lines_threshold = 600    # Hough_lines的Threshold 預設為 600
canny_threshold = 80           # Canny的Threshold 預設為 80
src, src2 = None, None

def return_time():    # 回傳當前時間
    seconds = time.time()
    now = time.localtime(seconds)
    return str("{:04d}{:02d}{:02d}_{:02d}{:02d}{:02d}".format(now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec))

def Hough_lines(hough_lines_threshold, img, horizontal_or_vertical):   # 做 霍夫直線偵測
    # global src
    global file_name
    img = np.uint8(img)
    dst = cv.Canny(img, canny_threshold, canny_threshold, None, 3)   # 霍夫直線偵測要先Canny

    cv.imwrite("developing_images\\" + f'{file_name}' + "_gray_normalized_kernel_" + f'{horizontal_or_vertical}' + "_" + f'{filter_size}' + "_canny_" + f'{canny_threshold}' + "-" + f'{canny_threshold}' + ".jpg", dst)  # 生成 Canny 的結果圖

    lines = cv.HoughLines(dst, 1, np.pi / 360, hough_lines_threshold)
    global horizontal_lines
    global vertical_lines
    if horizontal_or_vertical == "horizontal":   # 因為卷積的圖，垂直線的圖跟水平線的圖是分開的，所以houghlines偵測也要分兩次，一次偵測垂直線，一次水平線
        horizontal_lines = []
    if horizontal_or_vertical == "vertical":
        vertical_lines = []
    if lines is not None:
        for i in range(0, len(lines)):
            rho = lines[i][0][0]
            theta = lines[i][0][1]
            a = math.cos(theta)
            b = math.sin(theta)
            x0 = (a * rho)
            y0 = (b * rho)
            pt1 = [int(x0 + 5000 * (-b)), int(y0 + 5000 * a)]
            pt2 = [int(x0 - 5000 * (-b)), int(y0 - 5000 * a)]
            if (pt1[0] - pt2[0]) == 0:   # 計算直線斜率
                slope = (pt1[1] - pt2[1]) / (10 ** (-1))   # 避免pt1[0]-pt2[0]==0 (x的變化量)，導致分母為0
            else:
                slope = (pt1[1] - pt2[1]) / (pt1[0] - pt2[0])
            if (slope < 1) and (slope > -1):   # 依照斜率歸類為 水平線
                horizontal_lines.append([pt1[0], pt1[1], slope])
                cv.line(src, pt1, pt2, (0, 0, 255), 2, cv.LINE_AA)
            elif (slope > 1) or (slope < -1):   # 依照斜率歸類為 垂直線
                vertical_lines.append([pt1[0], pt1[1], slope])
                cv.line(src, pt1, pt2, (0, 0, 255), 2, cv.LINE_AA)



def Get_intersection_points():    # 拿直線方程式取交點
    # eq: slope*x - y = slope*x0 - y0
    global intersection_points
    intersection_points = []
    print("Horizontal Lines Founded:", len(horizontal_lines))
    print("Vertical Lines Founded:", len(vertical_lines))
    for horizontal_line in horizontal_lines:
        for vertical_line in vertical_lines:
            coefficient = np.array([[horizontal_line[2], -1], [vertical_line[2], -1]])
            constant = np.array([[horizontal_line[2] * horizontal_line[0] - horizontal_line[1]],
                                 [vertical_line[2] * vertical_line[0] - vertical_line[1]]])
            intersection_point = np.linalg.solve(coefficient, constant)
            intersection_points.append([int(intersection_point[0][0]), int(intersection_point[1][0])])
            cv.circle(src, (int(intersection_point[0][0]), int(intersection_point[1][0])), 5, (255, 0, 0), -1)

def quadrant_categorization():    # 將所有的交點分類成4個象限
    global quadrant_1_corner
    global quadrant_2_corner
    global quadrant_3_corner
    global quadrant_4_corner
    quadrant_1_corner, quadrant_2_corner, quadrant_3_corner, quadrant_4_corner = [], [], [], []
    for j in intersection_points:
        if (j[0] > nc / 2) and (j[1] < nr / 2):
            quadrant_1_corner.append(j)
        elif (j[0] < nc / 2) and (j[1] < nr / 2):
            quadrant_2_corner.append(j)
        elif (j[0] < nc / 2) and (j[1] > nr / 2):
            quadrant_3_corner.append(j)
        elif (j[0] > nc / 2) and (j[1] > nr / 2):
            quadrant_4_corner.append(j)

def all_quadrants_include_intersection():   # 檢查是不是每個象限都有找到交點
    quadrants_include_intersection = 0
    for quadrant in range(1, 5):
        if globals()['quadrant_' + str(f'{quadrant}') + '_corner'] == []:
            return False
        else:
            quadrants_include_intersection += 1
    if quadrants_include_intersection == 4:
        return True
    else:
        print("all_quadrants_include_intersection() error!")
        return "Error"

def fine_corner_condition(quadrant):   # 判斷水平線有沒有靠近圖片中心，過度遠離的不算；垂直線有沒有遠離圖片中心，過度靠近的不算
    max_d = 0
    temp_corner = []
    for point in globals()['quadrant_' + str(f'{quadrant}') + '_corner']:
        if (abs(point[0] - (nc/2)) > nc/5) and (abs(point[1] - (nr/2)) > nr/5):  # (距離中心點>max_d)&(距離邊界>40px)&(點不能超出邊界)
            d = math.sqrt((point[0] - nc / 2) ** 2 + (point[1] - nr / 2) ** 2)
            if (d >= max_d):
                temp_corner = point
                max_d = d
            print(temp_corner)
    return temp_corner

def fine_distance_to_edge(x, y):  # 判斷：交點是否位於靠近圖片外圍的區域
    # if (abs(x - (nc / 2)) < (nc / 6)) and (abs(y - (nr / 2)) < (nr / 6)):  # (距離中心點 < 1/6)
    #     return True
    # else:
    #     return False
    return True

def find_4_corners():   # 找出4個角落點
    while (all_quadrants_include_intersection() == False):
        decrease_threshold_then_redo_houghlines_and_get_intersections()

    for quadrant in range(1, 5):   # 做條件判斷，如果有交點不符合條件，則降低Hough_lines的Threshold，然後全部重新再算一次
        temp_corner = fine_corner_condition(quadrant)
        while (fine_distance_to_edge(temp_corner[0], temp_corner[1]) == False):
            decrease_threshold_then_redo_houghlines_and_get_intersections()
            temp_corner = fine_corner_condition(quadrant)
        corner_each_quadrant.append(temp_corner)

    for corner in corner_each_quadrant:   # 畫出4個角落點
        cv.circle(src, (int(corner[0]), int(corner[1])), 15, (0, 255, 0), -1)

def Perspective_transform():   # 透視轉換
    pts1 = np.float32(
        [corner_each_quadrant[0], corner_each_quadrant[1], corner_each_quadrant[2], corner_each_quadrant[3]])
    pts2 = np.float32([[corner_each_quadrant[0][0] - corner_each_quadrant[1][0], 0], [0, 0],
                       [0, corner_each_quadrant[2][1] - corner_each_quadrant[1][1]],
                       [corner_each_quadrant[0][0] - corner_each_quadrant[1][0],
                        corner_each_quadrant[2][1] - corner_each_quadrant[1][1]]])
    T = cv.getPerspectiveTransform(pts1, pts2)
    img2 = cv.warpPerspective(src2, T, (corner_each_quadrant[0][0] - corner_each_quadrant[1][0], corner_each_quadrant[2][1] - corner_each_quadrant[1][1]))
    return img2

def decrease_threshold_then_redo_houghlines_and_get_intersections():   # 當一整套流程走下來沒有辦法找到有效的四點時，就執行這個function（=降threshold再走一次整套流程）
    global hough_lines_threshold
    global gray_normalized_kernel_horizontal
    global gray_normalized_kernel_vertical
    hough_lines_threshold -= 10
    Hough_lines(hough_lines_threshold, gray_normalized_kernel_vertical, "vertical")
    # Hough_lines(hough_lines_threshold, gray_normalized_kernel_horizontal, "horizontal")
    Get_intersection_points()
    quadrant_categorization()


def houghlines_blackboard(file_name, src_from_webcam):
    global filter_size
    global horizontal_lines
    global vertical_lines
    global intersection_points
    global corner_each_quadrant
    global hough_lines_threshold
    global quadrant_1_corner
    global quadrant_2_corner
    global quadrant_3_corner
    global quadrant_4_corner
    global nr
    global nc
    global gray_normalized_kernel_horizontal
    global gray_normalized_kernel_vertical
    global src
    global src2
    global images
    global gray_normalized
    global result

    src = src_from_webcam

    # filter_size預設為33
    filter_size = 33

    print("-----\nFilename:", file_name)

    gray_normalized = histogram_equalization(src)  # 呼叫副程式做 直方圖標準化
    gray_normalized_kernel_horizontal, gray_normalized_kernel_vertical = convolution(file_name, gray_normalized,
                                                                                     filter_size)  # 呼叫副程式做 卷積
    gray_normalized_kernel_horizontal = crop(gray_normalized_kernel_horizontal)  # 呼叫副程式做 裁切
    gray_normalized_kernel_vertical = crop(gray_normalized_kernel_vertical)  # 呼叫副程式做 裁切

    print("Hough_lines Starts...\nPlease wait for a few seconds or minutes...\n")
    src = crop(src)
    nr, nc = src.shape[:2]
    # img.shape => (rows, columns)
    src2 = src.copy()

    Hough_lines(hough_lines_threshold, gray_normalized_kernel_vertical, "vertical")  # 霍夫直線偵測 找垂直線
    Hough_lines(hough_lines_threshold, gray_normalized_kernel_horizontal, "horizontal")  # 霍夫直線偵測 找水平線
    Get_intersection_points()  # 拿直線方程式取交點
    quadrant_categorization()  # 將所有的交點分類成4個象限
    find_4_corners()  # 找出4個角落點
    decrease_threshold_then_redo_houghlines_and_get_intersections()  # 降threshold，再走一次偵測流程
    result = Perspective_transform()  # 透視轉換

    cv.imwrite("developing_images\\" + f'{file_name}' + "_gray_normalized.jpg", gray_normalized)  # 生成 灰階圖
    cv.imwrite(
        "developing_images\\" + f'{file_name}' + "_gray_normalized_kernel_horizontal_" + f'{filter_size}' + ".jpg",
        gray_normalized_kernel_horizontal)  # 生成 水平卷積 的結果圖
    cv.imwrite(
        "developing_images\\" + f'{file_name}' + "_gray_normalized_kernel_vertical_" + f'{filter_size}' + ".jpg",
        gray_normalized_kernel_vertical)  # 生成 垂直卷積 的結果圖
    cv.imwrite(
        "developing_images\\" + f'{file_name}' + "_gray_normalized_kernel_canny_houghlines_" + f'{canny_threshold}' + "-" + f'{canny_threshold}' + "-" + f'{hough_lines_threshold}' + ".jpg",
        src)  # 生成 霍夫直線偵測 的結果圖
    cv.imwrite("developing_images\\" + f'{file_name}' + "_final_result.jpg", result)  # 生成 透視轉換後 的結果圖

    print("\nHough_lines Finished.\n")
    print("\"" + f'{file_name}' + "\" DONE.\n-----")



if __name__ == "__main__":
    while 1:
        if (filter_size < 5) or (filter_size % 2 == 0):
            # filter_size: 33 is default
            filter_size = int(input("Convolution Filter Size (n*n)\nDefault: 33*33\nPlease type in the n you want(odd and >=5): "))    # 使用者輸入卷積的Filter大小
        else:
            break

    start = time.time()  # 記錄開始執行程式的時間
    file_name = "FFC01EC6-E6F4-4FFF-BBD8-DFC4D0E0A6E1-16.9"
    img_to_houghlines = cv.imread("developing_images\\" + f'{file_name}' + ".jpg", 1)
    houghlines_blackboard(file_name, img_to_houghlines)

    # cv.imwrite("developing_images\\" + f'{file_name}' + "_gray_normalized_kernel_canny_houghlines_" + f'{canny_threshold}' + "-" + f'{canny_threshold}' + "-" + f'{hough_lines_threshold}' + ".jpg",src)
    # cv.imwrite("developing_images\\" + f'{file_name}' + "_gray_normalized.jpg", gray_normalized)  # 生成 灰階圖
    # cv.imwrite("developing_images\\" + f'{file_name}' + "_gray_normalized_kernel_horizontal_" + f'{filter_size}' + ".jpg", gray_normalized_kernel_horizontal)  # 生成 水平卷積 的結果圖
    # cv.imwrite("developing_images\\" + f'{file_name}' + "_gray_normalized_kernel_vertical_" + f'{filter_size}' + ".jpg", gray_normalized_kernel_vertical)  # 生成 垂直卷積 的結果圖
    # cv.imwrite("developing_images\\" + f'{file_name}' + "_gray_normalized_kernel_canny_houghlines_" + f'{canny_threshold}' + "-" + f'{canny_threshold}' + "-" + f'{hough_lines_threshold}' + ".jpg", src)  # 生成 霍夫直線偵測 的結果圖
    # cv.imwrite("developing_images\\" + f'{file_name}' + "_final_result.jpg", result)  # 生成 透視轉換後 的結果圖

    # cv.imwrite("images_todo\\results\\" + f'{file_name}' + "_final_result.jpg", img2)  # 在"images_todo/results"資料夾內生成 透視轉換後 的結果圖

    end = time.time()  # 記錄程式結束執行的時間
    print("Code Runtime: {:.1f}s".format(end - start))  # 印出程式執行所花的時間

    # cv2.imshow('My Image', src)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()