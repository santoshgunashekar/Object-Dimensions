# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 09:04:43 2019

@author: Santosh
"""

import numpy as np
import cv2

img = cv2.imread('Images\hello.png')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
#gray = np.float32(gray)
gray = cv2.GaussianBlur(gray, (7, 7), 0)
        
# perform edge detection, then perform a dilation + erosion to
# close gaps in between object edges
edged = cv2.Canny(gray, 50, 100)
edged = cv2.dilate(edged, None, iterations=1)
edged = cv2.erode(edged, None, iterations=1)

corners = cv2.goodFeaturesToTrack(gray, 100, 0.01, 10)
corners = np.int0(corners)

for corner in corners:
    x,y = corner.ravel()
    cv2.circle(img,(x,y),3,255,-1)
    
cv2.imwrite('Images\hello_o.png',img)   
#cv2.imshow('Corner',img)