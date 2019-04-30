from scipy.spatial import distance as dist
from imutils import perspective
import numpy as np
import imutils
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
image = cv2.imread('i9.jpeg')
#thresh = cv2.threshold(image, 100, 255, cv2.THRESH_BINARY)
#viewImage(thresh)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
viewImage(gray)

kernel = np.ones((5,5),np.float32)/25
#for i in range(5):
gray = cv2.filter2D(gray,-1,kernel)
#gray = cv2.GaussianBlur(gray, (5, 5), 0)
viewImage(gray)


ret,threshold = cv2.threshold(gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
viewImage(threshold)


edged = cv2.Canny(gray, 0.5*ret, ret)
viewImage(edged)

for i in range(5):
    edged = cv2.dilate(edged, kernel, iterations=1)
    #viewImage(edged)


    edged = cv2.erode(edged, kernel, iterations=1)
viewImage(edged)
#viewImage(threshold) ## 4

width=24.97
pixelsPerMetric=None
contour =  cv2.findContours(edged.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(contour)
count=1
cX=0
cY=0
for c in cnts:
    if cv2.contourArea(c) < 200:
        continue
    epsilon = 0.02*cv2.arcLength(c,True)
    approx = cv2.approxPolyDP(c,epsilon,True)
    if count==1:
        # compute the rotated bounding box of the contour compute the center of the contour,
        # then detect the name of the shape using only the contour
        M = cv2.moments(c)
        cX1 = int((M["m10"] / M["m00"]))
        cY1= int((M["m01"] / M["m00"]))
        if dist.euclidean((cX, cY), (cX1, cY1))<1:
            cX=cX1
            cY=cY1
            continue
        orig = image.copy()
        box = cv2.minAreaRect(c)
        box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
        box = np.array(box, dtype="int")

        # order the points in the contour such that they appear in top-left, top-right,
        # bottom-right, and bottom-left order, then draw the outline of the rotated bounding box
        box = perspective.order_points(box)
        cv2.drawContours(orig, [box.astype("int")], -1, (0, 255, 0), 2)

    	 # loop over the original points and draw them
        for (x, y) in box:
            cv2.circle(orig, (int(x), int(y)), 5, (0, 0, 255), -1)
            
	    # unpack the ordered bounding box, then compute the midpoint between the top-left
        # and top-right coordinates, followed by the midpoint between bottom-left and bottom-right coordinates
        (tl, tr, br, bl) = box
        (tltrX, tltrY) = midpoint(tl, tr)
        (blbrX, blbrY) = midpoint(bl, br)

	    # compute the midpoint between the top-left and top-right points, followed by the midpoint between the top-righ and bottom-right
        (tlblX, tlblY) = midpoint(tl, bl)
        (trbrX, trbrY) = midpoint(tr, br)

	    # draw the midpoints on the image
        cv2.circle(orig, (int(tltrX), int(tltrY)), 5, (255, 0, 0), -1)
        cv2.circle(orig, (int(blbrX), int(blbrY)), 5, (255, 0, 0), -1)
        cv2.circle(orig, (int(tlblX), int(tlblY)), 5, (255, 0, 0), -1)
        cv2.circle(orig, (int(trbrX), int(trbrY)), 5, (255, 0, 0), -1)

	    # draw lines between the midpoints
        cv2.line(orig, (int(tltrX), int(tltrY)), (int(blbrX), int(blbrY)),
		 (255, 0, 255), 2)
        cv2.line(orig, (int(tlblX), int(tlblY)), (int(trbrX), int(trbrY)),
		 (255, 0, 255), 2)

	# compute the Euclidean distance between the midpoints
        dA = dist.euclidean((tltrX, tltrY), (blbrX, blbrY))
        dB= dist.euclidean((tlblX, tlblY), (trbrX, trbrY))
        print(dA)
        print(dB)
	# if the pixels per metric has not been initialized, then compute it as the ratio of pixels to supplied metric (in this case, inches)
        if pixelsPerMetric is None:
            pixelsPerMetric = dA / width
        print(pixelsPerMetric)
        cv2.putText(orig, "{:.2f}".format(dA/pixelsPerMetric),
		(int(tltrX - 15), int(tltrY - 10)), cv2.FONT_HERSHEY_SIMPLEX,
		0.65, (255, 255, 255), 2)
        cv2.putText(orig, "{:.2f}".format(dB/pixelsPerMetric),
		(int(trbrX + 10), int(trbrY)), cv2.FONT_HERSHEY_SIMPLEX,
		0.65, (255, 255, 255), 2)
        
    else:
        M = cv2.moments(c)
        cX1 = int((M["m10"] / M["m00"]))
        cY1= int((M["m01"] / M["m00"]))
        if dist.euclidean((cX, cY), (cX1, cY1))<1:
            cX=cX1
            cY=cY1
            continue
        print(approx)
        for i in range(1, len(approx)):
            print((dist.euclidean(approx[i-1], approx[i]))/pixelsPerMetric)
            #print(approx[i-1])
            #print(approx[i])
            tlblX, tlblY = approx[i-1][0][0], approx[i-1][0][1]
            tlblX1, tlblY1 = approx[i][0][0], approx[i][0][1]
            print(tlblX, tlblY)
            print(tlblX1, tlblY1)
            print('Mid point is' )
            print((tlblX+tlblX1)/2, (tlblY+tlblY1)/2)
            x=int((tlblX+tlblX1)/2) - 15
            y=int((tlblY+tlblY1)/2) - 10
            
            cv2.putText(orig, "{:.2f}".format((dist.euclidean(approx[i-1], approx[i]))/pixelsPerMetric),
		(x, y), cv2.FONT_HERSHEY_SIMPLEX, 
        0.65, (255, 255, 255), 2)
            
        print((dist.euclidean(approx[0], approx[-1]))/pixelsPerMetric)
        tlblX, tlblY = approx[0][0][0], approx[0][0][1]
        tlblX1, tlblY1 = approx[-1][0][1], approx[-1][0][1]
        print('Mid point is' )
        print((tlblX+tlblX1)/2, (tlblY+tlblY1)/2)
        x=int((tlblX+tlblX1)/2) - 15
        y=int((tlblY+tlblY1)/2) - 10    
        
        cv2.putText(orig, "{:.2f}".format((dist.euclidean(approx[0], approx[-1]))/pixelsPerMetric),
		(x, y), cv2.FONT_HERSHEY_SIMPLEX, 
		0.65, (255, 255, 255), 2)
        print("Hey")
        
    cv2.drawContours(orig, [c], -1, (0, 255, 0), 2)
    
    M = cv2.moments(c)
    cX = int((M["m10"] / M["m00"]))
    cY = int((M["m01"] / M["m00"]))
    #cv2.putText(image, count, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    count=count+1
    viewImage(orig)