import sys
from datetime import datetime

from src.target_recognition import TargetRecognition

if __name__ == '__main__':

    def offest_received(x, z):
        print('{}: Target detected with centroid: {}, {}'.format(datetime.now(), x, z))
        sys.stdout.flush()


    target_recognition = TargetRecognition()
    target_recognition.register_callback(offest_received)
    target_recognition.start()

    input()