import socket
import pickle
from config import SERVER_ADDRESS, SERVER_PORT


class Client:
    def __init__(self):
        self._socket = socket.socket()

    def join_lobby(self) -> bool:
        self._socket.connect((SERVER_ADDRESS, SERVER_PORT))
        res = self._socket.recv(1).decode()
        return res == '1'

    def receive_text(self) -> list:
        txt = []
        received_data = self._socket.recv(1024)
        if received_data:
            txt = pickle.loads(received_data)
        return txt

    def receive_msg(self) -> str:
        received_data = self._socket.recv(1024).decode()
        return str(received_data)

    def send_msg(self, msg: str):
        self._socket.send(msg.encode())
