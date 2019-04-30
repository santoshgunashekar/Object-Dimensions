# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 11:25:16 2019

@author: Santosh
"""

from shapedetector import ShapeDetector
from scipy.spatial import distance as dist
import argparse
import imutils
import cv2
import numpy as np
from PIL import Image

im = Image.open('shadows_out_norm.png', mode='BGR')
pixels = list(im.getdata())
width, height = im.size
pixels = [pixels[i * width:(i + 1) * width] for i in range(height)]
print(len(pixels))
cnts = cv2.findContours(im.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
sd = ShapeDetector()