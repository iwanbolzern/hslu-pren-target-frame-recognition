# import the necessary packages
from datetime import datetime
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from multiprocessing import Queue
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
        self.camera = None

        self.init_camera()

        self.image_processing = ImageProcessing()

        # process pool
        self.process_pool = ProcessPoolExecutor()

        # queues
        self.current_image = None

    def init_camera(self):
        # initialize the camera and grab a reference to the raw camera capture
        self.camera = PiCamera()
        self.camera.resolution = (400, 400)
        self.camera.framerate = 20
        self.camera.color_effects = (128, 128)
        self.rawCapture = PiRGBArray(self.camera, size=(640, 480))

        # allow the camera to warmup
        time.sleep(0.1)

    def start(self):
        if not self.run_future:
            self.stop_interrupt = Event()
            future = self.run_pool.submit(self.__run_capture_thread)
            future.add_done_callback(self.__close_camera)

            self.run_future = self.run_pool.submit(self.run)
            self.run_future.add_done_callback(lambda future: print(future.result()))

    def __run_capture_thread(self):
        # capture frames from the camera
        for frame in self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True):
            # grab the raw NumPy array representing the image, then initialize the timestamp
            # and occupied/unoccupied text
            self.current_image = frame.array

            # clear the stream in preparation for the next frame
            self.rawCapture.truncate(0)

            print('Image captured')

            if self.stop_interrupt.is_set():
                break

    def run(self):
        # wait for image
        while self.current_image is None:
            time.sleep(0.001)

        # capture frames from the camera
        while not self.stop_interrupt.is_set():
            success, centroid = self.image_processing.process_image(self.current_image)
            print('{} Image processed {} {}'.format(datetime.now(), success, centroid))
            if success:
                for callback in self.centroid_callback:
                    callback(centroid[1], centroid[0])  # Because camera is other way around

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
