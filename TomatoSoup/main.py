import cv2

def show_xy(event,x,y,flags,userdata):
    print(event,x,y,flags)
    # 印出相關參數的數值，userdata 可透過 setMouseCallback 第三個參數垂遞給函式

cv2.namedWindow("preview")
vc = cv2.VideoCapture(2)

rval, frame = vc.read()

while True:

  if frame is not None:
     cv2.imshow("preview", frame)
  rval, frame = vc.read()

  if cv2.waitKey(1) & 0xFF == ord('q'):
     break

cv2.setMouseCallback('preview', show_xy)  # 設定偵測事件的函式與視窗

cv2.waitKey(0)     # 按下任意鍵停止
cv2.destroyAllWindows()


# import cv2
# img= cv2.imread('bo8pb5ljodhxnar2q3up_31b96e78-ef2e-4023-b23f-ebffb388944a.png')          #定義圖片位置
# img= cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  #轉化為灰度圖
# def onmouse(event, x, y, flags, param):   #標準滑鼠互動函式
#     if event==cv2.EVENT_MOUSEMOVE:      #當滑鼠移動時
#         print(img[y,x])           #顯示滑鼠所在畫素的數值，注意畫素表示方法和座標位置的不同
# def main():
#     cv2.namedWindow("img")          #構建視窗
#     cv2.setMouseCallback("img", onmouse)   #回撥繫結視窗
# while True:               #無限迴圈
#     cv2.imshow("img",img)        #顯示影象
#     if cv2.waitKey() == ord('q'):break  #按下‘q'鍵，退出
#     cv2.destroyAllWindows()         #關閉視窗
# if __name__ == '__main__':          #執行
#     main()

# import cv2
# img = cv2.imread('bo8pb5ljodhxnar2q3up_31b96e78-ef2e-4023-b23f-ebffb388944a.png')
#
def show_xy(event,x,y,flags,userdata):
    print(event,x,y,flags)
    # 印出相關參數的數值，userdata 可透過 setMouseCallback 第三個參數垂遞給函式
#
# cv2.imshow('oxxostudio', img)
# cv2.setMouseCallback('oxxostudio', show_xy)  # 設定偵測事件的函式與視窗
#
# cv2.waitKey(0)     # 按下任意鍵停止
# cv2.destroyAllWindows()

