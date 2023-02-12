"""File for Screen class
"""

import curses
import curses.panel
import time
from client import Client
from game import Game
from utils import text_with_fixed_column_size, total_characters_in_text
from constants import ESCAPE_ORD_CODE, BACKSPACE_ORD_CODE_1, BACKSPACE_ORD_CODE_2, ENTER_ORD_CODE
from constants import CURSES_BOX_LINES, CURSES_BOX_COLS, CURSES_BOX_BEGIN_Y, CURSES_BOX_BEGIN_X


class Screen:
    """Class for the screen responsible for drawing the game and handling keys
    """

    def __init__(self):
        """Constructor for Screen class
        """

        self._game = Game()
        self._screen = curses.initscr()
        self._client = None
        curses.cbreak()
        curses.noecho()
        curses.start_color()
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        # self._screen.border(0)
        self._screen.nodelay(True)
        curses.curs_set(False)

    def start(self):
        """The only public method which loads the game
        """

        if self._game.player.is_new_player():
            self._register_window()
        else:
            self._game.new_text()
            self._start_window()
        self._game.player.save_player_stats()

    def _register_window(self):
        """Register window shown when local storage file is unavailable
        """

        new_name = ''
        should_exit = False
        while True:
            box1 = self._screen.subwin(CURSES_BOX_LINES + 2, CURSES_BOX_COLS + 2,
                                       CURSES_BOX_BEGIN_Y - 1, CURSES_BOX_BEGIN_X - 1)
            box2 = self._screen.subwin(CURSES_BOX_LINES, CURSES_BOX_COLS,
                                       CURSES_BOX_BEGIN_Y, CURSES_BOX_BEGIN_X)
            box1.box()
            box2.clear()
            box2.addstr('This looks like first time launch.\n')
            box2.addstr(
                'Enter your name here and press <ENTER>: ' + str(new_name))
            self._screen.refresh()
            time.sleep(0.01)
            char = self._screen.getch()
            if char == ESCAPE_ORD_CODE:  # escape code
                should_exit = True
                break
            if (char in (BACKSPACE_ORD_CODE_1, BACKSPACE_ORD_CODE_2)) and len(new_name) > 0:
                new_name = new_name[:-1]
            if char == ENTER_ORD_CODE and len(new_name) > 0:
                break
            if (ord('a') <= char <= ord('z')) or (ord('A') <= char <= ord('Z')):
                new_name += chr(char)
        if not should_exit:
            self._game.player.set_name(new_name)
            self._start_window()
        curses.endwin()

    def _start_window(self):
        """Start window which shows the main menu of the game
        """

        player_name = self._game.player.name()
        while True:
            box1 = self._screen.subwin(CURSES_BOX_LINES + 2, CURSES_BOX_COLS + 2,
                                       CURSES_BOX_BEGIN_Y - 1, CURSES_BOX_BEGIN_X - 1)
            box2 = self._screen.subwin(CURSES_BOX_LINES, CURSES_BOX_COLS,
                                       CURSES_BOX_BEGIN_Y, CURSES_BOX_BEGIN_X)
            box1.box()
            box2.clear()
            box2.addstr('Hello, ' + str(player_name) + '!\n\n')
            box2.addstr('> New singleplayer game (press s)\n')
            box2.addstr('> New multiplayer game (press m)\n')
            box2.addstr('> Show statistics (press t)\n')
            box2.addstr('> Settings (press o)\n')
            box2.addstr('> Clear ALL player info (press c)\n')
            box2.addstr('> Exit (press e)\n')
            box2.addstr('\nIn order to go back from a menu, press ESC')
            self._screen.refresh()
            time.sleep(0.01)
            char = self._screen.getch()
            if char == ord('s'):
                self._game_window(0)
                break
            if char == ord('m'):
                self._multi_player_window()
                break
            if char == ord('t'):
                self._stats_window()
            if char == ord('o'):
                self._settings_window()
            if char == ord('c'):
                self._game.player.clear_player_stats()
                exit(0)
            if char == ord('e'):
                break

        curses.endwin()

    def _game_end_window(self, time_taken_secs: int, mistakes: int,
                         num_words: int, num_symbols: int, is_multi: bool):
        """Game end window shown when player finishes their text

        Args:
            time_taken_secs (int): time taken for the whole text
            mistakes (int): number of wrongly typed symbols
            num_words (int): number of words in the text
            num_symbols (int): number of symbols in the text
            is_multi (bool): is the game multiplayer one
        """

        wpm = num_words / time_taken_secs * 60
        if is_multi:
            self._client.send_msg(str(int(wpm)))
        self._game.player.add_result(int(wpm))
        self._game.player.save_player_stats()
        multi_result, opponent_wpm = -1, 0
        while True:
            box1 = self._screen.subwin(CURSES_BOX_LINES + 2, CURSES_BOX_COLS + 2,
                                       CURSES_BOX_BEGIN_Y - 1, CURSES_BOX_BEGIN_X - 1)
            box2 = self._screen.subwin(CURSES_BOX_LINES, CURSES_BOX_COLS,
                                       CURSES_BOX_BEGIN_Y, CURSES_BOX_BEGIN_X)
            box1.box()
            box2.clear()
            box2.addstr('Text finished in ' +
                        str(time_taken_secs) + ' seconds!\n')
            box2.addstr('WPM: ' + "{:.2f}".format(wpm) + '\n')
            box2.addstr('Mistakes: ' + str(mistakes) + '\n')
            box2.addstr(
                'Accuracy: ' + "{:.2f}".format(
                    (num_symbols - mistakes) / num_symbols * 100) + '%\n')
            if is_multi:
                if multi_result == -1:
                    box2.addstr('Waiting for the other player to finish ..\n')
                    msg = self._client.receive_msg_no_block()
                    if len(msg) > 0:
                        msg = msg.split(',')
                        multi_result = int(msg[0])
                        opponent_wpm = int(msg[1])
                elif multi_result == 1:
                    box2.addstr('You won! Opponent wpm: ' +
                                str(opponent_wpm) + '\n')
                else:
                    box2.addstr('You lost! Opponent wpm: ' +
                                str(opponent_wpm) + '\n')
            box2.addstr('\n\nIn order to go back, press ESC')
            self._screen.refresh()
            time.sleep(0.01)
            char = self._screen.getch()
            if char == ESCAPE_ORD_CODE:  # escape code
                break

        curses.endwin()
        self._game.new_text()
        self._start_window()

    def _multi_player_window(self):
        """Multi player window which handles the event of choosing multiplayer mode
        """

        self._client = Client()
        if self._client.join_lobby(self._game.player.name()):
            if not self._multi_player_lobby():
                self._client.close_socket()
                self._start_window()
                return
            self._multi_player_countdown()
            if self._client.receive_msg() == 'start':
                self._game_window(1)
        else:
            self._multi_player_wait()
            self._start_window()

    def _game_window(self, is_multi: bool):
        """Main game window which shows the text and tracks the player input

        Args:
            is_multi (bool): is current game multiplayer one
        """

        transformed_text = text_with_fixed_column_size(self._game.text(), 76)
        track_time, start_time, end_time = False, 0, 0
        if is_multi:
            track_time = True
            start_time = int(time.time())
        curr_pos_row, curr_pos_col = 0, 0
        last_char_wrong = False
        mistakes = 0
        while True:
            box1 = self._screen.subwin(CURSES_BOX_LINES + 2, CURSES_BOX_COLS + 2,
                                       CURSES_BOX_BEGIN_Y - 1, CURSES_BOX_BEGIN_X - 1)
            box2 = self._screen.subwin(CURSES_BOX_LINES, CURSES_BOX_COLS,
                                       CURSES_BOX_BEGIN_Y, CURSES_BOX_BEGIN_X)
            box1.box()
            if curr_pos_row == 0 and curr_pos_col == 0:
                box2.clear()
            box2.addstr(
                'Press the first symbol of first word to begin test!\n')
            if track_time:
                box2.addstr('Passed time: ' +
                            str(int(time.time()) - start_time) + ' secs\n\n')
            else:
                box2.addstr('Passed time: 0 secs\n\n')
            for row in range(len(transformed_text)):
                if row < curr_pos_row:
                    box2.addstr(transformed_text[row], curses.color_pair(1))
                elif row == curr_pos_row:
                    if last_char_wrong:
                        box2.addstr(
                            transformed_text[row][:curr_pos_col - 1],
                            curses.color_pair(1) | curses.A_UNDERLINE)
                        box2.addstr(
                            str(transformed_text[row][curr_pos_col - 1]),
                            curses.color_pair(2) | curses.A_UNDERLINE)
                        box2.addstr(transformed_text[row][curr_pos_col:])
                    else:
                        box2.addstr(
                            transformed_text[row][:curr_pos_col],
                            curses.color_pair(1) | curses.A_UNDERLINE)
                        box2.addstr(transformed_text[row][curr_pos_col:])
                else:
                    box2.addstr(transformed_text[row])
                box2.addstr('\n')
            self._screen.refresh()
            time.sleep(0.01)
            char = self._screen.getch()
            if char == ESCAPE_ORD_CODE:  # escape code
                break
            if char in (BACKSPACE_ORD_CODE_1, BACKSPACE_ORD_CODE_2):  # backspace
                if curr_pos_row == 0 and curr_pos_col == 0:
                    continue
                if curr_pos_col == 0:
                    curr_pos_row -= 1
                    curr_pos_col = len(transformed_text[curr_pos_row]) - 1
                else:
                    curr_pos_col -= 1
                last_char_wrong = False
            if (ord('a') <= char <= ord('z')) or char == ord(' '):
                if not track_time:
                    track_time = True
                    start_time = int(time.time())
                if last_char_wrong:
                    continue
                if char != ord(transformed_text[curr_pos_row][curr_pos_col]):
                    last_char_wrong = True
                    mistakes += 1
                curr_pos_col += 1
                if curr_pos_col == len(transformed_text[curr_pos_row]):
                    curr_pos_row += 1
                    curr_pos_col = 0
                if curr_pos_row == len(transformed_text) and not last_char_wrong:
                    end_time = int(time.time())
                    self._game_end_window(end_time - start_time, mistakes, len(
                        self._game.text()), total_characters_in_text(transformed_text), is_multi)
                    break

        curses.endwin()
        self._game.new_text()
        self._start_window()

    def _stats_window(self):
        """Window which shows player statistics from previous runs
        """

        while True:
            box1 = self._screen.subwin(CURSES_BOX_LINES + 2, CURSES_BOX_COLS + 2,
                                       CURSES_BOX_BEGIN_Y - 1, CURSES_BOX_BEGIN_X - 1)
            box2 = self._screen.subwin(CURSES_BOX_LINES, CURSES_BOX_COLS,
                                       CURSES_BOX_BEGIN_Y, CURSES_BOX_BEGIN_X)
            box1.box()
            box2.clear()
            box2.addstr('Player name: ' + self._game.player.name() + '\n')
            box2.addstr('Average WPM: ' +
                        "{:.2f}".format(self._game.player.average_wpm()) + '\n')
            box2.addstr('Total texts completed: ' +
                        str(self._game.player.total_number_of_races()) + '\n')
            box2.addstr('Last ten results: ' +
                        str(self._game.player.last_ten_races()) + '\n')
            box2.addstr('\n\nIn order to go back, press ESC')
            self._screen.refresh()
            time.sleep(0.01)
            char = self._screen.getch()
            if char == ESCAPE_ORD_CODE:  # escape code
                break

        curses.endwin()

    def _settings_window(self):
        """Window which presents some settings to the player regarding the game
        """

        while True:
            box1 = self._screen.subwin(CURSES_BOX_LINES + 2, CURSES_BOX_COLS + 2,
                                       CURSES_BOX_BEGIN_Y - 1, CURSES_BOX_BEGIN_X - 1)
            box2 = self._screen.subwin(CURSES_BOX_LINES, CURSES_BOX_COLS,
                                       CURSES_BOX_BEGIN_Y, CURSES_BOX_BEGIN_X)
            box1.box()
            box2.clear()
            box2.addstr('Update the number of words in a text:\n')
            box2.addstr('\t> 10 (press 1)\n')
            box2.addstr('\t> 30 (press 2)\n')
            box2.addstr('\t> 60 (press 3)\n')
            box2.addstr('\t> 100 (press 4)\n')
            box2.addstr('\n\nIn order to go back, press ESC')
            self._screen.refresh()
            time.sleep(0.01)
            char = self._screen.getch()
            if char == ESCAPE_ORD_CODE:  # escape code
                break
            if char == ord('1'):
                self._game.update_text_length(10)
                break
            if char == ord('2'):
                self._game.update_text_length(30)
                break
            if char == ord('3'):
                self._game.update_text_length(60)
                break
            if char == ord('4'):
                self._game.update_text_length(100)
                break

        self._game.new_text()
        curses.endwin()

    def _multi_player_countdown(self):
        """Window when multiplayer match is to begin with timer
        """

        time_left = 10
        init = False
        opponent_name = ''
        while True:
            box1 = self._screen.subwin(CURSES_BOX_LINES + 2, CURSES_BOX_COLS + 2,
                                       CURSES_BOX_BEGIN_Y - 1, CURSES_BOX_BEGIN_X - 1)
            box2 = self._screen.subwin(CURSES_BOX_LINES, CURSES_BOX_COLS,
                                       CURSES_BOX_BEGIN_Y, CURSES_BOX_BEGIN_X)
            box1.box()
            box2.clear()
            box2.addstr('Race will begin in ' +
                        str(time_left) + ' seconds!\n')
            if len(opponent_name) > 0:
                box2.addstr('Opponent is ' + opponent_name + '\n')
            self._screen.refresh()
            time.sleep(1)
            if not init:
                opponent_name = self._client.receive_msg()
                init = True
            time_left -= 1
            if time_left == 0:
                break
        curses.endwin()

    def _multi_player_wait(self):
        """Window shown when server is busy (2 players are already in a match)
        """

        while True:
            box1 = self._screen.subwin(CURSES_BOX_LINES + 2, CURSES_BOX_COLS + 2,
                                       CURSES_BOX_BEGIN_Y - 1, CURSES_BOX_BEGIN_X - 1)
            box2 = self._screen.subwin(CURSES_BOX_LINES, CURSES_BOX_COLS,
                                       CURSES_BOX_BEGIN_Y, CURSES_BOX_BEGIN_X)
            box1.box()
            box2.clear()
            box2.addstr(
                'There is currently an active game or server is unavailable.\nPlease try again later.\n')
            self._screen.refresh()
            time.sleep(0.01)
            char = self._screen.getch()
            if char == ESCAPE_ORD_CODE:  # escape code
                break

        curses.endwin()

    def _multi_player_lobby(self) -> bool:
        """Window shown when player selects multiplayer mode and waits for other player to join

        Returns:
            bool: true, if another player is found and game is to be played
        """

        game_on = False
        while True:
            box1 = self._screen.subwin(CURSES_BOX_LINES + 2, CURSES_BOX_COLS + 2,
                                       CURSES_BOX_BEGIN_Y - 1, CURSES_BOX_BEGIN_X - 1)
            box2 = self._screen.subwin(CURSES_BOX_LINES, CURSES_BOX_COLS,
                                       CURSES_BOX_BEGIN_Y, CURSES_BOX_BEGIN_X)
            box1.box()
            box2.clear()
            box2.addstr(
                'Waiting for another player to join.')
            self._screen.refresh()
            time.sleep(1)
            txt = self._client.receive_text()
            if len(txt) != 0:
                self._game.set_text(txt)
                game_on = True
                break
            char = self._screen.getch()
            if char == ESCAPE_ORD_CODE:  # escape code
                break

        curses.endwin()
        return game_on
