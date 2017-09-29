# import the necessary packages
import numpy as np
import argparse
import cv2

# load the image
# image = cv2.imread('landing_field_2.jpg')


cap = cv2.VideoCapture(0)  # Webcam Capture
#cap = cv2.VideoCapture("test_movies/high_res_slow.MOV")

while True:
    ret, roi_image = cap.read()
    #roi_image = cv2.imread("test_images/landing_field_2.jpg")

    # convert the image to grayscale, blur it, and find edges
    # in the image
    gray = cv2.cvtColor(roi_image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 11, 17, 17)
    ret, gray = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
    edged = cv2.Canny(gray, 30, 200)

    # find contours in the edged image, keep only the largest
    # ones, and initialize our screen contour
    (im2, cnts, hierarchy) = cv2.findContours(
        edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:10]

    edged = cv2.cvtColor(edged, cv2.COLOR_GRAY2RGB)

    # loop over our contours
    for c in cnts:
        # approximate the contour
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)

        if len(approx) >= 4 and len(approx) <= 6:
            # bounding box
            (x, y, w, h) = cv2.boundingRect(approx)
            ratio = w / float(h)

            # solidity
            area = cv2.contourArea(c)
            hullArea = cv2.contourArea(cv2.convexHull(c))
            solidity = area / float(hullArea)

            # filter
            keepDims = w > 25 and h > 25
            keepSolidity = solidity > 0.9
            keepAspectRatio = ratio >= 0.8 and ratio <= 1.2

            if keepDims and keepSolidity and keepAspectRatio:
                cv2.drawContours(roi_image, [approx], -1, (0, 0, 255), 4)
                cv2.drawContours(edged, [approx], -1, (0, 0, 255), 4)

                M = cv2.moments(approx)
                (cX, cY) = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

                cv2.circle(roi_image, (cX, cY), 2, (255, 0, 0), 2)
                cv2.circle(edged, (cX, cY), 2, (255, 0, 0), 2)

    cv2.imshow("Main Screen", roi_image)
    cv2.imshow("Edged", edged)
    cv2.imshow("Gray", gray)
    cv2.waitKey(1)
