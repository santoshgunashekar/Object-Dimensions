"""
    Module that is used by the end-user 
    Takes in image path and reference object width and
    Outputs dimensions of other objects in the image
"""

#import necessary packages
from Final import dim as Dimensions
import argparse


#Construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to the input image")
ap.add_argument("-w", "--width", required=True,
    help="width of the left most (standard) object")
args = vars(ap.parse_args())

#Get the path of the image from the terminal
path = args["image"]

#Get the width of the refernce object
width = float(args["width"])

Dimensions.init(path, width)