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
        self._data_lock2 = Lock()
        self._clients = []
        self._results = []

    def _multi_threaded_client(self, c):
        accept = True
        with self._data_lock:
            if len(self._clients) == 2:
                accept = False
        c.send(str(int(accept)).encode())
        if not accept:
            c.close()
            return
        player_name = c.recv(1024).decode()
        self._clients.append((c, player_name))
        if len(self._clients) == 2:
            txt = generate_fixed_length_text(30)
            data = pickle.dumps(txt)
            with self._data_lock:
                for (c, _) in self._clients:
                    c.send(data)
            sleep(2)
            with self._data_lock:
                for (c, name) in self._clients:
                    if name != self._clients[0][1]:
                        c.send(self._clients[0][1].encode())
                    else:
                        c.send(self._clients[1][1].encode())
            sleep(2)
            with self._data_lock:
                for (c, _) in self._clients:
                    c.send(b'start')
        msg = c.recv(1024).decode()  # this BLOCKS
        if not msg:
            print('Client dead!')
            with self._data_lock:
                self._clients.remove((c, player_name))
        else:
            print('Got from client ' + str(msg))
            with self._data_lock2:
                self._results.append((player_name, msg))
        with self._data_lock2:
            if len(self._results) == 2:
                if float(self._results[0][1]) > float(self._results[1][1]):
                    with self._data_lock:
                        if self._clients[0][1] == self._results[0][0]:
                            self._clients[0][0].send(b'0')
                            self._clients[1][0].send(b'1')
                        else:
                            self._clients[0][0].send(b'1')
                            self._clients[1][0].send(b'0')
                else:
                    with self._data_lock:
                        if self._clients[0][1] == self._results[0][0]:
                            self._clients[0][0].send(b'1')
                            self._clients[1][0].send(b'0')
                        else:
                            self._clients[0][0].send(b'0')
                            self._clients[1][0].send(b'1')
                self._results.clear()
                with self._data_lock:
                    self._clients.clear()

    def start(self):
        while True:
            c, address = self._socket.accept()
            print('Connected to: ' + address[0] + ':' + str(address[1]))
            t = Thread(target=self._multi_threaded_client, args=(c, ))
            t.start()


server = Server()
server.start()
