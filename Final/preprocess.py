"""
    Module to preprocess an image - includes conversion to grayscale,
    blurring, thresholding, canny edge detection, dilation and erosion
"""
#import the necessary packages
import cv2
import numpy as np

def viewImage(image, name):
     """
     Function to view an image
     Parameters
     ----------
     image : str
         Image being pre-processed
     name : str
         Name of the image that is displayed
     """
     cv2.namedWindow(name, cv2.WINDOW_NORMAL)
     cv2.imshow(name, image)
     cv2.waitKey(0)
     cv2.destroyAllWindows()

def writeImage(name, image):
    """
    Function to write an image
     Parameters
     ----------
     image : str
         Image being pre-processed
     name : str
         Path and name of the image that is written
     """
    cv2.imwrite(name, image)

def process(image):
    """
    Function to pre-process an image
     Parameters
     ----------
     image : str
         Path of the image that needs to be pre-processed
     """
     
     #Loads an image from a file
    image = cv2.imread(image)
    
    #Converts the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    viewImage(gray, 'Grayscale image')
    
    #Blurs the image which helps in further processing
    kernel = np.ones((5,5),np.float32)/25
    gray = cv2.filter2D(gray,-1,kernel)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    viewImage(gray, 'Blurred image')
    
    #Thresholding or binarizing of imnage is done here
    ret,threshold = cv2.threshold(gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    viewImage(threshold, 'Binarized image')
    
    #Canny edge detection is made use to detect edges from binarized image
    edged = cv2.Canny(gray, 0.5*ret, ret)
    viewImage(edged, 'Canny edge detection')
    
    #The edges in the images are dilated and eroded so that edges that are
    #detached while processing is connected again
    for i in range(5):
        edged = cv2.dilate(edged, kernel, iterations=1)
        edged = cv2.erode(edged, kernel, iterations=1)
    viewImage(edged, 'Dilated and Eroded edges')
    
    return edged

def init(path):  
    """
        Method to initialize the path
        Parameters:
        ----------
        image: str
            Path and name of the image to be processed
    """
    image=path
    edged = process(image)
    return edged