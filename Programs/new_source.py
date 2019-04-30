# -*- coding: utf-8 -*-
"""
Created on Sat Apr 20 20:24:54 2019

@author: Santosh
"""
from scipy.spatial import distance as dist
import cv2
import numpy as np
import imutils
def viewImage(image):
    cv2.namedWindow('Display', cv2.WINDOW_NORMAL)
    cv2.imshow('Display', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    

image = cv2.imread('Image\image5.jpeg')
image1 = image

hsv_img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
viewImage(hsv_img) ## 1


green_low = np.array([45 , 100, 50] )
green_high = np.array([75, 255, 255])
curr_mask = cv2.inRange(hsv_img, green_low, green_high)
hsv_img[curr_mask > 0] = ([75,255,200])
viewImage(hsv_img) ## 2
## converting the HSV image to Gray inorder to be able to apply 
## contouring


RGB_again = cv2.cvtColor(hsv_img, cv2.COLOR_HSV2RGB)
gray = cv2.cvtColor(RGB_again, cv2.COLOR_RGB2GRAY)
viewImage(gray) ## 3
gray = cv2.GaussianBlur(gray, (5, 5), 0)
viewImage(gray)
ret, threshold = cv2.threshold(gray, 100, 255, 0)
#viewImage(threshold)
#threshold = cv2.Canny(threshold, 150, 255)
#viewImage(threshold)
#threshold = cv2.dilate(threshold, None, iterations=1)
#viewImage(threshold)
#threshold = cv2.erode(threshold, None, iterations=1)

#viewImage(threshold) ## 4


contours =  cv2.findContours(threshold.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(contours)
count=1
for c in cnts:
    if cv2.contourArea(c) < 3000:
        continue
    epsilon = 0.02*cv2.arcLength(c,True)
    approx = cv2.approxPolyDP(c,epsilon,True)
    
    print(approx)
    for i in range(1, len(approx)):
        print(dist.euclidean(approx[i-1], approx[i]))
    print(dist.euclidean(approx[0], approx[-1]))
    print("Hey")
    cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
    M = cv2.moments(c)
    cX = int((M["m10"] / M["m00"]))
    cY = int((M["m01"] / M["m00"]))
    #cv2.putText(image, count, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    count=count+1
    viewImage(image)
    #cv2.waitKey(0)
#cv2.drawContours(image, contours, -1, (0, 0, 255), 3)
#viewImage(image) ## 5