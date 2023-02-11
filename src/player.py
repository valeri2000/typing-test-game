import json
import os

from config import PLAYER_STATS_FILE


class Player:
    def __init__(self):
        self._stats_file_name = PLAYER_STATS_FILE
        self._player_stats = self._load_player_stats(PLAYER_STATS_FILE)

    def _clear_player_stats(self) -> dict:
        return {
            'name': '',
            'number_of_races': 0,
            'average_wpm': 0.0,
            'last_ten_races': [0] * 10
        }

    def _load_player_stats(self, stats_file_name: str) -> dict:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        try:
            with open(dir_path+'/../'+stats_file_name, 'r') as file:
                player_stats = json.load(file)

            if 'name' not in player_stats or 'average_wpm' not in player_stats or \
                    'last_ten_races' not in player_stats or 'number_of_races' not in player_stats:
                raise ValueError
        except (FileNotFoundError, ValueError):
            player_stats = self._clear_player_stats()
            with open(dir_path+'/../'+stats_file_name, 'w+') as file:
                json.dump(player_stats, file)

        return player_stats

    def name(self) -> str:
        return self._player_stats['name']

    def is_new_player(self) -> bool:
        return len(self._player_stats['name']) == 0

    def set_name(self, name: str) -> None:
        self._player_stats['name'] = name

    def total_number_of_races(self) -> int:
        return self._player_stats['number_of_races']

    def average_wpm(self) -> float:
        return self._player_stats['average_wpm']

    def last_ten_races(self) -> list:
        return self._player_stats['last_ten_races']

    def add_result(self, result_as_wpm: int) -> None:
        self._player_stats['last_ten_races'].pop(0)
        self._player_stats['last_ten_races'].append(result_as_wpm)
        sum_wpm = self._player_stats['average_wpm'] * \
            self._player_stats['number_of_races'] + result_as_wpm
        self._player_stats['number_of_races'] += 1
        self._player_stats['average_wpm'] = sum_wpm / \
            (self._player_stats['number_of_races'])

    def save_player_stats(self) -> None:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        with open(dir_path+'/../'+self._stats_file_name, 'w') as file:
            json.dump(self._player_stats, file)

    def clear_player_stats(self):
        self._player_stats = self._clear_player_stats()
