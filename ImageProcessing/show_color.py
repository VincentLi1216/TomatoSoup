import cv2
img = cv2.imread('IMG_2918.JPG')

def show_xy(event,x,y,flags,param):
    if event == 0:
        img2 = img.copy()                         # 當滑鼠移動時，複製原本的圖片
        cv2.circle(img2, (x,y), 10, (0,0,0), 1)   # 繪製黑色空心圓
        cv2.imshow('IMG_2918.JPG', img2)            # 顯示繪製後的影像
    if event == 1:
        # color = img[y,x]                          # 當滑鼠點擊時
        # print(color)                              # 印出顏色
        coord = [x, y]
        print(coord)

cv2.imshow('IMG_2918.JPG', img)
cv2.setMouseCallback('IMG_2918.JPG', show_xy)

cv2.waitKey(0)
cv2.destroyAllWindows()