import socket
import pickle
from config import SERVER_ADDRESS, SERVER_PORT


class Client:
    """Client class which handles communication with server in multiplayer mode
    """

    def __init__(self):
        """Constructor for Client class
        """

        self._socket = socket.socket()

    def join_lobby(self, player_name: str) -> bool:
        """Method which is called when player selects multiplayer mode game

        Args:
            player_name (str): name of current player

        Returns:
            bool: true if player has joined multiplayer game successfully
        """

        try:
            self._socket.connect((SERVER_ADDRESS, SERVER_PORT))
            res = self._socket.recv(1).decode()
        except:
            res = '0'
        if res == '1':
            self.send_msg(player_name)
        return res == '1'

    def receive_text(self) -> list:
        """Method which gets the active multiplayer game text for both players

        Returns:
            list: sequence of the words in the text
        """

        txt = []
        try:
            received_data = self._socket.recv(1024, socket.MSG_DONTWAIT)
            if received_data:
                txt = pickle.loads(received_data)
        except:
            pass
        return txt

    def receive_msg(self) -> str:
        """Method which receives message from the server

        Returns:
            str: the received message as string
        """

        received_data = self._socket.recv(1024).decode()
        return str(received_data)

    def receive_msg_no_block(self) -> str:
        """Method which receives message from the server (returns immediately)

        Returns:
            str: the received message as string
        """

        received_data = ''
        try:
            received_data = self._socket.recv(
                1024, socket.MSG_DONTWAIT).decode()
        except:
            pass
        return str(received_data)

    def send_msg(self, msg: str) -> bool:
        """Method which sends message to the server

        Args:
            msg (str): the message as string

        Returns:
            bool: true if message is sent successfully
        """

        success = True
        try:
            bytes = self._socket.send(msg.encode())
            if bytes == 0:
                success = False
        except:
            success = False
        return success
