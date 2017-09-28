#7 DEC 2015
#This program uses multi-scale template matching to find an object in a video stream.
#The object is the "template" which is an image file (JPG, PNG, etc.)
#The video stream is from the raspberry pi camera module.
#This program works on the Raspberry PI 2, Jessie, OpenCV 3.0.0

import cv2
import numpy as np  # for template matching

from utils import imutils

cap = cv2.VideoCapture(0)  # Webcam Capture

template = cv2.imread('landing_field.jpg')                                        #I used a photo of sunglasses, cropped down to just the sunglasses and nothing else
(template_height, template_width) = template.shape[:2]
template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)                           #gray it
template = cv2.GaussianBlur     (template, (7,7), 0)                            #blur it
template = cv2.Canny(template, 50, 150)                                         #edge it
cv2.imshow("template", template)                                                #show it (not necessary, but I like to see what I'm working with

while True:
    ret, roi_image = cap.read()
    image_gray          = cv2.cvtColor(roi_image, cv2.COLOR_BGR2GRAY)           #change the image to grayscale
    (h, w)              = image_gray.shape[:2]
    center              = (w/2,h/2)
    im_gblurred         = cv2.GaussianBlur(image_gray, (7,7), 0)        #blur the image

    ### MULTI-SCALE TEMPLATE MATCHING
    ms_image = im_gblurred                              #this line is not required, but I was playing around with different multiscale image transformations
    found = None                                        #flag to keep track of the matched region

    #scan each scale of the image
    #ending value (20%), starting value (100%), number of slices in between (20)
    for scale in np.linspace(0.2, 1.0, 20)[::-1]:
        #resize the image according to the scale and keep track of the ratio of the resizing
        resized = imutils.resize(ms_image, width = int(ms_image.shape[1] * scale))
        r       = ms_image.shape[1] / float(resized.shape[1])

        #if the resized image is smaller than the template then break from the loop
        if resized.shape[0] < template_height or resized.shape[1] < template_width:
            break
        #detect the edges in the resized grayscale image and apply template matching to find the template in the image
        edged = cv2.Canny(resized, 50, 150)                     #must use the SAME parameters here as you did for the tempate ABOVE for best results

        #input image:   must be 8bit or 32bit-floating point
        #tempate image: must not be larger than the image to search, and same data type
        #method:        parameter specifying the comparison methods (SQDIFF, SQDIFFNORM, CCORR, CCORRNORM, CCOEFF, CCOEFFNORM)
        #mask:          mask of searched template.  must be same data type and size as template. It not set by default.
        #result:        map of comparison results, must be single channel 32bit float
        result = cv2.matchTemplate(edged, template, cv2.TM_CCOEFF)              #this is where the magic happens!
        #The cv2.minMaxLoc function takes the correlation result and returns a 4-tuple
        #that includes the minimum correlation value, the maximum correlation value,
        #the (x, y)-coordinate of the minimum value, and the (x, y)-coordinate of the
        #maximum value, respectively. We are only interested in the maximum value and
        #(x, y)-coordinate so we keep the maximums and discard the minimums.
        (_, maxVal, _, maxLoc)  = cv2.minMaxLoc(result)

        #if we found a new maximum correlation value, then update the bookkeeping variable
        if found is None or maxVal > found[0]:
            found = (maxVal, maxLoc, r)
        #unpack the bookkeeping variable and compute the (x, y) coordinates of the bounding box based on the resized ratio
        (_, maxLoc, r) = found
        (startX, startY) = (int(maxLoc[0] * r), int(maxLoc[1] * r))
        (endX, endY) = (int((maxLoc[0] + template_width) * r), int((maxLoc[1] + template_height) * r))

            #draw a box around the detected result and display the image
        cv2.rectangle(ms_image, (startX, startY), (endX, endY), (0, 0, 255), 2)
        cv2.imshow("Image", ms_image)
                             #Must use this to eliminate the error: "Incorrect buffer length"
        if cv2.waitKey(1) & 0xFF == ord('q'):       #press CTRL and Q to stop the program from running
            break

# When everything is done, release the capture
cap.release()
cv2.destroyAllWindows()