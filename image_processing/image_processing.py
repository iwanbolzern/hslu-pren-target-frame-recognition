import numpy as np
import argparse

from collections import defaultdict
from sklearn.neighbors import NearestNeighbors
import cv2
from operator import itemgetter
from typing import List, Tuple

# load the image
image = cv2.imread('landing_field_2.jpg')


class ImageProcessing:

    def __init__(self):
        self.grey_scale_image = None
        self.grey_blur_image = None
        self.black_white_image = None
        self.edged_image = None

    def process_image(self, image):
        # convert the image to grayscale, blur it
        self.grey_scale_image = cv2.cvtColor(roi_image, cv2.COLOR_BGR2GRAY)
        self.grey_blur_image = cv2.bilateralFilter(self.grey_scale_image, 11, 17, 17)
        self.black_white_image = cv2.threshold(self.grey_blur_image, 150, 255, cv2.THRESH_BINARY)

        # find contours
        self.edged_image = cv2.Canny(self.black_white_image, 30, 200)
        # hierarchy  [Next, Previous, First_Child, Parent]
        (im2, cnts, hierarchy) = cv2.findContours(self.edged_image.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


    def get_possible_contours(self, cntrs, hierarchy):
        # return everyting between 3 and 6 contours in each other
        pass



while True:
    ret, roi_image = cap.read()
    #roi_image = cv2.imread("test_images/landing_field_2.jpg")



    # find contours in the edged image, keep only the largest
    # ones, and initialize our screen contour

    #centers = get_centers(cnts)
    #get_n_closest_centers(centers, 4)

    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:10]
    screenCnt = None

    # loop over our contours
    for c in cnts:
        # approximate the contour
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)

        # if our approximated contour has four points, then
        # we can assume that we have found our screen
        if len(approx) == 4:
            screenCnt = approx
            break
    gray = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)
    if screenCnt is not None:
        #cv2.drawContours(roi_image, [screenCnt], -1, (0, 255, 0), 3)
        for c in cnts:
            cv2.drawContours(gray, [c], -1, (0, 255, 0), 3)
    cv2.imshow("Game Boy Screen", gray)
    cv2.waitKey(1)
