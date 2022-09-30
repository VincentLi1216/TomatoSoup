import cv2
import numpy as np

def perspective_transform(img, dots_coord):
    points1 = np.float32([dots_coord[0], dots_coord[1], dots_coord[2], dots_coord[3]])
    points2 = np.float32([[3541, 0], [3541, 887], [0, 887], [0,0]])

    img_size = (3541, 887)

    M = cv2.getPerspectiveTransform(points1, points2)

    warped = cv2.warpPerspective(img, M, img_size)

    cv2.imshow("display", warped)

    cv2.waitKey(0)
    cv2.destroyAllWindows()



if __name__ == "__main__":
    affine_transform(cv2.imread("IMG_2918.JPG"), [[3804, 1184], [3817, 2161], [213, 2031], [272, 1156]])