"""Advent of Code 2023."""
from typing import TextIO

import click

from . import days

DAYS = [
    "day01",
]


@click.command()
@click.argument("day", type=click.Choice(DAYS))
@click.argument("input", type=click.File())
@click.option("--fix", is_flag=True)
def cli(day: str, input: TextIO, fix: bool) -> None:
    """Advent of Code 2023.

    DAY: 1-25
    INPUT: input file
    """
    input_str = input.read()
    match day:
        case "day01":
            result = days.day01(input_str, fix)
        case _:
            result = "Not implemented yet"
    click.echo(result)
