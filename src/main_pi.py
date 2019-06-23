import time

import cv2
from picamera import PiCamera
from picamera.array import PiRGBArray

from src.image_processing import ImageProcessing

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
camera.color_effects = (128, 128)
rawCapture = PiRGBArray(camera, size=(640, 480))

# allow the camera to warmup
time.sleep(0.1)

image_processing = ImageProcessing()

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
    image = frame.array

    image_processing.process_image(image)
    image_processing.show_all_images()
    cv2.waitKey(1)

    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)