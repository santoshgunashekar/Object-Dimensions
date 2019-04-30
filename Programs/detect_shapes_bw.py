import numpy
import skimage.filters.rank
import skimage.morphology
import skimage.io
import cv2
# convert image to a uint8 image which only has 0, 128 and 255 values
# the source png image provided has other levels in it so it needs to be thresholded - adjust the thresholding method for your data
img_raw = skimage.io.imread('test_1.png', as_grey=True)
img = numpy.zeros_like(img_raw, dtype=numpy.uint8)
img[:,:] = 128
img[ img_raw < 0.25 ] = 0
img[ img_raw > 0.75 ] = 255

# define "next to" - this may be a square, diamond, etc
selem = skimage.morphology.disk(1)

# create masks for the two kinds of edges
black_gray_edges = (skimage.filters.rank.minimum(img, selem) == 0) & (skimage.filters.rank.maximum(img, selem) == 128)
gray_white_edges = (skimage.filters.rank.minimum(img, selem) == 128) & (skimage.filters.rank.maximum(img, selem) == 255)

# create a color image
img_result = numpy.dstack( [img,img,img] )

# assign colors to edge masks
img_result[ black_gray_edges, : ] = numpy.asarray( [ 0, 255, 0 ] )
img_result[ gray_white_edges, : ] = numpy.asarray( [ 255, 0, 0 ] )

cv2.imwrite('out.png',img_result)