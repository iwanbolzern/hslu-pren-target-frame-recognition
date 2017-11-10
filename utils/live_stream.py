import socket
from threading import Thread

import pickle
import struct

class LiveStream:

    def __init__(self):
        self.server_socket = None
        self.listen_thread = None
        self.is_listening = False
        self.clients = []

    def start(self, ip_address: str='', port: int=5005):
        self.stop()

        # start listen
        self.is_listening = True
        self.listen_thread = Thread(target=self._listen, args=(ip_address, port))
        self.listen_thread.start()

    def send_frame(self, image):
        data = pickle.dumps(image)
        for client in self.clients:
            client.sendall(struct.pack("L", len(data)) + data)

    def stop(self):
        if self.listen_thread:
            self.is_listening = False
            self.listen_thread.join()
            self.listen_thread = None
            self.server_socket = None

    def _listen(self, ip_address: str, port: int):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.settimeout(10)
        self.server_socket.bind((ip_address, port))
        self.server_socket.listen(5)  # defines max connect requests

        while self.is_listening:
            try:
                conn, address = self.server_socket.accept()
                self.clients.append(conn)
                print("Client {} connected to live stream\n".format(address))
            except Exception as ex:
                if ex.args and ex.args[0] == 'timed out':
                    pass # ignore time out exception
                else:
                    raise ex


