from imutils import contours

def sort(cnts):
    (cnts,_)=contours.sort_contours(cnts)
    return cnts
