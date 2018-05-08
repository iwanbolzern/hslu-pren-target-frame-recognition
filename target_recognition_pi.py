# import the necessary packages
from datetime import datetime
import time
from concurrent.futures import ThreadPoolExecutor
from threading import Event
from typing import Callable

from picamera.array import PiRGBArray
from picamera import PiCamera

from image_processing.image_processing import ImageProcessing


class TargetRecognition:

    def __init__(self):
        self.centroid_callback = []
        self.run_pool = ThreadPoolExecutor()
        self.run_future = None
        self.stop_interrupt = None
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
        if not self.run_future:
            self.stop_interrupt = Event()
            self.run_future = self.run_pool.submit(self.run)

    def run(self):
        # capture frames from the camera
        for frame in self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True):
            # grab the raw NumPy array representing the image, then initialize the timestamp
            # and occupied/unoccupied text
            image = frame.array

            success, centroid = self.image_processing.process_image(image)
            print('{} Image processed {} {}'.format(datetime.now(), success, centroid))
            if success:
                map(lambda cb: cb(centroid[0], centroid[1]), self.centroid_callback)

            # clear the stream in preparation for the next frame
            self.rawCapture.truncate(0)

            if self.stop_interrupt.is_set():
                break

    def stop(self):
        self.stop_interrupt.set()
        self.run_future.result()
        self.run_future = None

    def register_callback(self, callback: Callable[[int, int], None]):
        self.centroid_callback.append(callback)

    def unregister_callback(self, callback: Callable[[int, int], None]):
        self.centroid_callback.remove(callback)
