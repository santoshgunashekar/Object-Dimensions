# -*- coding: utf-8 -*-
"""
Created on Sun Apr  7 12:43:50 2019

@author: Santosh
"""

import argparse
import imutils
import cv2
 
# construct the argument parser and parse the arguments
 
# load the input image from disk
image = cv2.imread("images\coin.jpeg", 0)
 
# convert the image to grayscale, blur it, and threshold it
#gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(image, (5,5), 0)
thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]

# extract contours from the image
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
 
# loop over the contours and draw them on the input image
for c in cnts:
	cv2.drawContours(image, [c], -1, (0, 0, 255), 2)
 
# display the total number of shapes on the image
text = "I found {} total shapes".format(len(cnts))
cv2.putText(image, text, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
		(0, 0, 255), 2)
 
# write the output image to disk
cv2.imwrite("images\coin_o.jpeg", image)