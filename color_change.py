import cv2
import numpy as np
import os

image = cv2.imread("5.png", cv2.IMREAD_UNCHANGED)
mask = cv2.imread("5-binary.png")
original = image.copy()
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
binary = cv2.bitwise_not(thresh)

cv2.imwrite("5-binary.png", binary)

_, mask = cv2.threshold(mask, thresh = 180, maxval = 255, type = cv2.THRESH_BINARY)

color_add = np.copy(original)

color_add[(mask==255).all(-1)] = [0, 191, 255, 255]

color_add_w = cv2.addWeighted(color_add, 1.0, image, 0.3, 0, color_add)

cv2.imshow('2', color_add_w)
cv2.imwrite('5-green.png', color_add_w)
cv2.waitKey()
