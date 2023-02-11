from player import Player
from utils import generate_fixed_length_text


class Game:
    def __init__(self, text_length=10):
        self._text = generate_fixed_length_text(text_length)
        self._text_length = text_length
        self.player = Player()

    def text(self) -> list:
        return self._text

    def new_text(self):
        self._text = generate_fixed_length_text(self._text_length)

    def update_text_length(self, text_length: int):
        self._text_length = text_length
