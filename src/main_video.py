import cv2

from src.image_processing import ImageProcessing

#cap = cv2.VideoCapture("test_movies/high_res_slow.MOV")  # Webcam Capture
cap = cv2.VideoCapture("test_movies/pi_dark.h264")  # Webcam Capture

image_processing = ImageProcessing()

while True:
    ret, image = cap.read()

    image_processing.process_image(image)
    image_processing.show_all_images()
    cv2.waitKey(1)

