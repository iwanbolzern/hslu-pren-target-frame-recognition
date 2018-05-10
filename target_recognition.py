# import the necessary packages
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from threading import Event
from typing import Callable

import cv2

from image_processing.image_processing import ImageProcessing


class TargetRecognition:

    def __init__(self):
        self.centroid_callback = []
        self.run_pool = ThreadPoolExecutor()
        self.run_future = None
        self.stop_interrupt = None

        # init camera
        self.rawCapture = cv2.VideoCapture(0)  # Webcam Capture

        # allow the camera to warmup
        time.sleep(0.1)

        self.image_processing = ImageProcessing()

    def start(self):
        if not self.run_future:
            self.stop_interrupt = Event()
            self.run_future = self.run_pool.submit(self.run)
            self.run_future.add_done_callback(lambda future: print(future.result()))

    def run(self):
        # capture frames from the camera
        while True:
            ret, image = self.rawCapture.read()

            print('Image process started')
            success, centroid = self.image_processing.process_image(image)
            print('{} Image processed {} {}'.format(datetime.now(), success, centroid))
            if success:
                for callback in self.centroid_callback:
                    callback(centroid[0], centroid[1])

            # clear the stream in preparation for the next frame
            # self.rawCapture.truncate(0)

            if self.stop_interrupt.is_set():
                break

    def stop(self):
        self.stop_interrupt.set()
        self.run_future = None

    def register_callback(self, callback: Callable[[int, int], None]):
        self.centroid_callback.append(callback)

    def unregister_callback(self, callback: Callable[[int, int], None]):
        self.centroid_callback.remove(callback)


if __name__ == '__main__':
    t_rec = TargetRecognition()

    def callback(x, y):
        t_rec.unregister_callback(callback)
        t_rec.stop()

    t_rec.start()
