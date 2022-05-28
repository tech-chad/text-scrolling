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
