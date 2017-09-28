# import the necessary packages
import numpy as np
import argparse
import cv2

# load the image
# image = cv2.imread('landing_field_2.jpg')


cap = cv2.VideoCapture(0)  # Webcam Capture

while True:
    ret, roi_image = cap.read()
    imgray = cv2.cvtColor(roi_image, cv2.COLOR_BGR2GRAY)
    bil_filter = cv2.bilateralFilter(imgray, 11, 17, 17)
    ret, thresh = cv2.threshold(imgray, 240, 255, cv2.THRESH_BINARY)

    cv2.imshow("Image", thresh)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # press CTRL and Q to stop the program from running
        break

    # find the contours in the mask
    (im2, cnts, _) = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    print("I found %d black shapes" % (len(cnts)))
    #cv2.imshow("Mask", shapeMask)

    # loop over the contours
    for c in cnts:
        # draw the contour and show it
        cv2.drawContours(roi_image, [c], -1, (0, 255, 0), 2)
        #cv2.imshow("Image", roi_image)

        if cv2.waitKey(1) & 0xFF == ord('q'):       #press CTRL and Q to stop the program from running
            break