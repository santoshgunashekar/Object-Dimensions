"""
    Module to input a preprocessed image and get the contours in it
    and for every contour, detect the edges, the corner of the edges,
    compute the distance in the image and scale them to real world dimensions
"""

#import the necessary packages
import cv2
from scipy.spatial import distance as dist
from imutils import contours
import imutils
import Final.preprocess as pp
import math

def process(image, edged, width):
    """
    Function to process an image and find the dimension of objects in it
     Parameters
     ----------
     image: str
         Path and name of the original image
     edged : uint8
         Pre-processed image
     width: float
            Width of the leftmost (standard reference) object
     """
    
    #Read the original image
    image = cv2.imread(image)
    
    #Set the Pixel Per Metric as None initially
    pixelsPerMetric=None
    
    #find the contours in the image and store them
    contour =  cv2.findContours(edged.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(contour)
    (cnts,_)=contours.sort_contours(cnts)
    #counter to distinguish the reference object from other objects in the image
    count=1
    
    #loop through the contours
    for c in cnts:
        
        #Get a copy of the original image
        orig=image.copy()
        
        #Check for convexity defects and correct them
        c=cv2.convexHull(c)
        
        #Ignore minor contours which are noises mostly
        if cv2.contourArea(c) < 2000:
            continue

        #epsilon here defines how precisely the edges of a contour in the image
        epsilon = 0.02*cv2.arcLength(c,True)
        
        #Approximates a contour to another shape with less number of vertices
        approx = cv2.approxPolyDP(c,epsilon,True)
        
        #if the contour is the reference object
        if count==1:
            
            #epsilon is very fine here since the left-most and righ-most 
            #point of the refernce object is to be determined
            epsilon = 0.0001*cv2.arcLength(c,True)
            approx = cv2.approxPolyDP(c,epsilon,True)
            
            #assume the first point is the left most 
            #and the last point is the right most point of reference object
            left_most=approx[0]
            right_most=approx[-1]
            
            #loop over the points of the reference object to find the
            #left most and right most point
            for i in range(len(approx)):
                if approx[i][0][0] < left_most[0][0]:
                    left_most=approx[i]
                if approx[i][0][0] > right_most[0][0]:
                    right_most=approx[i]
                    
            #It defines the ratio of number of pixels in the image
            #to the real distance
            pixelsPerMetric = abs(left_most[0][0]-right_most[0][0])/width
            
            #Displaying the ratio and drawing the contour
            print('Pixel Per Metric Ratio is: ',(pixelsPerMetric))
            cv2.drawContours(orig, [c], -1, (0, 255, 0), 2)
            
        #If the contour is not the reference object
        else:
            
            #If the contour is a circle
            if(len(approx)>=8):
                
                #Find the center and minimum radius fitting the contour
                center, radius = cv2.minEnclosingCircle(approx)
                
                #Compute the circumference of the circle
                s2=cv2.arcLength(c,True)/math.pi    
                
                #Making sure the contour is definitely a circle
                if cv2.isContourConvex(c):
                    
                    #Draw a circle around the contour
                    cv2.circle(orig, (int(center[0]), int(center[1])),
                               int(radius), (0,255,0), thickness=2, lineType=8, shift=0)
                
                #Write the dimension of the image
                cv2.putText(orig, "{:.2f}".format(s2/pixelsPerMetric),
        		(int(center[0]), int(center[1])), cv2.FONT_HERSHEY_SIMPLEX, 0.65,
                (0, 0, 255), 2)
                
            #If the contour is not a circle
            else:
                
                #loop over the vertices of the object (contour)
                for i in range(len(approx)):
                    
                    #Get the coordinates of current and previous vertex
                    tlblX, tlblY = approx[i-1][0][0], approx[i-1][0][1]
                    tlblX1, tlblY1 = approx[i][0][0], approx[i][0][1]
                    
                    #Find the midpoint of these two vertices
                    x=int((tlblX+tlblX1)/2) - 15
                    y=int((tlblY+tlblY1)/2) - 10
                    
                    #Write the dimensions near the midpoint
                    cv2.putText(orig, "{:.2f}".format((dist.euclidean(approx[i-1], approx[i]))/pixelsPerMetric),
    		          (x, y), cv2.FONT_HERSHEY_SIMPLEX, 
                     0.65, (0, 0, 255), 2)
                    
                    #draw the contour on the image
                    cv2.drawContours(orig, [c], -1, (0, 255, 0), 2)
                    
        #counter to keep track of objects or shapes identified              
        count=count+1
        
        #viewing the image with dimensions for each contour
        pp.viewImage(orig,'')
    