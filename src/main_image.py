import cv2

from src.image_processing import ImageProcessing

# load the image
image = cv2.imread('test_images/landing_field_grayscale.jpg')

image_processing = ImageProcessing()
image_processing.process_image(image)
image_processing.show_all_images()
cv2.waitKey(0)


