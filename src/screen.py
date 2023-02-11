import curses
import curses.panel
import time
from game import Game
from utils import text_with_fixed_column_size


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

    def _single_player_window(self):
        transformed_text = text_with_fixed_column_size(self._game.text(), 78)
        while True:
            box1 = self._screen.subwin(20, 80, 6, 50)
            box2 = self._screen.subwin(18, 78, 7, 51)
            box1.box()
            for row in range(len(transformed_text)):
                box2.addstr(transformed_text[row] + '\n')
            self._screen.refresh()
            time.sleep(0.01)
            char = self._screen.getch()
            if char == 27:  # escape code
                break

        curses.endwin()

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
