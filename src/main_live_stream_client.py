import time

import cv2

from src.utils.live_stream_client import LiveStreamClient


def show_image(frame):
    cv2.imshow('frame', frame)
    cv2.waitKey(1)


liveStream = LiveStreamClient()
liveStream.register_image_callback(show_image)
liveStream.connect('127.0.0.1', 5005)

time.sleep(30) # time to start the other processes
while True:
    text = input("Write e or exit to close")
    if text == "e" or text == "exit":
        break