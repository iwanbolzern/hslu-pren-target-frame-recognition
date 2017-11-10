import pickle
import socket
import struct
from threading import Thread


class LiveStreamClient:

    def __init__(self):
        self.client_socket = None
        self.receive_thread = None
        self.image_callbacks = []

    def connect(self, ip_address: str, port: int):
        self.receive_thread = Thread(target=self._receive, args=(ip_address, port))
        self.receive_thread.start()

    def stop(self):
        self.receive_thread.stop()

    def _receive(self, ip_address: str, port: int):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((ip_address, port))

        data = b''
        payload_size = struct.calcsize("L")

        while True:
            while len(data) < payload_size:
                data += self.client_socket.recv(4096)

            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("L", packed_msg_size)[0]
            while len(data) < msg_size:
                data += self.client_socket.recv(4096)
            frame_data = data[:msg_size]
            data = data[msg_size:]

            frame = pickle.loads(frame_data)
            self._send_frame_callback(frame)

    def _send_frame_callback(self, frame):
        for callback in self.image_callbacks:
            callback(frame)

    def register_image_callback(self, callback):
        self.image_callbacks.append(callback)

