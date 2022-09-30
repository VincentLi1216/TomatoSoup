import cv2

cv2.namedWindow("taking shots")
  vc = cv2.VideoCapture(0)
  vc.set(cv2.CAP_PROP_FRAME_WIDTH, 2160)
  vc.set(cv2.CAP_PROP_FRAME_HEIGHT, 1440)

  rval, frame = vc.read()

  while True:

    if frame is not None:
      cv2.imshow("window1", frame)
    rval, frame = vc.read()

    if cv2.waitKey(1) & 0xFF == ord('q'):

      break