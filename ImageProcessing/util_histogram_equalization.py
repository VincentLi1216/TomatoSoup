'''
這是副程式。
'''

import numpy as np
import cv2 as cv

def histogram_equalization(file_name):
    img1 = cv.imread("developing_images\\"+f'{file_name}'+".jpg", 0)
    nr, nc = img1.shape[:2]
    # img.shape => (rows, columns)
    print("Image Size: {} x {} (Horizontal x Vertical)".format(nc, nr))    # 印出圖片尺寸
    print("\nHistogram Equalization Starts...")

    def normalization(data):    # 標準化
        return (data - np.min(data)) / (np.max(data) - np.min(data)) * 255
    img1 = normalization(img1)

    print("Histogram Equalization Finished.")

    # cv.imwrite(f'{file_name}'+"_gray_normalized.jpg", img1)

    return img1

if __name__ == "__main__":
    # file_name = str(input("Paste the filename: "))
    file_name = "20220522_222935"
    histogram_equalization(file_name)