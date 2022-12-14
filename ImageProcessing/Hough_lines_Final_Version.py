'''
這是主程式!!!
若想要執行程式，請先將想要掃描的圖片放入"images_todo"資料夾內，然後再直接執行此主程式，掃描結果會生成在"results"資料夾內
'''

import math
import glob
from PIL import Image
import time
import cv2 as cv
import numpy as np
from util_histogram_equalization import *
from util_convolution import *
from util_crop import *

image_formats = ['.jpg','.png','.bmp']
filter_size = 0
images = []
horizontal_lines, vertical_lines, intersection_points, corner_each_quadrant = [], [], [], []
hough_lines_threshold = 0       # Hough_lines的Threshold下方會做設定，這邊只是先產生變數而已
canny_threshold = 60       # Canny的Threshold 預設為 60
quadrant_1_corner, quadrant_2_corner, quadrant_3_corner, quadrant_4_corner = [], [], [], []

def return_time():    # 回傳當前時間
    seconds = time.time()
    now = time.localtime(seconds)
    return str("{:04d}{:02d}{:02d}_{:02d}{:02d}{:02d}".format(now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec))

def main(file_name):
    global horizontal_lines
    global vertical_lines
    global intersection_points
    global corner_each_quadrant
    global hough_lines_threshold
    global quadrant_1_corner
    global quadrant_2_corner
    global quadrant_3_corner
    global quadrant_4_corner
    horizontal_lines, vertical_lines, intersection_points, corner_each_quadrant = [], [], [], []
    hough_lines_threshold = 550       # Hough_lines的Threshold 預設為 550
    quadrant_1_corner, quadrant_2_corner, quadrant_3_corner, quadrant_4_corner = [], [], [], []
    nr, nc = 0, 0

    print("-----\nFilename:", file_name)

    gray_normalized = histogram_equalization(file_name)    # 呼叫副程式做 直方圖標準化
    cv.imwrite(f'{file_name}'+"_gray_normalized.jpg", gray_normalized)    # 生成 灰階圖

    gray_normalized_kernel_horizontal, gray_normalized_kernel_vertical = convolution(file_name, gray_normalized, filter_size)    # 呼叫副程式做 卷積
    gray_normalized_kernel_horizontal = crop(gray_normalized_kernel_horizontal)    # 呼叫副程式做 裁切
    gray_normalized_kernel_vertical = crop(gray_normalized_kernel_vertical)    # 呼叫副程式做 裁切
    cv.imwrite(f'{file_name}'+"_gray_normalized_kernel_horizontal_"+f'{filter_size}'+".jpg", gray_normalized_kernel_horizontal)    # 生成 水平卷積 的結果圖
    cv.imwrite(f'{file_name}'+"_gray_normalized_kernel_vertical_"+f'{filter_size}'+".jpg", gray_normalized_kernel_vertical)    # 生成 垂直卷積 的結果圖

    print("Hough_lines Starts...\nPlease wait for a few seconds or minutes...\n")
    src = cv.imread("images_todo\\"+f'{file_name}'+".jpg", 1)
    src = crop(src)
    nr, nc = src.shape[:2]
    # img.shape => (rows, columns)
    src2 = src.copy()



    def Hough_lines(hough_lines_threshold, img, horizontal_or_vertical):    # 做 霍夫直線偵測
        img = np.uint8(img)
        dst = cv.Canny(img, canny_threshold, canny_threshold, None, 3)    # 霍夫直線偵測包含Canny

        cv.imwrite(f'{file_name}'+"_gray_normalized_kernel_"+f'{horizontal_or_vertical}'+"_"+f'{filter_size}'+"_canny_"+f'{canny_threshold}'+"-"+f'{canny_threshold}'+".jpg", dst)    # 生成 Canny 的結果圖

        lines = cv.HoughLines(dst, 1, np.pi / 360, hough_lines_threshold)
        global horizontal_lines
        global vertical_lines
        if horizontal_or_vertical == "horizontal":
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
                if (pt1[0] - pt2[0]) == 0:                            # 計算直線斜率
                    slope = (pt1[1] - pt2[1]) / (10**(-1))            # 避免pt1[0]-pt2[0]==0 (x的變化量)，導致分母為0
                else:
                    slope = (pt1[1] - pt2[1]) / (pt1[0] - pt2[0])
                if (slope < 1) and (slope > -1):                        # 依照斜率歸類為 水平線
                    horizontal_lines.append([pt1[0],pt1[1],slope])
                    cv.line(src, pt1, pt2, (0, 0, 255), 2, cv.LINE_AA)
                elif (slope > 1) or (slope < -1):                        # 依照斜率歸類為 垂直線
                    vertical_lines.append([pt1[0],pt1[1],slope])
                    cv.line(src, pt1, pt2, (0, 0, 255), 2, cv.LINE_AA)



    def Get_intersection_points():    # 拿直線方程式取交點
        # eq: slope*x - y = slope*x0 - y0
        global intersection_points
        intersection_points = []
        print("Horizontal Lines Founded:", len(horizontal_lines))
        print("Vertical Lines Founded:", len(vertical_lines))
        for horizontal_line in horizontal_lines:
            for vertical_line in vertical_lines:
                coefficient = np.array([ [horizontal_line[2],-1] , [vertical_line[2],-1] ])
                constant = np.array([ [horizontal_line[2]*horizontal_line[0]-horizontal_line[1]] , [vertical_line[2]*vertical_line[0]-vertical_line[1]] ])
                intersection_point = np.linalg.solve(coefficient,constant)
                intersection_points.append( [int(intersection_point[0][0]) , int(intersection_point[1][0])] )
                cv.circle(src, (int(intersection_point[0][0]),int(intersection_point[1][0])), 5, (255,0,0), -1)



    def quadrant_categorization():    # 將所有的交點分類成4個象限
        global quadrant_1_corner
        global quadrant_2_corner
        global quadrant_3_corner
        global quadrant_4_corner
        quadrant_1_corner, quadrant_2_corner, quadrant_3_corner, quadrant_4_corner = [], [], [], []
        for j in intersection_points:
            if (j[0] > nc/2) and (j[1] < nr/2):
                quadrant_1_corner.append(j)
            elif (j[0] < nc/2) and (j[1] < nr/2):
                quadrant_2_corner.append(j)
            elif (j[0] < nc/2) and (j[1] > nr/2):
                quadrant_3_corner.append(j)
            elif (j[0] > nc/2) and (j[1] > nr/2):
                quadrant_4_corner.append(j)



    def Find_4_corners():    # 找出4個角落點
        global hough_lines_threshold
        list_included_values = 0
        while list_included_values < 4:    # while迴圈判斷：四個象限內是否都存在交點，若否，則降低Hough_lines的Threshold
            list_included_values = 0
            for quadrant in range(1, 5):
                if globals()['quadrant_'+str(f'{quadrant}')+'_corner'] == []:
                    hough_lines_threshold -= 10
                    print("Current Threshold:", hough_lines_threshold)
                    Hough_lines(hough_lines_threshold, gray_normalized_kernel_vertical, "vertical")
                    Hough_lines(hough_lines_threshold, gray_normalized_kernel_horizontal, "horizontal")
                    Get_intersection_points()
                    quadrant_categorization()
                    break
                else:
                    list_included_values += 1

        def find_corner_in_each_quadrant(quadrant):    # 判斷：交點是否過度貼近邊界，甚至跑到圖片外。找到符合條件且距離中心點最遠的點
            max_d = 0
            temp_corner = []
            for point in globals()['quadrant_'+str(f'{quadrant}')+'_corner']:
                if (math.sqrt((point[0]-nc/2)**2+(point[1]-nr/2)**2) > max_d) and ((nc/2)-abs(point[0]-(nc/2)) > 40) and ((nr/2)-abs(point[1]-(nr/2)) > 40) and (abs(point[0]-(nc/2))<=(nc/2)) and (abs(point[1]-(nr/2))<=(nr/2)):   # (距離中心點>max_d)&(距離邊界>40px)&(點不能超出邊界)
                    max_d = math.sqrt((point[0]-nc/2)**2+(point[1]-nr/2)**2)
                    temp_corner = point
            return temp_corner

        def fine_distance_to_edge(x, y):    # 判斷：交點是否位於靠近圖片外圍的區域
            if (abs(x-(nc/2)) > (nc/6)) and (abs(y-(nr/2)) > (nr/6)):   # (距離中心點 > 1/6)
                return True
            else:
                return False

        for quadrant in range(1,5):    # 做條件判斷，如果有交點不符合條件，則降低Hough_lines的Threshold，然後全部重新再算一次
            reasonable_point = False
            temp_corner = find_corner_in_each_quadrant(quadrant)
            while reasonable_point is False:
                if fine_distance_to_edge(temp_corner[0], temp_corner[1]) is True:
                    corner_each_quadrant.append(temp_corner)
                    reasonable_point = True
                else:
                    hough_lines_threshold -= 10
                    print("Current Threshold:", hough_lines_threshold)
                    Hough_lines(hough_lines_threshold, gray_normalized_kernel_vertical, "vertical")
                    Hough_lines(hough_lines_threshold, gray_normalized_kernel_horizontal, "horizontal")
                    Get_intersection_points()
                    quadrant_categorization()
                    temp_corner = find_corner_in_each_quadrant(quadrant)

        for corner in corner_each_quadrant:    # 畫出4個角落點
            cv.circle(src, (int(corner[0]),int(corner[1])), 15, (0, 255, 0), -1)



    def Perspective_transform():    # 透視轉換
        pts1 = np.float32([corner_each_quadrant[0], corner_each_quadrant[1], corner_each_quadrant[2], corner_each_quadrant[3]])
        pts2 = np.float32([[corner_each_quadrant[0][0]-corner_each_quadrant[1][0], 0], [0, 0], [0, corner_each_quadrant[2][1]-corner_each_quadrant[1][1]], [corner_each_quadrant[0][0]-corner_each_quadrant[1][0], corner_each_quadrant[2][1]-corner_each_quadrant[1][1]]])
        T = cv.getPerspectiveTransform(pts1, pts2)
        img2 = cv.warpPerspective(src2, T, (corner_each_quadrant[0][0]-corner_each_quadrant[1][0], corner_each_quadrant[2][1]-corner_each_quadrant[1][1]))
        return img2



    Hough_lines(hough_lines_threshold, gray_normalized_kernel_vertical, "vertical")    # 霍夫直線偵測 找垂直線
    Hough_lines(hough_lines_threshold, gray_normalized_kernel_horizontal, "horizontal")    # 霍夫直線偵測 找水平線

    Get_intersection_points()    # 拿直線方程式取交點

    Find_4_corners()    # 找出4個角落點
    # print('4 corners:',corner_each_quadrant)

    # print("hough_lines_threshold:", hough_lines_threshold)
    # print('Intersection Points [x, y]:', intersection_points)
    # print('Intersection Points:', len(intersection_points))

    img2 = Perspective_transform()    # 透視轉換

    cv.imwrite(f'{file_name}'+"_gray_normalized_kernel_canny_houghlines_"+f'{canny_threshold}'+"-"+f'{canny_threshold}'+"-"+f'{hough_lines_threshold}'+".jpg", src)    # 生成 霍夫直線偵測 的結果圖
    cv.imwrite(f'{file_name}' + "_final_result.jpg", img2)    # 生成 透視轉換後 的結果圖
    cv.imwrite("images_todo\\results\\" + f'{file_name}' + "_final_result.jpg", img2)    # 在"images_todo/results"資料夾內生成 透視轉換後 的結果圖

    print("\nHough_lines Finished.\n")
    print("\"" + f'{file_name}'+ "\" DONE.\n-----")
    return img2


