"""File for Server class
"""

import socket
import pickle
from time import sleep
from threading import Thread, Lock
from config import SERVER_PORT
from utils import generate_fixed_length_text


class Server:
    """Class for the server responsible for managing multiplayer games
    """

    def __init__(self):
        """Constructor for Server class
        """

        self._socket = socket.socket()
        self._socket.bind(('', SERVER_PORT))
        self._socket.listen()
        self._clients_lock = Lock()
        self._results_lock = Lock()
        self._clients = []
        self._results = []

    def _client_manager(self, sock: socket.socket):
        """Method which is run in new threads for managing multiple clients

        Args:
            c (socket.socket): socket for single client
        """

        accept = '1'
        with self._clients_lock:
            if len(self._clients) == 2:
                accept = '0'
        sock.send(accept.encode())
        if accept == '0':
            sock.close()
            return
        player_name = sock.recv(1024).decode()
        with self._clients_lock:
            self._clients.append((sock, player_name))
        with self._clients_lock:
            if len(self._clients) == 2:
                txt = generate_fixed_length_text(10)
                data = pickle.dumps(txt)
                for (curr_sock, _) in self._clients:
                    curr_sock.send(data)
                sleep(2)
                for (curr_sock, name) in self._clients:
                    if name != self._clients[0][1]:
                        curr_sock.send(self._clients[0][1].encode())
                    else:
                        curr_sock.send(self._clients[1][1].encode())
                sleep(2)
                for (curr_sock, _) in self._clients:
                    curr_sock.send(b'start')
        msg = sock.recv(1024).decode()  # block
        if not msg:
            print('Client dead!')
            with self._clients_lock:
                self._clients.remove((sock, player_name))
        else:
            print('Got from client ' + str(msg))
            wpm = int(msg)
            with self._results_lock:
                self._results.append((player_name, wpm))
        with self._results_lock:
            if len(self._results) == 2:
                with self._clients_lock:
                    if self._clients[0][1] == self._results[0][0]:
                        self._clients[0][0].send(
                            ('1,'+str(self._results[1][1])).encode())
                        self._clients[1][0].send(
                            ('0,'+str(self._results[0][1])).encode())
                    else:
                        self._clients[0][0].send(
                            ('0,'+str(self._results[0][1])).encode())
                        self._clients[1][0].send(
                            ('1,'+str(self._results[1][1])).encode())

                self._results.clear()
                with self._clients_lock:
                    self._clients.clear()

    def start(self):
        """Main public method which executes server logic
        """

        while True:
            sock, addr = self._socket.accept()
            print('Connected to: ' + addr[0] + ':' + str(addr[1]))
            thread = Thread(target=self._client_manager, args=(sock, ))
            thread.start()


server = Server()
server.start()
