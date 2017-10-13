import numpy as np
import argparse

from collections import defaultdict
from scipy import ndimage
import cv2
from operator import itemgetter
from typing import List, Tuple

from image_processing import centroid_handler
from image_processing.contour import Contour
from image_processing.hierarchy_tree import Tree
from image_processing.generic import Generic

# load the image
from image_processing.proportion_handler import ProportionHandler

image = cv2.imread('landing_field_2.jpg')


class ImageProcessing:

    def __init__(self):
        self.min_max_contours = Generic(min=3, max=9)
        self.grey_scale_image = None
        self.grey_blur_image = None
        self.black_white_image = None
        self.edged_image = None
        self.processed_image = None

    def process_image(self, image):
        # convert the image to grayscale, blur it
        self.grey_scale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        self.grey_blur_image = cv2.bilateralFilter(self.grey_scale_image, 11, 17, 17)
        ret, self.black_white_image = cv2.threshold(self.grey_blur_image, 150, 255, cv2.THRESH_BINARY)

        # find contours
        self.edged_image = cv2.Canny(self.black_white_image, 30, 200)
        # get all contours which are nested into each other. hierarchy  [Next, Previous, First_Child, Parent]
        (im2, contours, hierarchy) = cv2.findContours(self.edged_image.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = [Contour(contour) for contour in contours]
        possible_contours = self.get_possible_contours(contours, hierarchy)

        proportion_handler = ProportionHandler(4)
        for contours in possible_contours:
            satisfy = proportion_handler.does_contours_satisfy_proportions(contours)
            if satisfy:
                # calc and draw point
                center = ndimage.measurements.center_of_mass(np.array(contour.center for contour in contours))
                self.processed_image = image.copy()
                cv2.Circle(self.processed_image, center, 3, (0, 255, 0), thickness=1, lineType=8, shift=0)

                for c in contours:
                    cv2.drawContours(self.processed_image, [c], -1, (0, 255, 0), 3)

                return True, center

        return False, None

    def check_for_for_corners(self):
        # approximate the contour
        #peri = cv2.arcLength(contour, True)
        #approx = cv2.approxPolyDP(contour, 0.02 * peri, True)

        # if our approximated contour has four points
        #if len(approx) == 4:
        pass

    def get_possible_contours(self, cntrs, hierarchy):
        tree = Tree(hierarchy)
        possible_contours = []
        for leave in tree.leaves:
            parents, has_more = leave.get_n_parents(self.min_max_contours.max)
            if len(parents) >= self.min_max_contours.min: # check if there are enough contours in each other
                possible_contours.append([cntrs[parent.index] for parent in parents])

                # check if there are more contours in each other
                cur_leave = leave
                while has_more:
                    cur_leave = cur_leave.parent
                    parents, has_more = cur_leave.get_n_parents(self.min_max_contours.max)
                    possible_contours.append([cntrs[parent.index] for parent in parents])

        return possible_contours


 # while True:
 #     ret, roi_image = cap.read()
 #     #roi_image = cv2.imread("test_images/landing_field_2.jpg")
 #
 #
 #
 #     # find contours in the edged image, keep only the largest
 #     # ones, and initialize our screen contour
 #
 #     #centers = get_centers(cnts)
 #     #get_n_closest_centers(centers, 4)
 #
 #     cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:10]
 #     screenCnt = None
 #
 #     # loop over our contours
 #     for c in cnts:
 #
 #     gray = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)
 #     if screenCnt is not None:
 #         #cv2.drawContours(roi_image, [screenCnt], -1, (0, 255, 0), 3)
 #         for c in cnts:
 #             cv2.drawContours(gray, [c], -1, (0, 255, 0), 3)
 #     cv2.imshow("Game Boy Screen", gray)
 #     cv2.waitKey(1)
