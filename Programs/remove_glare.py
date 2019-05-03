#matplotlib inline

from matplotlib import pyplot as plt
import cv2
import numpy as np
#import os, sys
def _imshow(image,title):
    cv2.namedWindow(title, cv2.WINDOW_NORMAL)
    cv2.imshow(title, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
def _imshow1(I, theTitle=None):
    if len(I.shape) == 3:
        cv2.imshow(theTitle,I)
        #imshow(I)x
    else:
        if I.min() == 0 and I.max() == 1:
            cv2.imshow(I, cmap="gray")
        else:
            cv2.imshow(I, cmap="gray",vmin=0,vmax=255)
    cv2.xticks([])
    cv2.yticks([])
    if theTitle:
        cv2.title(theTitle);
	
image_in = cv2.cvtColor(cv2.imread("Image\image7.jpeg"), cv2.COLOR_BGR2RGB); # Load the glared image
h, s, v = cv2.split(cv2.cvtColor(image_in, cv2.COLOR_RGB2HSV)) # split into HSV components

plt.subplot(1,4,1); _imshow(image_in, "original")
plt.subplot(1,4,2); _imshow(h, "Hue")
plt.subplot(1,4,3); _imshow(s, "Saturation")
plt.subplot(1,4,4); _imshow(v, "Brightness")

nonSat = s < 180 # Find all pixels that are not very saturated

# Slightly decrease the area of the non-satuared pixels by a erosion operation.
disk = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
nonSat = cv2.erode(nonSat.astype(np.uint8), disk)

# Set all brightness values, where the pixels are still saturated to 0.
v2 = v.copy()
v2[nonSat == 0] = 0;

plt.subplot(1,3,1); _imshow(nonSat, "s > 180")
plt.subplot(1,3,2); _imshow(v, "Original\nBrightness")
plt.subplot(1,3,3); _imshow(v2, "Masked\nBrightness")

plt.subplot(1,2,1); plt.hist(v2.flatten(), bins=50);  # draw the histogram of pixel brightnesses
plt.xlabel("Brightness value");
plt.ylabel("Frequency");
plt.title("Brightness histogram")

glare = v2 > 200;    # filter out very bright pixels.
# Slightly increase the area for each pixel
glare = cv2.dilate(glare.astype(np.uint8), disk);  
glare = cv2.dilate(glare.astype(np.uint8), disk);
plt.subplot(1,2,2); _imshow(glare,'Glare');
plt.title("Glare mask");

corrected = cv2.inpaint(image_in, glare, 5, cv2.INPAINT_NS)
plt.subplot(1,3,1); _imshow(image_in, "Original")
plt.subplot(1,3,2); _imshow(glare, "Glare Mask")
plt.subplot(1,3,3); _imshow(corrected, "Corrected");

