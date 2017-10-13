import cv2

from image_processing.image_processing import ImageProcessing

# load the image
image = cv2.imread('test_images/landing_field_2.jpg')

image_processing = ImageProcessing()
image_processing.process_image(image)
cv2.imshow("Processed Image", image_processing.processed_image)
cv2.waitKey(1)


