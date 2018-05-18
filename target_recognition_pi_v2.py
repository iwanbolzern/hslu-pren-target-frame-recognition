# import the necessary packages
from datetime import datetime
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from multiprocessing import Queue, Array
from threading import Event
from typing import Callable

import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera

from utils import ringbuffer
from image_processing.image_processing import ImageProcessing


class TargetRecognition:

    def __init__(self):
        self.centroid_callback = []
        self.run_pool = ThreadPoolExecutor()
        self.run_future = None
        self.stop_interrupt = None
        self.camera = None

        self.image_processing = ImageProcessing()

        # process pool
        self.process_pool = ProcessPoolExecutor()

        # queues
        self.current_image = Array('i', range(307200))
        self.binary_queue_out = Array('i', range(307200))

    def init_camera(self):
        # initialize the camera and grab a reference to the raw camera capture
        self.camera = PiCamera()
        self.camera.resolution = (640, 480)
        self.camera.framerate = 20
        self.camera.color_effects = (128, 128)
        self.rawCapture = PiRGBArray(self.camera, size=(640, 480))

        # allow the camera to warmup
        time.sleep(0.1)

    def start(self):
        if not self.run_future:
            self.stop_interrupt = Event()
            self.run_future = self.run_pool.submit(self.run)
            self.run_future.add_done_callback(lambda future: print(future.result()))

    def __run_capture_process(self):
        self.init_camera()
        # capture frames from the camera
        for frame in self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True):
            # grab the raw NumPy array representing the image, then initialize the timestamp
            # and occupied/unoccupied text
            with self.current_image.get_lock():
                for i in range(len(frame.array)):
                    self.current_image[i] = frame.array[i]

            # clear the stream in preparation for the next frame
            self.rawCapture.truncate(0)

            if self.stop_interrupt.is_set():
                break

    def __run_binary_process(self):
        while not self.stop_interrupt.is_set():
            array = np.frombuffer(self.current_image).reshape((16, 16, 16))
            
            image = self.image_processing.to_binary_img(array)
            with self.binary_queue_out.get_lock():
                for i in range(len(image)):
                    self.binary_queue_out[i] = image[i]

    def run(self):
        future = self.process_pool.submit(self.__run_capture_thread)
        future.add_done_callback(self.__close_camera)

        future = self.process_pool.submit(self.__run_binary_process)
        future.add_done_callback(lambda future: print(future.result()))

        # capture frames from the camera
        while not self.stop_interrupt.is_set():
            array = []
            for i in range(len(self.binary_queue_out)):
                array.append(self.binary_queue_out[i])
            success, centroid = self.image_processing.process_image(array)
            print('{} Image processed {} {}'.format(datetime.now(), success, centroid))
            if success:
                for callback in self.centroid_callback:
                    callback(480 - centroid[1], centroid[0])  # Because camera is other way around

    def __close_camera(self, future):
        print(future.result())
        try:
            self.camera.close()
        except Exception as ex:
            pass

    def stop(self):
        self.stop_interrupt.set()
        self.run_future = None

    def register_callback(self, callback: Callable[[int, int], None]):
        self.centroid_callback.append(callback)

    def unregister_callback(self, callback: Callable[[int, int], None]):
        self.centroid_callback.remove(callback)

if __name__ == '__main__':
    targetRec = TargetRecognition()
    targetRec.start()