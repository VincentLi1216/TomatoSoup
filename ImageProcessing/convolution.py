'''
這是副程式。
'''

import numpy as np
import cv2 as cv
import scipy.signal

def convolution(file_name, gray_normalized, filter_size):
    print("\nConvolution Starts...\nPlease wait for a few seconds...")

    # --------------- 生成 水平 方向的Mask ---------------
    kernel_horizontal = np.ones((filter_size, filter_size), dtype='int')
    kernel_horizontal[ int((filter_size-1)/2-1):int((filter_size-1)/2+2) , : ] *= 0
    kernel_horizontal[ 0:int((filter_size-1)/2-1) , : ] *= (-1)
    # --------------------------------------------------

    # --------------- 生成 垂直 方向的Mask ---------------
    kernel_vertical = np.ones((filter_size, filter_size), dtype='int')
    kernel_vertical[ : , int((filter_size-1)/2-1):int((filter_size-1)/2+2) ] *= 0
    kernel_vertical[ : , 0:int((filter_size-1)/2-1) ] *= (-1)
    # --------------------------------------------------

    result_horizontal = scipy.signal.convolve(gray_normalized, kernel_horizontal, 'same')    # 水平卷積
    result_vertical = scipy.signal.convolve(gray_normalized, kernel_vertical, 'same')    # 垂直卷積

    def normalization(data):    # 標準化
        return (data - np.min(data)) / (np.max(data) - np.min(data)) * 255

    result_horizontal = normalization(abs(result_horizontal))    # 卷積後也要做一次標準化
    result_vertical = normalization(abs(result_vertical))    # 卷積後也要做一次標準化

    print("Convolution Finished.\n")

    # cv.imwrite(f'{file_name}'+"_gray_normalized_kernel_horizontal_"+f'{filter_size}'+".jpg", result_horizontal)
    # cv.imwrite(f'{file_name}'+"_gray_normalized_kernel_vertical_"+f'{filter_size}'+".jpg", result_vertical)

    return result_horizontal, result_vertical


if __name__ == "__main__":
    # file_name = str(input("Paste the filename: "))
    file_name = "20220522_222432"
    convolution(file_name)