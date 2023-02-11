import socket
from config import SERVER_ADDRESS, SERVER_PORT


class Client:
    def __init__(self):
        self._socket = socket.socket()

    def join_lobby(self) -> bool:
        self._socket.connect((SERVER_ADDRESS, SERVER_PORT))
        res = self._socket.recv(1).decode()
        return res


hey = Client()
hey.join_lobby()
