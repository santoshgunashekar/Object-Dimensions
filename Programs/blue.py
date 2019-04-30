# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 09:53:07 2019

@author: Santosh
"""

import cv2
import numpy as np
img = cv2.imread("Images\shiva4.jpeg")
b,g,r = cv2.split(img)
cv2.imwrite("Images\blue.jpeg", b )