import numpy as np
import cv2

def distorion_correction():
  cv2.namedWindow("window1")

  input_camera = None  #user enter camera index
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


  src = frame
  vc.release()
  # cv2.destroyWindow("window1")
  cv2.destroyAllWindows()
  # src    = cv2.imread("distortedImage.jpg")
  width = src.shape[1]
  height = src.shape[0]

  distCoeff = np.zeros((4, 1), np.float64)

  # TODO: add your coefficients here!
  k1 = 0.0e-7;  # negative to remove barrel distortion
  k2 = 0.0;
  p1 = 0.0;
  p2 = 0.0;

  distCoeff[0, 0] = k1;
  distCoeff[1, 0] = k2;
  distCoeff[2, 0] = p1;
  distCoeff[3, 0] = p2;

  # assume unit matrix for camera
  cam = np.eye(3, dtype=np.float32)

  cam[0, 2] = width / 2.0  # define center x
  cam[1, 2] = height / 2.0  # define center y
  cam[0, 0] = 10.  # define focal length x
  cam[1, 1] = 10.  # define focal length y

  # here the undistortion will be computed
  dst = cv2.undistort(src, cam, distCoeff)

  return dst