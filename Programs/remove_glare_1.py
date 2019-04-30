# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 19:12:11 2019

@author: Santosh
"""

import cv2
import numpy

frame = cv2.imread('i3.jpeg')

if frame is None:
    print('Error loading image')
    exit()    

rows = frame.shape[0]
cols = frame.shape[1]

hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV);

for i in range(0, cols):
    for j in range(0, rows):
        hsv[j, i][1] = 255;

frame = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR);

cv2.imshow("Frame", frame)
cv2.waitKey(0)