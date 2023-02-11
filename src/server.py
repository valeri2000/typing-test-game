import socket
import pickle
from time import sleep
from threading import Thread, Lock
from config import SERVER_PORT
from utils import generate_fixed_length_text


class Server:
    def __init__(self):
        self._socket = socket.socket()
        self._socket.bind(('', SERVER_PORT))
        self._socket.listen()
        self._data_lock = Lock()
        self._clients = []

    def _multi_threaded_client(self, c):
        accept = True
        with self._data_lock:
            if len(self._clients) == 2:
                accept = False
            else:
                self._clients.append(c)
        c.send(str(int(accept)).encode())
        if not accept:
            c.close()
        else:
            if len(self._clients) == 2:
                txt = generate_fixed_length_text(10)
                data = pickle.dumps(txt)
                for c in self._clients:
                    c.send(data)
                sleep(10)
                with self._data_lock:
                    for c in self._clients:
                        c.send(b'start')
            while True:
                msg = c.recv(1024).decode()  # this BLOCKS
                if not msg:
                    print('Client dead!')
                    with self._data_lock:
                        self._clients.remove(c)
                    break
                else:
                    print('Got from client ' + str(msg))

    def start(self):
        while True:
            c, address = self._socket.accept()
            print('Connected to: ' + address[0] + ':' + str(address[1]))
            t = Thread(target=self._multi_threaded_client, args=(c, ))
            t.start()


hey = Server()
hey.start()
