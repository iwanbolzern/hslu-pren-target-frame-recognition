# import the necessary packages
import numpy as np
import argparse
import cv2

# load the image
image = cv2.imread('landing_field_2.jpg')
imgray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
ret,thresh = cv2.threshold(imgray,127,255,0)

# find the contours in the mask
(im2, cnts, _) = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
print("I found %d black shapes" % (len(cnts)))
#cv2.imshow("Mask", shapeMask)

# loop over the contours
for c in cnts:
    # draw the contour and show it
    cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
    cv2.imshow("Image", image)

cv2.waitKey(0)