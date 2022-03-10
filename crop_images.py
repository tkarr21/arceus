import cv2
import numpy as np
import os

current_dir = "assets/arm"

# Get name of every file in directory, store in list
all_files = os.listdir(current_dir)

for img in all_files:
	# Make sure the file is a png file.
	if img[-3:] == 'png':
		# Read in the image, keep the Alpha values
		image = cv2.imread(current_dir + "/" + img, cv2.IMREAD_UNCHANGED)
		#cv2.imshow('image', image)
		#cv2.waitKey()
		original = image.copy()
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
		binary = cv2.bitwise_not(thresh)

		x,y,w,h = cv2.boundingRect(binary)
		#cv2.rectangle(image, (x,y), (x + w, y + h), (36,255,12), 2)
		ROI = original[y:y+h, x:x+w]
	
		cv2.imwrite(current_dir + "/" + img, ROI)


#####################################################################################################
# Below was my tests to get it to work for a single image.

"""
# Load image, convert to grayscale, Gaussian blur, Otsu's threshold
image = cv2.imread('arceus-main/assets/head/156.png', cv2.IMREAD_UNCHANGED)
original = image.copy()
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (3,3), 0)
thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
binary = cv2.bitwise_not(thresh)
#thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV)[1]

# Obtain bounding rectangle and extract ROI
x,y,w,h = cv2.boundingRect(binary)
print(x,y,w,h)
#cv2.rectangle(image, (x, y), (x + w, y + h), (36,255,12), -1)
ROI = original[y:y+h, x:x+w]

# Add alpha channel
b,g,r,alpha = cv2.split(ROI)
#alpha = np.ones(b.shape, dtype=b.dtype) * 200
ROI = cv2.merge([b,g,r,alpha])

cv2.imshow('thresh', thresh)
cv2.imshow('image', image)
cv2.imshow('ROI', ROI)
cv2.waitKey()
cv2.imwrite("output.png", ROI)
"""
