from __future__ import annotations

import argparse
import curses
import random
import time

from typing import Optional
from typing import Sequence

DEFAULT_TEXT = "Your custom text here"
DEFAULT_SPEED = 4
SPEED = [0.01, 0.025, 0.03, 0.04, 0.05, 0.07, 0.08, 0.09, 0.15, 0.3]


def set_curses_color() -> None:
    curses.init_pair(1, random.randrange(0, curses.COLORS), 16)


def curses_main(screen: curses._CursesWindow, args: argparse.Namespace):
    curses.curs_set(0)  # Set the cursor to off.
    screen.timeout(0)  # Turn blocking off for screen.getch().
    curses.use_default_colors()
    set_curses_color()
    delay = SPEED[args.speed]

    size_y, size_x = screen.getmaxyx()
    x = text_end = size_x - 1
    y = random.randint(0, size_y - 2)
    text_start = 0

    run = True
    while run:
        time.sleep(delay)
        size_y, size_x = screen.getmaxyx()  # screen resizing
        if y >= size_y - 1 or x >= size_x - 1:
            x = text_end = size_x - 1
            y = random.randint(0, size_y - 2)
            text_start = 0
            screen.clear()

        if x >= 1:
            x -= 1
        else:
            x = 0
            text_start += 1
        text_end -= 1
        screen.addstr(y, x,
                      args.text[text_start:size_x - text_end],
                      curses.color_pair(1))
        screen.clrtoeol()  # removes the last letter
        screen.refresh()
        if text_start >= len(args.text) + 5:  # done with current line?
            x = text_end = size_x - 1
            y = random.randint(0, size_y - 1)
            text_start = 0
            set_curses_color()

        ch = screen.getch()
        if ch != -1 and args.screensaver:
            run = False
        elif ch in [81, 113]:  # q, Q
            run = False
        elif 48 <= ch <= 57:  # 0 to 9
            delay = SPEED[int(chr(ch))]


def positive_int_zero_to_nine(value: str) -> int:
    """
    Used with argparse.
    Checks to see if value is positive int between 0 and 10.
    """
    try:
        int_value = int(value)
        if int_value < 0 or int_value >= 10:
            raise argparse.ArgumentTypeError(f"{value} is an invalid positive "
                                             f"int value 0 to 9")
        return int_value
    except ValueError:
        raise argparse.ArgumentTypeError(f"{value} is an invalid positive int "
                                         f"value 0 to 9")


def argument_parser(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("text", default=DEFAULT_TEXT, nargs="?",
                        help="Custom text string wrapped in quotes")
    parser.add_argument("-s", "--speed",
                        type=positive_int_zero_to_nine,
                        default=DEFAULT_SPEED,
                        help=f"Set scrolling speed 0 to 9.  (0-Fast, "
                             f"{DEFAULT_SPEED}-Default, 9-Slow)")

    parser.add_argument("--screensaver", action="store_true",
                        help="Screensaver mode. Any key will exit")

    return parser.parse_args(argv)


def main():
    args = argument_parser()
    try:
        curses.wrapper(curses_main, args)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
