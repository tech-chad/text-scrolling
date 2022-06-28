import curses
import os
from unittest import mock

import pytest

import text_scrolling


@pytest.mark.parametrize("argument, expected_result", [
    ([], 4), (["-s", "1"], 1), (["--speed", "9"], 9)
])
def test_argument_parser_speed(argument, expected_result):
    result = text_scrolling.argument_parser(argument)
    assert result.speed == expected_result


@pytest.mark.parametrize("argument, expected_result", [
    ([], "Your custom text here"), (["test string"], "test string")
])
def test_argument_parser_text(argument, expected_result):
    result = text_scrolling.argument_parser(argument)
    result.text = expected_result


@pytest.mark.parametrize("argument, expected_speed, expected_text", [
    ([], 4, "Your custom text here"),
    (["test string"], 4, "test string"),
    (["test string", "-s", "3"], 3, "test string"),
    (["--speed", "7"], 7, "Your custom text here"),
])
def test_argument_parser_text_speed(argument, expected_speed, expected_text):
    result = text_scrolling.argument_parser(argument)
    assert result.speed == expected_speed
    assert result.text == expected_text


@pytest.mark.parametrize("argument, expected_result", [
    ([], False), (["--screensaver"], True),
])
def test_argument_parser_screensaver(argument, expected_result):
    result = text_scrolling.argument_parser(argument)
    assert result.screensaver == expected_result


@pytest.mark.parametrize("argument, expected_result", [
    ([], None,), (["-c", "blue"], "blue"), (["--color", "red"], "red")
])
def test_argument_parser_color(argument, expected_result):
    result = text_scrolling.argument_parser(argument)
    assert result.color == expected_result


@pytest.mark.parametrize("argument, expected_result", [
    ([], "black"), (["-C", "green"], "green"),
    (["--bg_text_color", "blue"], "blue"),
])
def test_argument_parser(argument, expected_result):
    result = text_scrolling.argument_parser(argument)
    assert result.bg_text_color == expected_result


@pytest.mark.parametrize("argument, expected_result", [
    ([], False), (["-b"], True), (["--bold_text"], True),
])
def test_argument_parser_bold_text(argument, expected_result):
    result = text_scrolling.argument_parser(argument)
    assert result.bold_text == expected_result


@pytest.mark.parametrize("argument, expected_result", [
    ([], False), (["-i"], True), (["--italic_text"], True),
])
def test_argument_parser_italic_text(argument, expected_result):
    result = text_scrolling.argument_parser(argument)
    assert result.italic_text == expected_result


@pytest.mark.parametrize("argument, expected_result", [
    ([], False), (["-u"], True), (["--underline_text"], True),
])
def test_argument_parser_underline_text(argument, expected_result):
    result = text_scrolling.argument_parser(argument)
    assert result.underline_text == expected_result


@pytest.mark.parametrize("argument, expected_result", [
    ([], False), (["-f"], True), (["--flash_text"], True),
])
def test_argument_parser_flashing_text(argument, expected_result):
    result = text_scrolling.argument_parser(argument)
    assert result.flash_text == expected_result


@pytest.mark.parametrize("test_values, expected_results", [
    ("0", 0), ("1", 1), ("2", 2), ("3", 3), ("4", 4),
    ("5", 5), ("6", 6), ("7", 7), ("8", 8), ("9", 9)
])
def test_positive_int_zero_to_nine_normal(test_values, expected_results):
    result = text_scrolling.positive_int_zero_to_nine(test_values)
    assert result == expected_results


@pytest.mark.parametrize("test_values", [
    "-5", "10", "100", "2.5", " ", "Test", "test&*#", "", " 125445244545"
])
def test_positive_int_zero_to_nine_error(test_values):
    with pytest.raises(text_scrolling.argparse.ArgumentTypeError):
        text_scrolling.positive_int_zero_to_nine(test_values)


@pytest.mark.parametrize("test_values, expected_results", [
    ("red", "red"), ("Green", "green"), ("BLUE", "blue"),
    ("yeLLOW", "yellow"), ("magenta", "magenta"),
    ("Cyan", "cyan"), ("whiTe", "white")
])
def test_color_type_normal(test_values, expected_results):
    result = text_scrolling.color_type(test_values)
    assert result


@pytest.mark.parametrize("test_values", [
    "orange", "12", "who", "<>", "", " ", "ter8934", "834DFD",
    "blue1", "234", "55white"
])
def test_color_type_error(test_values):
    with pytest.raises(text_scrolling.argparse.ArgumentTypeError):
        text_scrolling.color_type(test_values)


@mock.patch.dict(os.environ, {"TERM": "xterm-256color"})
def test_set_curses_color_random():
    with mock.patch.object(text_scrolling.random, "randrange", return_value=24):
        curses.initscr()
        curses.start_color()
        text_scrolling.set_curses_color("random", "black")
        assert curses.pair_content(2) == (24, 16)
        assert curses.pair_content(1) == (16, 16)


@pytest.mark.parametrize("bg_color, color_num", [
    ("red", 1), ("green", 2), ("yellow", 3), ("blue", 4),
    ("magenta", 5), ("cyan", 6), ("white", 7),
])
@mock.patch.dict(os.environ, {"TERM": "xterm-256color"})
def test_set_curses_color_random_set_bg_color(bg_color, color_num):
    with mock.patch.object(text_scrolling.random, "randrange", return_value=24):
        curses.initscr()
        curses.start_color()
        text_scrolling.set_curses_color("random", bg_color)
        assert curses.pair_content(2) == (24, color_num)
        assert curses.pair_content(1) == (16, 16)


@pytest.mark.parametrize("color, color_num", [
    ("red", 1), ("green", 2), ("yellow", 3), ("blue", 4),
    ("magenta", 5), ("cyan", 6), ("white", 7),
])
@mock.patch.dict(os.environ, {"TERM": "xterm-256color"})
def test_set_curses_color_color(color, color_num):
    curses.initscr()
    curses.start_color()
    text_scrolling.set_curses_color(color, "black")
    assert curses.pair_content(2) == (color_num, 16)
    assert curses.pair_content(1) == (16, 16)


@pytest.mark.parametrize("bg_color, color_num", [
    ("red", 1), ("green", 2), ("yellow", 3), ("blue", 4),
    ("magenta", 5), ("cyan", 6), ("white", 7),
])
@mock.patch.dict(os.environ, {"TERM": "xterm-256color"})
def test_set_curses_color_color_bg_color(bg_color, color_num):
    curses.initscr()
    curses.start_color()
    text_scrolling.set_curses_color("blue", bg_color)
    assert curses.pair_content(2) == (4, color_num)
    assert curses.pair_content(1) == (16, 16)


def test_argument_parser_show_help(capsys):
    with pytest.raises(SystemExit):
        text_scrolling.argument_parser(["-h"])
        captured_output = capsys.readouterr().out
        assert "usage:" in captured_output


def test_text_scrolling_main_show_help(capsys):
    with pytest.raises(SystemExit):
        text_scrolling.main(["-h"])
        captured_output = capsys.readouterr().out
        assert "usage:" in captured_output
