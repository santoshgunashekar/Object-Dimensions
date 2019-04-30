# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 19:15:13 2019

@author: Santosh
"""

import numpy as np
import cv2
from matplotlib import pyplot as plt

img = cv2.imread('i3.jpeg')
img1= cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
dst = cv2.fastNlMeansDenoisingColored(img,None,10,10,7,21)

plt.subplot(121),plt.imshow(img)
plt.subplot(122),plt.imshow(dst)
plt.show()
cv2.imwrite('outputo1.jpeg',dst)