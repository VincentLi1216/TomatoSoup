'''
這是副程式。
'''

import numpy as np
import cv2

def crop(img):
    nr, nc = img.shape[:2]
    crop = 20
    img = img[crop:nr - crop, crop:nc - crop]
    # cv2.imwrite("cropped.jpg", img)

    return img

if __name__ == '__main__':
    src = cv2.imread("20220521_162319.jpg", 1)
    crop(src)