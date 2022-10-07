import cv2
import numpy as np

def perspective_transform(img, dots_coord):
    img_size = (3700, 1000)  #轉換至的黑板大小

    points1 = np.float32([dots_coord[0], dots_coord[1], dots_coord[2], dots_coord[3]])  #黑板四個角落點
    points2 = np.float32([[img_size[0], 0], [img_size[0], img_size[1]], [0, img_size[1]], [0,0]])  #轉換至的黑板大小



    M = cv2.getPerspectiveTransform(points1, points2)  #取得轉換矩陣

    warped = cv2.warpPerspective(img, M, img_size)  #透視轉換

    cv2.imshow("TomatoSoup - All Set! Press \"Q\" to upload", warped)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return warped



if __name__ == "__main__":
    perspective_transform(cv2.imread("IMG_2918.JPG"), [[3804, 1184], [3817, 2161], [213, 2031], [272, 1156]])