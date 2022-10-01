import cv2

def cam_cap():
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


    vc.release()
    # cv2.destroyWindow("window1")
    cv2.destroyAllWindows()

    return frame
