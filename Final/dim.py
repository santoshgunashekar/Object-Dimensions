"""
    Module that links both the pre-processing and the 
    estimating the dimensions of the objects in the image
"""

#import necessary packages
import Final.preprocess as pp
import Final.findDimensions as fd

def init(path, width):
    """
    path: str
         Path and name of the original image
    width: float
            Width of the leftmost (standard reference) object
    """
    
    #Get the processed image and pass it to the module that computes dimensions
    edged=pp.init(path)
    fd.process(path, edged, width)