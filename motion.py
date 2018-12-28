import cv2
import numpy as np
im = cv2.imread('WIN_20181129_13_32_56_Pro.jpg')
img = cv2.imread('WIN_20181129_13_32_56_Pro.jpg',0)
img = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
img = cv2.medianBlur(img,5)
img = cv2.medianBlur(img,5)
cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)

contours = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,20, param1=50,param2=30,minRadius=20 ,maxRadius=40)

final = np.zeros(im.shape,np.uint8)
mask = np.zeros(img.shape,np.uint8)

for i in range(0,len(contours)):
    mask[...]=0
    # cv2.drawContours(mask,contours,i,255,-1)
    cv2.drawContours(final,contours,i,cv2.mean(im,mask),-1)

cv2.imshow('im',im)
cv2.imshow('final',final)
cv2.waitKey(0)