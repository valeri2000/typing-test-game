import json
import os

from config import PLAYER_STATS_FILE


class Player:
    """Class for player
    """

    def __init__(self):
        """Constructor for Player class
        """

        self._stats_file_name = PLAYER_STATS_FILE
        self._player_stats = self._load_player_stats(PLAYER_STATS_FILE)

    def _clear_player_stats(self) -> dict:
        """Method which clears player previously save statistics

        Returns:
            dict: cleared player data as dictionary
        """

        return {
            'name': '',
            'number_of_races': 0,
            'average_wpm': 0.0,
            'last_ten_races': [0] * 10
        }

    def _load_player_stats(self, stats_file_name: str) -> dict:
        """Method which loads player statistics from file

        Args:
            stats_file_name (str): file name where the data is saved

        Returns:
            dict: the player data as dictionary which will be created if file is not valid
        """

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
        """Public method for getting the player name

        Returns:
            str: player name as string
        """

        return self._player_stats['name']

    def is_new_player(self) -> bool:
        """Public method which checks if the player is valid (file for stats did exist)

        Returns:
            bool: true if player is not registered
        """

        return len(self._player_stats['name']) == 0

    def set_name(self, name: str) -> None:
        """Public method for settings player name

        Args:
            name (str): new name of the player
        """

        self._player_stats['name'] = name

    def total_number_of_races(self) -> int:
        """Public method for getting total number of races of a player

        Returns:
            int: number of total races
        """

        return self._player_stats['number_of_races']

    def average_wpm(self) -> float:
        """Public method for getting average words per minute for a player of all their races

        Returns:
            float: the expected average words per minute
        """

        return self._player_stats['average_wpm']

    def last_ten_races(self) -> list:
        """Public method for getting the last ten WPM results of a player

        Returns:
            list: sequence of the last ten game results 
        """
        return self._player_stats['last_ten_races']

    def add_result(self, result_as_wpm: int) -> None:
        """Method for handling new result for a plyer

        Args:
            result_as_wpm (int): new results in words per minute format
        """

        self._player_stats['last_ten_races'].pop(0)
        self._player_stats['last_ten_races'].append(result_as_wpm)
        sum_wpm = self._player_stats['average_wpm'] * \
            self._player_stats['number_of_races'] + result_as_wpm
        self._player_stats['number_of_races'] += 1
        self._player_stats['average_wpm'] = sum_wpm / \
            (self._player_stats['number_of_races'])

    def save_player_stats(self) -> None:
        """Public method for saving player stats to a file
        """

        dir_path = os.path.dirname(os.path.realpath(__file__))
        with open(dir_path+'/../'+self._stats_file_name, 'w') as file:
            json.dump(self._player_stats, file)

    def clear_player_stats(self):
        """Public method for clearing player stats which calls private on
        """

        self._player_stats = self._clear_player_stats()
