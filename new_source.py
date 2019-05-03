# -*- coding: utf-8 -*-
"""
Created on Sat Apr 20 20:24:54 2019

@author: Santosh
"""
from scipy.spatial import distance as dist
from imutils import perspective
import numpy as np
import math
import imutils
import cv2
def viewImage(image):
    cv2.namedWindow('Display', cv2.WINDOW_NORMAL)
    cv2.imshow('Display', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def midpoint(ptA, ptB):
	return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)

image = cv2.imread('Programs\Image\image10.jpeg')

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (5, 5), 0)
ret, threshold = cv2.threshold(gray, 95, 255, cv2.THRESH_BINARY)
#viewImage(threshold)
edged = cv2.Canny(gray, 50, 100)
viewImage(edged)
edged = cv2.dilate(edged, None, iterations=1)
edged = cv2.erode(edged, None, iterations=1)

#viewImage(threshold) ## 4

width=24.97
pixelsPerMetric=None
contour =  cv2.findContours(edged.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(contour)
count=1
s=0
for c in cnts:
    if cv2.contourArea(c) < 3000:
        continue
    epsilon = 0.02*cv2.arcLength(c,True)
    approx = cv2.approxPolyDP(c,epsilon,True)
    if count==1:
        # compute the rotated bounding box of the contour
        orig = image.copy()
        for i in range(1, len(approx)):
            #sum=sum+dist.euclidean(approx[i-1], approx[i])
            s=s+dist.euclidean(approx[i-1], approx[i])
        #sum=sum+dist.euclidean(approx[-1], approx[0])
        s=s+dist.euclidean(approx[0], approx[-1])
        s1=s/math.pi
        print(s1)
        if pixelsPerMetric is None:
            pixelsPerMetric = s1 / width
        print(pixelsPerMetric)
        
    elif (len(approx)>6):
        s2=0
        print(approx)
        for i in range(1, len(approx)):
            s2=s2+((dist.euclidean(approx[i-1], approx[i]))/pixelsPerMetric)
        s2=s2+((dist.euclidean(approx[0], approx[-1]))/pixelsPerMetric)
        s3=s2/math.pi
        print(s3)
        print("Hi Circle")
        
    else:
        for i in range(1, len(approx)):
            #sum=sum+dist.euclidean(approx[i-1], approx[i])
            print(dist.euclidean(approx[i-1], approx[i]))
            print((dist.euclidean(approx[i-1], approx[i]))/pixelsPerMetric)
        #sum=sum+dist.euclidean(approx[-1], approx[0])
        print((dist.euclidean(approx[0], approx[-1])))
        print((dist.euclidean(approx[i-1], approx[i]))/pixelsPerMetric)
        #sum/=len(approx)
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