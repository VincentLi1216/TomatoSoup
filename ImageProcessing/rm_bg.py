import cv2
import numpy as np
import time

start_time = time.time()
img = cv2.imread("IMG_2918.JPG")

print(img.shape)
height = img.shape[0]
width = img.shape[1]
print(width, height)

tolerance = 100
rm_b = 74
rm_g = 74
rm_r = 60

for y in range(height):
    for x in range(width):
        if abs(img[y][x][0]-rm_b) < tolerance and abs(img[y][x][1]-rm_g) < tolerance and abs(img[y][x][2]-rm_r) < tolerance:
            img[y][x] = [255, 0, 0]

cv2.imshow('My Image', img)
end_time = time.time()
print("duration:", end_time-start_time)
cv2.waitKey(0)
cv2.destroyAllWindows()