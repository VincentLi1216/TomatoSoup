from util_houghlines_blackboard import *

file_name = return_time()
# file_name = "FFC01EC6-E6F4-4FFF-BBD8-DFC4D0E0A6E1-16.9"
# img_to_houghlines = cv.imread("developing_images\\" + f'{file_name}' + ".jpg", 1)


cv2.namedWindow("window1")

input_camera = None  # user enter camera index
while input_camera == None or int(input_camera) > 3 or int(input_camera) < 0:
    input_camera = int(input("Please enter the camera you would like to use(0~3):"))

vc = cv2.VideoCapture(input_camera)

vc.set(cv2.CAP_PROP_FRAME_WIDTH, 3840)
vc.set(cv2.CAP_PROP_FRAME_HEIGHT, 2160)

rval, frame = vc.read()

while True:

    if frame is not None:
        cv2.imshow("window1", frame)
    rval, frame = vc.read()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


result_img = houghlines_blackboard(file_name, frame)



# vc.release()
# # cv2.destroyWindow("window1")
# cv2.destroyAllWindows()
# print("window destoried")





# cv2.imshow("result_img", result_img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

