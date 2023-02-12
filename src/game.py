"""File for the Game class
"""

from player import Player
from utils import generate_fixed_length_text
from constants import DEFAULT_SINGLE_PLAYER_WORDS


class Game:
    """Class for the game consisting of the player and the text
    """

    def __init__(self, text_length=DEFAULT_SINGLE_PLAYER_WORDS):
        """Constructor for Game class

        Args:
            text_length: number of words for the game text. Defaults to DEFAULT_SINGLE_PLAYER_WORDS.
        """

        self._text = generate_fixed_length_text(text_length)
        self._text_length = text_length
        self.player = Player()

    def text(self) -> list:
        """Public method for getting the text

        Returns:
            list: sequence of the words in the text
        """

        return self._text

    def new_text(self):
        """Public method for generating new text
        """

        self._text = generate_fixed_length_text(self._text_length)

    def set_text(self, text: list):
        """Public method for setting text

        Args:
            text (list): the new sequence of words for the text
        """

        self._text = text

    def update_text_length(self, text_length: int):
        """Public method which updates text length. It doesn't generate new text!

        Args:
            text_length (int): new number of words for generating texts
        """

        self._text_length = text_length
