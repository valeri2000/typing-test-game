from player import Player
from utils import generate_fixed_length_text


class Game:
    def __init__(self, text_length=60):
        self._text = generate_fixed_length_text(text_length)
        self.player = Player()

    def text(self) -> list:
        return self._text

    def save_player(self) -> None:
        self.player.save_player_stats()
