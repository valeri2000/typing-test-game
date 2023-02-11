import curses
import curses.panel
import time
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
            box2.addstr('Clear ALL player info (press c)\n')
            box2.addstr('Exit (press e)\n')
            self._screen.refresh()
            time.sleep(0.01)
            char = self._screen.getch()
            if char == ord('s'):
                self._single_player_window()
                break
            elif char == ord('m'):
                break
            elif char == ord('t'):
                self._stats_window()
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
            box2.addstr('WPM: ' + str(wpm) + '\n')
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

    def _single_player_window(self):
        transformed_text = text_with_fixed_column_size(self._game.text(), 76)
        track_time, start_time, end_time = False, 0, 0
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
                    self._game_end_window(end_time - start_time, mistakes, len(
                        self._game.text()), total_characters_in_text(transformed_text))
                    break

        curses.endwin()
        self._game.new_text()
        self._start_window()

    def _stats_window(self):
        while True:
            box1 = self._screen.subwin(20, 80, 6, 50)
            box2 = self._screen.subwin(18, 78, 7, 51)
            box1.box()
            box2.clear()
            box2.addstr('TODO')
            self._screen.refresh()
            time.sleep(0.01)
            char = self._screen.getch()
            if char == 27:  # escape code
                break

        curses.endwin()
