# -*- coding: utf-8 -*-
"""
Created on Sat Apr 20 19:56:54 2019

@author: Santosh
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
#matplotlib inline

image = cv2.imread('Image\image7.jpeg', 0)

if image is None:
    raise ValueError('Image not found!')

# background equalization
max_value = np.max(image)
backgroundRemoved = image.astype(float)
blur = cv2.GaussianBlur(backgroundRemoved, (151,151), 50)
backgroundRemoved = backgroundRemoved/blur
backgroundRemoved = (backgroundRemoved*max_value/np.max(backgroundRemoved)).astype(np.uint8)


fig = plt.figure(figsize=(20, 20))
plt.subplot(311),plt.imshow(image, 'gray'),plt.title('Input'),plt.axis('off')
plt.subplot(312),plt.imshow(backgroundRemoved, 'gray'),plt.title('Background Removed'),plt.axis('off')
cv2.imwrite("bd.png",backgroundRemoved)
ret, thres = cv2.threshold(backgroundRemoved,130,255,cv2.THRESH_BINARY)

# remove horizontal lines
kernel = np.ones((4, 1),np.uint8)
dilation1 = cv2.dilate(thres, kernel, iterations = 1)

# remove vertical lines
kernel = np.ones((1, 4),np.uint8)
dilation2 = cv2.dilate(dilation1, kernel, iterations = 1)

kernel = np.ones((3, 3),np.uint8)
erosion = cv2.erode(dilation2, kernel, iterations = 1)

plt.subplot(313),plt.imshow(erosion, 'gray'),plt.title('Final'),plt.axis('off')
plt.show()

kernel = np.ones((1, 4),np.uint8)
dilation = cv2.dilate(dilation2, kernel, iterations = 1)

kernel = np.ones((3, 3),np.uint8)
erosion = cv2.erode(dilation, kernel, iterations = 1)

fig = plt.figure() 
plt.imshow(erosion, cmap='gray'),plt.title('missmatch')
plt.show()