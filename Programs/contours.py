# -*- coding: utf-8 -*-
"""
Created on Sun Apr  7 10:51:19 2019

@author: Santosh
"""

import numpy as np
import cv2
im = cv2.imread('soap.jpeg')
imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(imgray, 127, 255, 0)
im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)