if __name__ == "__main__":
    start = time.time()    # 記錄開始執行程式的時間
    while 1:
        if (filter_size < 5) or (filter_size % 2 == 0):
            # filter_size: 33 is default
            filter_size = int(input("Convolution Filter Size (n*n)\nDefault: 33*33\nPlease type in the n you want(odd and >=5): "))    # 使用者輸入卷積的Filter大小
        else:
            break
    for formats in image_formats:    # 抓取"images_todo"資料夾內所有要掃描的圖片
        for file in glob.glob("images_todo\\*"+f'{formats}', recursive=True):
            file_name = file[(file.find('\\')+1):]
            file_name = file_name[:file_name.find('.')]
            main(file_name)    # 執行主程式
            images.append( Image.open("images_todo\\results\\" + f'{file_name}' + "_final_result.jpg") )
    image1 = images[0]
    images.pop(0)
    image1.save("images_todo\\results\\"+"Combination_"+f'{return_time()}'+"_filter_"+f'{filter_size}'+".pdf", save_all=True, append_images=images)    # 輸出合併後的PDF檔
    print("Saved File:", "images_todo/results/"+"Combination_"+f'{return_time()}'+".pdf")    # 印出PDF檔的路徑及檔名
    end = time.time()    # 記錄程式結束執行的時間
    print("Code Runtime: {:.1f}s".format(end-start))    # 印出程式執行所花的時間