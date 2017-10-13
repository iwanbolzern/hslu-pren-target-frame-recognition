# import the necessary packages
import numpy as np
import argparse

from collections import defaultdict
from sklearn.neighbors import NearestNeighbors
import cv2
from operator import itemgetter
from typing import List, Tuple

from image_processing.image_processing import ImageProcessing

cap = cv2.VideoCapture("test_movies/high_res_slow.MOV")  # Webcam Capture

while True:
    ret, image = cap.read()

    image_processing = ImageProcessing()
    image_processing.process_image(image)
    image_processing.show_all_images()
    cv2.waitKey(1)

