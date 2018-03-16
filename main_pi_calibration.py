from target_recognition_pi import TargetRecognition

if __name__ == '__main__':

    def offest_received(x, z):
        print('Target detected with centroid: {}, {}'.format(x, z))

    target_recognition = TargetRecognition()
    target_recognition.register_callback(offest_received)
    target_recognition.start()