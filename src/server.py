import socket
import pickle
from time import sleep, time
from threading import Thread, Lock
from config import SERVER_PORT
from utils import generate_fixed_length_text


class Server:
    def __init__(self):
        self._socket = socket.socket()
        self._socket.bind(('', SERVER_PORT))
        self._socket.listen()
        self._clients_lock = Lock()
        self._results_lock = Lock()
        self._clients = []
        self._results = []

    def _client_manager(self, c):
        accept = '1'
        with self._clients_lock:
            if len(self._clients) == 2:
                accept = '0'
        c.send(accept.encode())
        if accept == '0':
            c.close()
            return
        player_name = c.recv(1024).decode()
        with self._clients_lock:
            self._clients.append((c, player_name))
        with self._clients_lock:
            if len(self._clients) == 2:
                txt = generate_fixed_length_text(10)
                data = pickle.dumps(txt)
                for (c, _) in self._clients:
                    c.send(data)
                sleep(2)
                for (c, name) in self._clients:
                    if name != self._clients[0][1]:
                        c.send(self._clients[0][1].encode())
                    else:
                        c.send(self._clients[1][1].encode())
                sleep(2)
                for (c, _) in self._clients:
                    c.send(b'start')
        msg = c.recv(1024).decode()  # block
        if not msg:
            print('Client dead!')
            with self._clients_lock:
                self._clients.remove((c, player_name))
        else:
            print('Got from client ' + str(msg))
            msg = str(time())
            with self._results_lock:
                self._results.append((player_name, msg))
        with self._results_lock:
            if len(self._results) == 2:
                # result[0][0] < results[0][1]
                with self._clients_lock:
                    flag = self._clients[0][1] == self._results[0][0]
                    self._clients[0][0].send(str(int(flag)).encode())
                    self._clients[1][0].send(str(int(flag ^ 1)).encode())
                self._results.clear()
                with self._clients_lock:
                    self._clients.clear()

    def start(self):
        while True:
            c, addr = self._socket.accept()
            print('Connected to: ' + addr[0] + ':' + str(addr[1]))
            t = Thread(target=self._client_manager, args=(c, ))
            t.start()


server = Server()
server.start()
