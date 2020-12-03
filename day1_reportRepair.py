#!/usr/bin/env python3

## --- Part One ---
# Before you leave, the Elves in accounting just need you to fix your expense report (your puzzle input); apparently, something isn't quite adding up.
# Specifically, they need you to find the two entries that sum to 2020 and then multiply those two numbers together.
# For example, suppose your expense report contained the following:
## 1721
## 979
## 366
## 299
## 675
## 1456
# In this list, the two entries that sum to 2020 are 1721 and 299. Multiplying them together produces 1721 * 299 = 514579, so the correct answer is 514579.
# Of course, your expense report is much larger. Find the two entries that sum to 2020; what do you get if you multiply them together?
#
## TEST:    $ python -m unittest day1_reportRepair.py
## RUN:     $ ./day1_reportRepair.py $(cat day1_expense_report.txt) --distribute_in 2
#
## --- Part Two ---
# The Elves in accounting are thankful for your help; one of them even offers you a starfish coin they had left over from a past vacation. They offer you a second one if you can find three numbers in your expense report that meet the same criteria.
# Using the above example again, the three entries that sum to 2020 are 979, 366, and 675. Multiplying them together produces the answer, 241861950.
# In your expense report, what is the product of the three entries that sum to 2020?
#
## TEST:    $ python -m unittest day1_reportRepair.py
## RUN:     $ ./day1_reportRepair.py $(cat day1_expense_report.txt) --distribute_in 3
#

import unittest
import time


def multiply_entries_that_addsTo(list_of_entries, distribute_in=2, adds_to=2020):
    """Mulply entries that toghether adds to a number

    Keyword arguments:
    list_of_entries -- list of the entries where to search for a matching criteria
    distribute_in -- number of entries that needs to add to the result
    adds_to -- the result that the number of entries needs to match
    """
    for x in list_of_entries:
        y = adds_to - x
        subset = list(filter(lambda entry: entry <= y, list_of_entries))
        # subset = list_of_entries
        if distribute_in == 2:
            if y in subset:
                return x, y, x * y
        else:
            val = multiply_entries_that_addsTo(subset, distribute_in - 1, adds_to=y)
            if val is not None:
                return x, *val[:-1], x * val[-1]
    return None


class TestFind2020(unittest.TestCase):
    def setUp(self):
        self.startTime = time.time()

    def tearDown(self):
        t = time.time() - self.startTime
        print(f"{self.id()}: {t}")

    def test_multiply_2(self):
        example_data = [1721, 979, 366, 299, 675, 1456]
        self.assertEqual(multiply_entries_that_addsTo(example_data)[-1], 514579)

    def test_multiply_3(self):
        example_data = [1721, 979, 366, 299, 675, 1456]
        self.assertEqual(multiply_entries_that_addsTo(example_data, 3)[-1], 241861950)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Repair this expense report")
    parser.add_argument("entries", type=int, nargs="+", help="expense report entries")
    parser.add_argument(
        "--distribute_in",
        type=int,
        nargs="?",
        default=2,
        choices=[2, 3],
        help="number of entries that needs to adds to 2020",
    )

    entries = parser.parse_args().entries
    distribute_in = parser.parse_args().distribute_in
    result = multiply_entries_that_addsTo(entries, distribute_in=distribute_in)
    if result is not None:
        print(
            f"The {distribute_in} entries that sum to 2020 are {result[:-1]}. Multiplying them together produces the answer, {result[-1]}."
        )
