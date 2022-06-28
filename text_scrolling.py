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
CURSES_BLACK = 16
CURSES_COLOR = {"red": curses.COLOR_RED, "green": curses.COLOR_GREEN,
                "blue": curses.COLOR_BLUE, "yellow": curses.COLOR_YELLOW,
                "magenta": curses.COLOR_MAGENTA, "cyan": curses.COLOR_CYAN,
                "white": curses.COLOR_WHITE, "black": CURSES_BLACK}
COLORS = ["red", "green", "blue", "yellow", "magenta", "cyan", "white", "black"]


def set_curses_color(color: str, bg_color: str) -> None:
    curses.init_pair(1, CURSES_BLACK, CURSES_BLACK)
    if color == "random":
        curses.init_pair(2,
                         random.randrange(0, curses.COLORS),
                         CURSES_COLOR[bg_color])
    else:
        curses.init_pair(2, CURSES_COLOR[color], CURSES_COLOR[bg_color])


def curses_main(screen: curses._CursesWindow, args: argparse.Namespace):
    curses.curs_set(0)  # Set the cursor to off.
    screen.timeout(0)  # Turn blocking off for screen.getch().
    curses.use_default_colors()
    color = "random" if args.color is None else args.color
    text_bg_color = args.bg_text_color
    set_curses_color(color, text_bg_color)
    screen.bkgd(" ", curses.color_pair(1))
    delay = SPEED[args.speed]
    color_number = 0
    text_bg_color_number = 0

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
        attributes = curses.A_NORMAL
        if args.bold_text:
            attributes += curses.A_BOLD
        if args.italic_text:
            attributes += curses.A_ITALIC
        screen.addstr(y, x,
                      args.text[text_start:size_x - text_end],
                      curses.color_pair(2) + attributes)
        screen.clrtoeol()  # removes the last letter
        screen.refresh()
        if text_start >= len(args.text) + 5:  # done with current line?
            x = text_end = size_x - 1
            y = random.randint(0, size_y - 1)
            text_start = 0
            set_curses_color(color, text_bg_color)

        ch = screen.getch()
        if ch != -1 and args.screensaver:
            run = False
        elif ch in [81, 113]:  # q, Q
            run = False
        elif 48 <= ch <= 57:  # 0 to 9
            delay = SPEED[int(chr(ch))]
        elif ch == 99:  # c
            color = COLORS[color_number]
            set_curses_color(color, text_bg_color)
            color_number = 0 if color_number == 7 else color_number + 1
        elif ch == 114:  # r
            color = "random"
            set_curses_color(color, text_bg_color)
        elif ch == 67:  # C
            text_bg_color = COLORS[text_bg_color_number]
            set_curses_color(color, text_bg_color)
            if text_bg_color_number == 7:
                text_bg_color_number = 0
            else:
                text_bg_color_number += 1
        elif ch == 100:  # d
            args.bold_text = False
            args.italic_text = False
            delay = SPEED[DEFAULT_SPEED]
            color = "random"
            text_bg_color = "black"
            set_curses_color(color, text_bg_color)
        elif ch == 98:  # b
            args.bold_text = not args.bold_text
        elif ch == 105:  # i
            args.italic_text = not args.italic_text


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


def color_type(value: str) -> str:
    """
    Used with argparse
    Checks to see if the value is a valid color and returns
    the lower case color name.
    """
    lower_value = value.lower()
    if lower_value in CURSES_COLOR.keys():
        return lower_value
    raise argparse.ArgumentTypeError(f"{value} is an invalid color name")


def argument_parser(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("text", default=DEFAULT_TEXT, nargs="?",
                        help="Custom text string wrapped in quotes")
    parser.add_argument("-s", "--speed",
                        type=positive_int_zero_to_nine,
                        default=DEFAULT_SPEED,
                        help=f"Set scrolling speed 0 to 9.  (0-Fast, "
                             f"{DEFAULT_SPEED}-Default, 9-Slow)")
    parser.add_argument("-c", "--color", type=color_type,
                        help=f"Set solid color. Available solid color: "
                             f"{', '.join(COLORS)}")
    parser.add_argument("-C", "--bg_text_color", type=color_type,
                        metavar="COLOR",
                        default="black", help="Set text background color")
    parser.add_argument("-b", "--bold_text", action="store_true",
                        help="Bold text")
    parser.add_argument("-i", "--italic_text", action="store_true",
                        help="Italic text")

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
