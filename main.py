import cv2 as cv
import numpy as np
from skimage import transform as tf
import time
import math


global font
font = 10

img = cv.imread('index.jpg')
img2 = cv.imread('index.jpg', 0)
img_copy = img.copy()
cap = cv.VideoCapture(0)
if cap.isOpened():
  ret, frame = cap.read()
  fsubground = cv.createBackgroundSubtractorMOG2()
else:
  ret = False
ret, frame2 = cap.read()

move = False
while ret:
  ret, frame = cap.read()
  fgmask = fsubground.apply(frame)
  kernal = np.ones((9, 9), np.uint8)

  cv.rectangle(frame, (400, 400), (100,100), (0, 255, 0), 0)
  roi = frame[100:400, 100:400]
  hsvim = cv.cvtColor(roi, cv.COLOR_BGR2HSV)
  lower = np.array([0, 48, 80], dtype="uint8")
  upper = np.array([20, 255, 255], dtype="uint8")
  skinRegionHSV = cv.inRange(hsvim, lower, upper)
  #cv.imshow("HSV", hsvim)
  blurred = cv.GaussianBlur(skinRegionHSV, (7, 7), 0)


  ret,thresh = cv.threshold(blurred,0,255,cv.THRESH_BINARY)

  opening = cv.morphologyEx(thresh, cv.MORPH_OPEN, kernal)

  #cv.imshow("thresh", thresh)

  fgmask = cv.erode(opening, kernal, iterations=2)
  fgmask = cv.dilate(opening, kernal, iterations=2)
  fgmask[np.abs(fgmask) < 250] = 0
  #cv.imshow('Background Sub', fgmask)

  contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

  try:
    contours = max(contours, key=lambda x: cv.contourArea(x))
    cv.drawContours(roi, [contours], -1, (255, 255, 0), 2)
    hull = cv.convexHull(contours)
    cv.drawContours(roi, [hull], -1, (0, 255, 255), 2)
    hull = cv.convexHull(contours, returnPoints=False)
    defects = cv.convexityDefects(contours, hull)
    #areahull = cv.contourArea(hull)
    areacnt = cv.contourArea(contours)
    print("value", areacnt)
    if defects is not None:
      cnt = 0
    for i in range(defects.shape[0]):

      # calculate the angle
      s, e, f, d = defects[i][0]
      start = tuple(contours[s][0])
      end = tuple(contours[e][0])
      far = tuple(contours[f][0])
      a = np.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
      b = np.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
      c = np.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)
      angle = np.arccos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c))


      #cosine theorem
      if angle <= np.pi / 2:
        # angle less than 90 degree, treat as fingers
        cnt += 1
        cv.circle(roi, far, 4, [255, 0, 0], -1)
        Q = cv.moments(contours)
        if Q['m00'] != 0:
          cx = int(Q['m10'] / Q['m00'])
          cy = int(Q['m01'] / Q['m00'])
          center = (cx, cy)
          cv.circle(roi, center, 7, (0, 255, 255), -1)

    if cnt >= 0:
      cnt = cnt+1
      cv.putText(roi, str(cnt), (0, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv.LINE_AA)

      if cnt == 1:
        if (areacnt > 8000 and areacnt < 10000):
          font += 1

      if (areacnt > 14000 and areacnt < 16000 ):
          cnt =6
      if cnt == 6:
        #draw
        img_copy = img.copy()
        cv.circle(img, (cx, cy), font, (0, 0, 255), -1)
        cv.imshow("drawing", img)


      if cnt == 2:
        if (areacnt > 12000 and areacnt < 14000):

          if not move:
            last = far
            move = True
          row, col, depth = img.shape
          n = (far[0] - last[0], far[1] - last[1])
          dst = cv.resize(img, (col + n[0], row + n[0]))
          cv.imshow("Scaling", dst)
      if cnt == 3:
          if not move:
            last = far
            move = True
          row, col, depth = img.shape
          n = (far[0] - last[0], far[1] - last[1])
          m = np.float32([[1, 0, n[0]], [0, 1, n[1]]])
          dst = cv.warpAffine(img, m, (row, col))
          cv.imshow("Translation", dst)

      if cnt == 4:
          row, col, depth = img.shape
          M = cv.getRotationMatrix2D((col / 2, row / 2), -90, 1)
          rotate_30 = cv.warpAffine(img, M, (col, row))
          img = rotate_30
          cv.imshow("Rotate", rotate_30)
          time.sleep(0.5)

      if cnt == 5:
          tfSkew = tf.AffineTransform(shear=0.7)
          skew = tf.warp(image=img, inverse_map=tfSkew)
          cv.imshow("Skew", skew)
          rows, cols = img2.shape
          img_output = np.zeros(img2.shape, dtype=img2.dtype)
          for i in range(rows):
            for j in range(cols):
              offset_x = int(128.0 * math.sin(2 * 3.14 * i / (2 * cols)))
              offset_y = 3
              if j + offset_x < cols:
                img_output[i, j] = img2[i, (j + offset_x) % cols]
              else:
                img_output[i, j] = 0
          cv.imshow('Warp', img_output)



  except:
    pass
  cv.imshow('final_result', roi)
  if cv.waitKey(40) == 27:
    break
  #frame1 = frame2
  ret, frame2 = cap.read()


cv.destroyAllWindows()
cap.release()
#cv.imwrite('C:/Users/USER/Desktop/pythonProject1', img)