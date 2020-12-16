#!/usr/bin/env python3
import unittest
import matplotlib.pyplot as plt


def part_one(numbers, th=2020):
    nums = [int(n) for n in numbers.split(",")]
    num_dict = {int(n): i + 1 for i, n in enumerate(nums)}
    prev = nums[-1]
    for i in range(len(nums), th):
        age_of_prev = i - num_dict[prev] if prev in num_dict.keys() else 0
        num_dict[prev] = i
        prev = age_of_prev
    return age_of_prev


class TestMemoryGame(unittest.TestCase):
    def test_part_one(self):
        self.assertEqual(436, part_one("0,3,6"))
        self.assertEqual(1, part_one("1,3,2"))
        self.assertEqual(10, part_one("2,1,3"))
        self.assertEqual(27, part_one("1,2,3"))
        self.assertEqual(78, part_one("2,3,1"))
        self.assertEqual(438, part_one("3,2,1"))
        self.assertEqual(1836, part_one("3,1,2"))

    def test_part_two(self):
        th = 30000000
        self.assertEqual(175594, part_one("0,3,6", th))
        self.assertEqual(2578, part_one("1,3,2", th))
        self.assertEqual(3544142, part_one("2,1,3", th))
        self.assertEqual(261214, part_one("1,2,3", th))
        self.assertEqual(6895259, part_one("2,3,1", th))
        self.assertEqual(18, part_one("3,2,1", th))
        self.assertEqual(362, part_one("3,1,2", th))


if __name__ == "__main__":
    puzzle_input = "0,3,1,6,7,5"
    result = part_one(puzzle_input)
    print(f"Given your starting numbers, the 2020th number spoken is {result}")
    result2 = part_one(puzzle_input, 30000000)
    print(f"Given your starting numbers, the 30000000th number spoken is {result2}")
