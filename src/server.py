import socket
from threading import Thread, Lock
from config import SERVER_PORT


class Server:
    def __init__(self):
        self._socket = socket.socket()
        self._socket.bind(('', SERVER_PORT))
        self._socket.listen()
        self._data_lock = Lock()
        self._count_clients = 0

    def _multi_threaded_client(self, c):
        accept = True
        with self._data_lock:
            if self._count_clients == 2:
                accept = False
            else:
                self._count_clients += 1
        c.send(str(int(accept)).encode())
        if not accept:
            c.close()

    def start(self):
        while True:
            c, address = self._socket.accept()
            print('Connected to: ' + address[0] + ':' + str(address[1]))
            t = Thread(target=self._multi_threaded_client, args=(c, ))
            t.start()


hey = Server()
hey.start()
