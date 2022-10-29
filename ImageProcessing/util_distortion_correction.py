import numpy as np
import cv2
from util_camera_capture import *

def distorion_correction():

  src = cam_cap()

  width = src.shape[1]
  height = src.shape[0]

  distCoeff = np.zeros((4, 1), np.float64)

  # TODO: add your coefficients here!
  k1 = 10e-7;  # negative to remove barrel distortion?>
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