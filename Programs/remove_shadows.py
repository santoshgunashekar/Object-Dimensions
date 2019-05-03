# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 09:37:49 2019

@author: Santosh
"""

import cv2
import numpy as np

img = cv2.imread('Image\image7.jpeg', -1)

rgb_planes = cv2.split(img)

result_planes = []
result_norm_planes = []
for plane in rgb_planes:
    dilated_img = cv2.dilate(plane, np.ones((7,7), np.uint8))
    bg_img = cv2.medianBlur(dilated_img, 21)
    diff_img = 255 - cv2.absdiff(plane, bg_img)
    arr = np.array([])
    norm_image = cv2.normalize(diff_img, arr, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
    result_planes.append(diff_img)
    result_norm_planes.append(norm_image)

result = cv2.merge(result_planes)
result_norm = cv2.merge(result_norm_planes)

cv2.imwrite('i71.jpeg', result)
cv2.imwrite('i711.jpeg', result_norm)