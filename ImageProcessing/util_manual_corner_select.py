import cv2
from util_perspective_transform import *
from util_distortion_correction import *
from util_save_img import *


# 變數初始化
dots = []  # 記錄座標的空串列
dot_num = 0  # 已經寫入的dot數
tolerance = 30  # 重新選點時的最大誤差
index = None  # 錯誤點對應到的dots[]參數
fix_phase = 0  # 目前修正階段, phase % 2 = 1代表已經選擇好錯誤點, phase%2 = 0代表起始狀態或錯誤以被修正
# frame = distorion_correction()
origin_frame = None
frame = None

def get_frame():
    global frame
    frame = distorion_correction()
    # save_img(frame, "orig")

def corner_selector():
    global dots
    global dot_num
    global index
    global fix_phase
    global origin_frame

    get_frame()

    # frame = distorion_correction()

    origin_frame = frame.copy()  # 將原始frame進行快照，以便未來修正點可以清除後重新畫線






    dots = get_json_data("user_pref.json", "corners")



    if len(dots) == 4:
        dot_num = 4

        for i in range(4):


            cv2.circle(frame, (dots[i][0], dots[i][1]), 10, (0, 255, 0), -1)  # 在點擊的位置，繪製（藍色）圓形

        for i in range(3):
            cv2.line(frame, (dots[i][0], dots[i][1]), (dots[i+1][0], dots[i+1][1]), (0, 255, 0), 2)  # 取得最後的兩個座標，繪製直線

        cv2.line(frame, (dots[0][0], dots[0][1]), (dots[3][0], dots[3][1]), (0, 255, 0), 2)  # 取得最後的兩個座標，繪製直線

        cv2.imshow('TomatoSoup - Press \"Q\" to confirm corners', frame)





    def show_xy(event, x, y, flags, param):
        global dot_num
        global index
        global fix_phase
        global origin_frame
        global frame





        if event == 1:

            if fix_phase % 2 == 1:  # 第六點(修正點）重新繪製

                # 將視窗回復原始樣貌
                frame = origin_frame.copy()
                cv2.imshow('TomatoSoup - Press \"Q\" to confirm corners', frame)

                dots[index] = [x, y]  # 將錯誤點座標改成修正點

                # 畫線
                for i in range(4):
                    cv2.circle(frame, (dots[i][0], dots[i][1]), 10, (0, 0, 255), -1)  # 在點擊的位置，繪製圓形
                    if i != 3:
                        x1 = dots[i][0]
                        y1 = dots[i][1]
                        x2 = dots[i + 1][0]
                        y2 = dots[i + 1][1]
                        cv2.line(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                    else:
                        x1 = dots[dot_num - 4][0]
                        y1 = dots[dot_num - 4][1]
                        x2 = dots[dot_num - 1][0]
                        y2 = dots[dot_num - 1][1]
                        cv2.line(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)  # 取得第一和第四個座標，繪製直線

                index = None

                cv2.imshow('TomatoSoup - Press \"Q\" to confirm corners', frame)

            if dot_num == 4 and fix_phase % 2 == 0:  # 第五點（錯誤點）確認
                for i in range(4):
                    if abs(dots[i][0] - x) <= tolerance and abs(dots[i][1] - y) <= tolerance:
                        index = i
                        # print(i)
                        cv2.circle(frame, (dots[index][0], dots[index][1]), 10, (255, 0, 0), -1)  # 在點擊的位置，繪製（藍色）圓形
                        cv2.imshow('TomatoSoup - Press \"Q\" to confirm corners', frame)
                        fix_phase += 1

                    if index != None:
                        break
            elif dot_num == 4:
                fix_phase += 1

            if dot_num < 4 and index == None:  # 一到四點正常畫線

                dots.append([x, y])  # 記錄座標
                cv2.circle(frame, (x, y), 10, (0, 0, 255), -1)  # 在點擊的位置，繪製圓形
                cv2.imshow('TomatoSoup - Press \"Q\" to confirm corners', frame)
                dot_num = len(dots)  # 目前有幾個座標
                # print(dot_num)

                if dot_num > 1:  # 二到三點畫線
                    x1 = dots[dot_num - 2][0]
                    y1 = dots[dot_num - 2][1]
                    x2 = dots[dot_num - 1][0]
                    y2 = dots[dot_num - 1][1]
                    cv2.line(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)  # 取得最後的兩個座標，繪製直線

                if dot_num == 4:  # 第四點畫線
                    x1 = dots[dot_num - 4][0]
                    y1 = dots[dot_num - 4][1]
                    x2 = dots[dot_num - 1][0]
                    y2 = dots[dot_num - 1][1]
                    cv2.line(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)  # 取得第一和第四個座標，繪製直線

                cv2.imshow('TomatoSoup - Press \"Q\" to confirm corners', frame)

    cv2.imshow('TomatoSoup - Press \"Q\" to confirm corners', frame)
    cv2.setMouseCallback('TomatoSoup - Press \"Q\" to confirm corners', show_xy)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # 將四個點依照象限排列
    dots.sort(key=lambda s: s[0])

    sorted_dots = []
    if dots[2][1] < dots[3][1]:
        sorted_dots.append(dots[2])
        sorted_dots.append(dots[3])
    else:
        sorted_dots.append(dots[3])
        sorted_dots.append(dots[2])

    if dots[0][1] > dots[1][1]:
        sorted_dots.append(dots[0])
        sorted_dots.append(dots[1])
    else:
        sorted_dots.append(dots[1])
        sorted_dots.append(dots[0])
    # print(sorted_dots)

    put_json_data("user_pref.json", ["corners", sorted_dots])

    fixed_img = perspective_transform(origin_frame, sorted_dots)

    # cv2.imwrite("prc_img.jpg", fixed_img)
    # save_img(fixed_img, "fixed")
    return fixed_img




if __name__ == "__main__":
    print(corner_selector())