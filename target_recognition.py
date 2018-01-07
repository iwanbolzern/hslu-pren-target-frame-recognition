# import the necessary packages
import time
import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera

from image_processing.image_processing import ImageProcessing


class TargetRecognition:

    def __init__(self):
        # initialize the camera and grab a reference to the raw camera capture
        self.camera = PiCamera()
        self.camera.resolution = (640, 480)
        self.camera.framerate = 32
        self.camera.color_effects = (128, 128)
        self.rawCapture = PiRGBArray(self.camera, size=(640, 480))

        # allow the camera to warmup
        time.sleep(0.1)

        self.image_processing = ImageProcessing()


    def start(self):
        # capture frames from the camera
        for frame in self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True):
            # grab the raw NumPy array representing the image, then initialize the timestamp
            # and occupied/unoccupied text
            image = frame.array

            success, centroid = self.image_processing.process_image(image)

            # clear the stream in preparation for the next frame
            rawCapture.truncate(0)

    def register_callback(self, callback):
