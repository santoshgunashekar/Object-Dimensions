from scipy.spatial import distance as dist
from imutils import perspective
import numpy as np
import imutils
import math
import cv2

output = [] 


def viewImage(image):
    cv2.namedWindow('Display', cv2.WINDOW_NORMAL)
    cv2.imshow('Display', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def midpoint(ptA, ptB):
	return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)

def removeNestings(l): 
    for i in l: 
        if type(i) == list: 
            removeNestings(i) 
        else: 
            output.append(i) 
    return output


#image = cv2.imread('Images\late.png')
image = cv2.imread('Programs\Image\image10.jpeg')
#thresh = cv2.threshold(image, 100, 255, cv2.THRESH_BINARY)
#viewImage(thresh)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
print(cv2.HuMoments(cv2.moments(gray)).flatten())
viewImage(gray)

kernel = np.ones((5,5),np.float32)/25
#for i in range(5):
gray = cv2.filter2D(gray,-1,kernel)
#gray = cv2.GaussianBlur(gray, (5, 5), 0)
viewImage(gray)


ret,threshold = cv2.threshold(gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
viewImage(threshold)


edged = cv2.Canny(gray, 50, 100)
viewImage(edged)

for i in range(5):
    edged = cv2.dilate(edged, kernel, iterations=1)
    #viewImage(edged)


    edged = cv2.erode(edged, kernel, iterations=1)
viewImage(edged)
#viewImage(threshold) ## 4

width=24
pixelsPerMetric=None
contour =  cv2.findContours(edged.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(contour)
count=1
cX=0
cY=0
for c in cnts:
    s=0
    if cv2.contourArea(c) < 2000:
        continue
    epsilon = 0.02*cv2.arcLength(c,True)
    approx = cv2.approxPolyDP(c,epsilon,True)
    print(cv2.minEnclosingCircle(approx))
    
    if count==1:
        c=cv2.convexHull(c)
        # compute the rotated bounding box of the contour compute the center of the contour,
        # then detect the name of the shape using only the contour
        orig = image.copy()
        for i in range(1, len(approx)):
            #sum=sum+dist.euclidean(approx[i-1], approx[i])
            s=s+dist.euclidean(approx[i-1], approx[i])
        #sum=sum+dist.euclidean(approx[-1], approx[0])
        s=s+dist.euclidean(approx[0], approx[-1])
        s1=s/math.pi
        print(s1)
        if pixelsPerMetric is None:
            pixelsPerMetric = s1 / width
        print(pixelsPerMetric)
        
    else:
        orig=image.copy()
        c=cv2.convexHull(c)
        M = cv2.moments(c)
        cX1 = int((M["m10"] / M["m00"]))
        cY1= int((M["m01"] / M["m00"]))
        if dist.euclidean((cX, cY), (cX1, cY1))<1:
            cX=cX1
            cY=cY1
            continue
        print(approx)
        counter=0;
        for i in range(1, len(approx)):
            print((dist.euclidean(approx[i-1], approx[i]))/pixelsPerMetric)
            #s=s+(dist.euclidean(approx[i-1], approx[i]))/pixelsPerMetric
            #print(approx[i-1])
            #print(approx[i])
            tlblX, tlblY = approx[i-1][0][0], approx[i-1][0][1]
            tlblX1, tlblY1 = approx[i][0][0], approx[i][0][1]
            print(tlblX, tlblY)
            print(tlblX1, tlblY1)
            print('Mid point is' )
            print((tlblX+tlblX1)/2, (tlblY+tlblY1)/2)
            #x=int((tlblX+tlblX1)/2) - 15
            #y=int((tlblY+tlblY1)/2) - 10
            
            
        for i in range(len(approx)):
                tlblX, tlblY = approx[i-1][0][0], approx[i-1][0][1]
                tlblX1, tlblY1 = approx[i][0][0], approx[i][0][1]
                #print(tlblX, tlblY)
                #print(tlblX1, tlblY1)
                #print('Mid point is' )
                #print((tlblX+tlblX1)/2, (tlblY+tlblY1)/2)
                x=int((tlblX+tlblX1)/2) - 15
                y=int((tlblY+tlblY1)/2) - 10
                cv2.putText(orig, "{:.2f}".format((dist.euclidean(approx[i-1], approx[i]))/pixelsPerMetric),
		(x, y), cv2.FONT_HERSHEY_SIMPLEX, 
        0.65, (255, 255, 255), 2)
                
        print((dist.euclidean(approx[0], approx[-1]))/pixelsPerMetric)
        s=s+(dist.euclidean(approx[0], approx[-1]))/pixelsPerMetric
        tlblX, tlblY = approx[0][0][0], approx[0][0][1]
        tlblX1, tlblY1 = approx[-1][0][1], approx[-1][0][1]
        print('Mid point is' )
        print((tlblX+tlblX1)/2, (tlblY+tlblY1)/2)
        x=int((tlblX+tlblX1)/2) - 15
        y=int((tlblY+tlblY1)/2) - 10    
        
        if(len(approx)>6):
            s1=0
            for i in range(1,len(approx)):
                s1=s1+(dist.euclidean(approx[i-1], approx[i]))/pixelsPerMetric
            s1=s1+(dist.euclidean(approx[0], approx[-1]))/pixelsPerMetric
            s2=s1/math.pi
            print(s2)
            print("Hi circle")   
            
        cv2.putText(orig, "{:.2f}".format((dist.euclidean(approx[0], approx[-1]))/pixelsPerMetric),
    		(x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.65,
            (255, 255, 255), 2)
                
        print("Hey")
        
    cv2.drawContours(orig, [c], -1, (0, 255, 0), 2)
    
    M = cv2.moments(c)
    cX = int((M["m10"] / M["m00"]))
    cY = int((M["m01"] / M["m00"]))
    #cv2.putText(image, count, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    count=count+1
    viewImage(orig)