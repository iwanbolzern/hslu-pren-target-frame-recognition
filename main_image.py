
import cv2

# load the image
image = cv2.imread('landing_field_2.jpg')



while True:
    ret, roi_image = cap.read()
    #roi_image = cv2.imread("test_images/landing_field_2.jpg")

    # convert the image to grayscale, blur it, and find edges
    # in the image
    gray = cv2.cvtColor(roi_image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 11, 17, 17)
    ret, gray = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    edged = cv2.Canny(gray, 30, 200)

    # find contours in the edged image, keep only the largest
    # ones, and initialize our screen contour
    (im2, cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
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
