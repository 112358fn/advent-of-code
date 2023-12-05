import re

import pytest


def day01(input: str, fix: bool) -> str:  # pragma: no cover
    lines = input.splitlines()
    _func = first_last_digits_fix if fix else first_last_digits
    numbers = map(_func, lines)
    return str(sum(numbers))


def first_last_digits(input: str) -> int:
    numbers = filter(lambda x: x.isdigit(), input)
    digits = list(map(int, numbers))
    return 10 * digits[0] + digits[-1]


def str_int(x: str) -> int:
    match x:
        case "one": _val = 1
        case "two": _val = 2
        case "three": _val = 3
        case "four": _val = 4
        case "five": _val = 5
        case "six":  _val = 6
        case "seven": _val = 7
        case "eight": _val = 8
        case "nine": _val = 9
        case _: _val = int(x)
    return _val


def first_last_digits_fix(input: str) -> int:
    pattern = r"(?=(one|two|three|four|five|six|seven|eight|nine|[0-9]))"
    _re = re.compile(pattern)
    numbers = map(str_int, _re.findall(input))
    digits = list(numbers)
    return (10 * digits[0]) + digits[-1]


@pytest.mark.parametrize(
    ("input", "expected_output"),
    [
        ("1abc2", 12),
        ("pqr3stu8vwx", 38),
        ("a1b2c3d4e5f", 15),
        ("treb7uchet", 77),
    ],
)
def test_first_last_digit(input: str, expected_output: int) -> None:
    assert first_last_digits(input) == expected_output


@pytest.mark.parametrize(
    ("input", "expected_output"),
    [
        ("two1nine", 29),
        ("eightwothree", 83),
        ("abcone2threexyz", 13),
        ("xtwone3four", 24),
        ("4nineeightseven2", 42),
        ("zoneight234", 14),
        ("7pqrstsixteen", 76),
        ("oneight", 18),
    ],
)
def test_first_last_digit_fix(input: str, expected_output: int) -> None:
    assert first_last_digits_fix(input) == expected_output
