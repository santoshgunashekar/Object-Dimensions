
from scipy.spatial import distance as dist
from imutils import perspective
import numpy as np
import imutils
import math
import cv2

def viewImage(image):
    cv2.namedWindow('Display', cv2.WINDOW_NORMAL)
    cv2.imshow('Display', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def midpoint(ptA, ptB):
	return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)


#image = cv2.imread('Images\late.png')
image = cv2.imread('Programs\Image\image9.jpeg')
#thresh = cv2.threshold(image, 100, 255, cv2.THRESH_BINARY)
#viewImage(thresh)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
print(cv2.HuMoments(cv2.moments(gray)).flatten())
viewImage(gray)

kernel = np.ones((5,5),np.float32)/25
#for i in range(5):
gray = cv2.filter2D(gray,-1,kernel)
gray = cv2.GaussianBlur(gray, (5, 5), 0)
viewImage(gray)


ret,threshold = cv2.threshold(gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
viewImage(threshold)


edged = cv2.Canny(gray, 0.50*ret, ret)
viewImage(edged)

for i in range(5):
    edged = cv2.dilate(edged, kernel, iterations=1)
    #viewImage(edged)


    edged = cv2.erode(edged, kernel, iterations=1)
viewImage(edged)
#viewImage(threshold) ## 4

width=24.97
pixelsPerMetric=1
contour =  cv2.findContours(edged.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(contour)
count=1
prev=0
#print(len(cnts))
for c in cnts:
    print(count)
    if cv2.contourArea(c) < 2000:
        #print('Small')
        continue
    
    M = cv2.moments(c)
    cX1 = int((M["m10"] / M["m00"]))
    cY1= int((M["m01"] / M["m00"]))
    print('The midpoints of the contour are:')
    print(cX1, cY1)
    epsilon = 0.02*cv2.arcLength(c,True)
    approx = cv2.approxPolyDP(c,epsilon,True)
    
    
    if count==1:
        c=cv2.convexHull(c)
        epsilon = 0.0001*cv2.arcLength(c,True)
        approx = cv2.approxPolyDP(c,epsilon,True)
        left_most=approx[0]
        right_most=approx[-1]
        for i in range(len(approx)):
            if approx[i][0][0] < left_most[0][0]:
                left_most=approx[i]
            if approx[i][0][0] > right_most[0][0]:
                right_most=approx[i]
        #print(approx)
        print(left_most, right_most)
        print(abs(left_most[0][0]-right_most[0][0])/width)
        pixelsPerMetric = abs(left_most[0][0]-right_most[0][0])/width
        center, radius = cv2.minEnclosingCircle(approx)
        print(radius)
        
        orig = image.copy()
        s = cv2.arcLength(c,True)
        s1=s/math.pi
        print(s,s1)
        #if pixelsPerMetric is None:
            #pixelsPerMetric = s1 / width
        print(pixelsPerMetric)
        
    else:
        center, radius = cv2.minEnclosingCircle(approx)
        orig=image.copy()
        c=cv2.convexHull(c)
        print(approx)
        counter=0;
        
        if(len(approx)>=8):
            s=0
            for i in range(len(approx)):
                s=s+(dist.euclidean(approx[i-1], approx[i]))/pixelsPerMetric
            s1 = cv2.arcLength(c,True)
            s2=s1/math.pi
            print(s2/pixelsPerMetric, s/math.pi)
            print("Hi circle")
            cv2.circle(orig, (int(center[0]), int(center[1])), int(radius), -1)
            cv2.putText(orig, "{:.2f}".format(s2/pixelsPerMetric),
    		(int(center[0]), int(center[1])), cv2.FONT_HERSHEY_SIMPLEX, 0.65,
            (255, 255, 255), 2)
            #cv2.putText(orig, "{:.2f}".format((dist.euclidean(approx[0], approx[-1]))/pixelsPerMetric), (int(center[0]), int(center[1])), cv2.FONT_HERSHEY_SIMPLEX, 0.65,(255, 255, 255), 2)
        else:   
            for i in range(len(approx)):
                print(i)
                tlblX, tlblY = approx[i-1][0][0], approx[i-1][0][1]
                tlblX1, tlblY1 = approx[i][0][0], approx[i][0][1]
                print((dist.euclidean(approx[i-1], approx[i]))/pixelsPerMetric)
                x=int((tlblX+tlblX1)/2) - 15
                y=int((tlblY+tlblY1)/2) - 10
                print('Mid point is' )
                print((tlblX+tlblX1)/2, (tlblY+tlblY1)/2)
                cv2.putText(orig, "{:.2f}".format((dist.euclidean(approx[i-1], approx[i]))/pixelsPerMetric),
		          (x, y), cv2.FONT_HERSHEY_SIMPLEX, 
                 0.65, (255, 255, 255), 2)
                
        print("Hey")
    cv2.drawContours(orig, [c], -1, (0, 255, 0), 2)
    count=count+1
    viewImage(orig)