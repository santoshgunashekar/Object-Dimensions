from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import numpy as np
import argparse
import imutils
import cv2


image = cv2.imread("Images\late.png", 0)
maxsize = (1028, 1028)
tn_image = image.thumbnail(maxsize, PIL.Image.ANTIALIAS)
cv2.imwrite('Images\late_o.png',tn_image)