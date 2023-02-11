import curses
import curses.panel
import time
from client import Client
from game import Game
from utils import text_with_fixed_column_size, total_characters_in_text


class Screen:
    def __init__(self):
        self._game = Game()
        self._screen = curses.initscr()
        curses.cbreak()
        curses.noecho()
        curses.start_color()
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        self._screen.border(0)
        self._screen.nodelay(True)
        curses.curs_set(False)

    def start(self):
        if self._game.player.is_new_player():
            self._register_window()
        else:
            self._game.new_text()
            self._start_window()
        self._game.player.save_player_stats()

    def _register_window(self):
        new_name = ''
        exit = False
        while True:
            box1 = self._screen.subwin(20, 80, 6, 50)
            box2 = self._screen.subwin(18, 78, 7, 51)
            box1.box()
            box2.clear()
            box2.addstr('This looks like first time launch.\n')
            box2.addstr(
                'Enter your name here and press <ENTER>: ' + str(new_name))
            self._screen.refresh()
            time.sleep(0.01)
            char = self._screen.getch()
            if char == 27:  # escape code
                exit = True
                break
            elif (char == 8 or char == 127) and len(new_name) > 0:
                new_name = new_name[:-1]
            elif char == 10 and len(new_name) > 0:
                break
            elif (char >= ord('a') and char <= ord('z')) or (char >= ord('A') and char <= ord('Z')):
                new_name += chr(char)
        if not exit:
            self._game.player.set_name(new_name)
            self._start_window()
        curses.endwin()

    def _start_window(self):
        player_name = self._game.player.name()
        while True:
            box1 = self._screen.subwin(20, 80, 6, 50)
            box2 = self._screen.subwin(18, 78, 7, 51)
            box1.box()
            box2.addstr('Hello, ' + str(player_name) + '!\n\n')
            box2.addstr('New singleplayer game (press s)\n')
            box2.addstr('New multiplayer game (press m)\n')
            box2.addstr('Show statistics (press t)\n')
            box2.addstr('Settings (press o)\n')
            box2.addstr('Clear ALL player info (press c)\n')
            box2.addstr('Exit (press e)\n')
            box2.addstr('\n\nIn order to go back from a menu, press ESC')
            self._screen.refresh()
            time.sleep(0.01)
            char = self._screen.getch()
            if char == ord('s'):
                self._game_window(0)
                break
            elif char == ord('m'):
                self._multi_player_window()
                break
            elif char == ord('t'):
                self._stats_window()
            elif char == ord('o'):
                self._settings_window()
            elif char == ord('c'):
                self._game.player.clear_player_stats()
                break
            elif char == ord('e'):
                break

        curses.endwin()

    def _game_end_window(self, time_taken_secs: int, mistakes: int, num_words: int, num_symbols: int):
        wpm = num_words / time_taken_secs * 60
        self._game.player.add_result(int(wpm))
        self._game.player.save_player_stats()
        while True:
            box1 = self._screen.subwin(20, 80, 6, 50)
            box2 = self._screen.subwin(18, 78, 7, 51)
            box1.box()
            box2.clear()
            box2.addstr('Text finished in ' +
                        str(time_taken_secs) + ' seconds!\n')
            box2.addstr('WPM: ' + "{:.2f}".format(wpm) + '\n')
            box2.addstr('Mistakes: ' + str(mistakes) + '\n')
            box2.addstr(
                'Accuracy: ' + "{:.2f}".format((num_symbols - mistakes) / num_symbols * 100) + '%\n')
            self._screen.refresh()
            time.sleep(0.01)
            char = self._screen.getch()
            if char == 27:  # escape code
                break

        curses.endwin()
        self._game.new_text()
        self._start_window()

    def _multi_player_window(self):
        self._client = Client()
        if self._client.join_lobby():
            txt = self._client.receive_text()
            self._game.set_text(txt)
            self._multi_player_countdown()
            if self._client.receive_msg() == 'start':
                self._game_window(1)

    def _game_window(self, is_multi: bool):
        transformed_text = text_with_fixed_column_size(self._game.text(), 76)
        track_time, start_time, end_time = False, 0, 0
        if is_multi:
            track_time = True
            start_time = int(time.time())
        curr_pos_row, curr_pos_col = 0, 0
        last_char_wrong = False
        mistakes = 0
        while True:
            box1 = self._screen.subwin(20, 80, 6, 50)
            box2 = self._screen.subwin(18, 78, 7, 51)
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
                            transformed_text[row][:curr_pos_col - 1], curses.color_pair(1) | curses.A_UNDERLINE)
                        box2.addstr(
                            str(transformed_text[row][curr_pos_col - 1]), curses.color_pair(2) | curses.A_UNDERLINE)
                        box2.addstr(transformed_text[row][curr_pos_col:])
                    else:
                        box2.addstr(
                            transformed_text[row][:curr_pos_col], curses.color_pair(1) | curses.A_UNDERLINE)
                        box2.addstr(transformed_text[row][curr_pos_col:])
                else:
                    box2.addstr(transformed_text[row])
                box2.addstr('\n')
            self._screen.refresh()
            time.sleep(0.01)
            char = self._screen.getch()
            if char == 27:  # escape code
                break
            elif char == 8 or char == 127:  # backspace
                if curr_pos_row == 0 and curr_pos_col == 0:
                    continue
                if curr_pos_col == 0:
                    curr_pos_row -= 1
                    curr_pos_col = len(transformed_text[curr_pos_row]) - 1
                else:
                    curr_pos_col -= 1
                last_char_wrong = False
            elif (char >= ord('a') and char <= ord('z')) or char == ord(' '):
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
                    if is_multi:
                        self._client.send_msg(str(time.time()))
                        break
                    self._game_end_window(end_time - start_time, mistakes, len(
                        self._game.text()), total_characters_in_text(transformed_text))
                    break

        curses.endwin()
        self._game.new_text()
        if not is_multi:
            self._start_window()

    def _stats_window(self):
        while True:
            box1 = self._screen.subwin(20, 80, 6, 50)
            box2 = self._screen.subwin(18, 78, 7, 51)
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
            if char == 27:  # escape code
                break

        curses.endwin()

    def _settings_window(self):
        while True:
            box1 = self._screen.subwin(20, 80, 6, 50)
            box2 = self._screen.subwin(18, 78, 7, 51)
            box1.box()
            box2.clear()
            box2.addstr('Update the number of words in a text:\n')
            box2.addstr('\t10 (press 1)\n')
            box2.addstr('\t30 (press 2)\n')
            box2.addstr('\t60 (press 3)\n')
            box2.addstr('\t100 (press 4)\n')
            box2.addstr('\n\nIn order to go back, press ESC')
            self._screen.refresh()
            time.sleep(0.01)
            char = self._screen.getch()
            if char == 27:  # escape code
                break
            elif char == ord('1'):
                self._game.update_text_length(10)
                break
            elif char == ord('2'):
                self._game.update_text_length(30)
                break
            elif char == ord('3'):
                self._game.update_text_length(60)
                break
            elif char == ord('4'):
                self._game.update_text_length(100)
                break

        self._game.new_text()
        curses.endwin()

    def _multi_player_countdown(self):
        time_left = 10
        while True:
            box1 = self._screen.subwin(20, 80, 6, 50)
            box2 = self._screen.subwin(18, 78, 7, 51)
            box1.box()
            box2.clear()
            box2.addstr('Race will begin in ' + str(time_left) + ' seconds!')
            self._screen.refresh()
            time.sleep(1)
            time_left -= 1
            if time_left == 0:
                break
        curses.endwin()
