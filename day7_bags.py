#!/usr/bin/env python3

# -- Day 7: Handy Haversacks ---
# You land at the regional airport in time for your next flight. In fact, it looks like you'll even have time to grab some food: all flights are currently delayed due to issues in luggage processing.
# Due to recent aviation regulations, many rules (your puzzle input) are being enforced about bags and their contents; bags must be color-coded and must contain specific quantities of other color-coded bags. Apparently, nobody responsible for these regulations considered how long they would take to enforce!
# For example, consider the following rules:
# light red bags contain 1 bright white bag, 2 muted yellow bags.
# dark orange bags contain 3 bright white bags, 4 muted yellow bags.
# bright white bags contain 1 shiny gold bag.
# muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
# shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
# dark olive bags contain 3 faded blue bags, 4 dotted black bags.
# vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
# faded blue bags contain no other bags.
# dotted black bags contain no other bags.
# These rules specify the required contents for 9 bag types. In this example, every faded blue bag is empty, every vibrant plum bag contains 11 bags (5 faded blue and 6 dotted black), and so on.
# You have a shiny gold bag. If you wanted to carry it in at least one other bag, how many different bag colors would be valid for the outermost bag? (In other words: how many colors can, eventually, contain at least one shiny gold bag?)
# In the above rules, the following options would be available to you:
# A bright white bag, which can hold your shiny gold bag directly.
# A muted yellow bag, which can hold your shiny gold bag directly, plus some other bags.
# A dark orange bag, which can hold bright white and muted yellow bags, either of which could then hold your shiny gold bag.
# A light red bag, which can hold bright white and muted yellow bags, either of which could then hold your shiny gold bag.
# So, in this example, the number of bag colors that can eventually contain at least one shiny gold bag is 4.
# How many bag colors can eventually contain at least one shiny gold bag? (The list of rules is quite long; make sure you get all of it.
# Your puzzle answer was 274.
#
# --- Part Two ---
# It's getting pretty expensive to fly these days - not because of ticket prices, but because of the ridiculous number of bags you need to buy!
# Consider again your shiny gold bag and the rules from the above example:
# faded blue bags contain 0 other bags.
# dotted black bags contain 0 other bags.
# vibrant plum bags contain 11 other bags: 5 faded blue bags and 6 dotted black bags.
# dark olive bags contain 7 other bags: 3 faded blue bags and 4 dotted black bags.
# So, a single shiny gold bag must contain 1 dark olive bag (and the 7 bags within it) plus 2 vibrant plum bags (and the 11 bags within each of those): 1 + 1*7 + 2 + 2*11 = 32 bags!
# Of course, the actual rules have a small chance of going several levels deeper than this example; be sure to count all of the bags, even if the nesting becomes topologically impractical!
# Here's another example:
# shiny gold bags contain 2 dark red bags.
# dark red bags contain 2 dark orange bags.
# dark orange bags contain 2 dark yellow bags.
# dark yellow bags contain 2 dark green bags.
# dark green bags contain 2 dark blue bags.
# dark blue bags contain 2 dark violet bags.
# dark violet bags contain no other bags.
# In this example, a single shiny gold bag must contain 126 other bags.
# How many individual bags are required inside your single shiny gold bag?
# Your puzzle answer was 158730.

import unittest
import time
import re
from pprint import pprint


def extract(data):
    bags = {}
    regex = r"^(\w+ \w+) bags contain (no other bags|.*)\.$"
    sub_regex = r"([0-9]+) (\w+ \w+) bag"
    for line in data.split("\n"):
        matches = re.findall(regex, line)
        match = matches[0]
        if "no other bags" in match[1]:
            bags[match[0]] = None
        else:
            sub_matches = re.findall(sub_regex, match[1])
            bags[match[0]] = {
                sub_match[1]: int(sub_match[0]) for sub_match in sub_matches
            }
    return bags


def find_container_for(bags, total, *colors):
    can_contain = []
    for color in colors:
        for container, allowed_colors in bags.items():
            if allowed_colors is None:
                continue
            if color in allowed_colors:
                can_contain.append(container)
    if len(can_contain) == 0:
        return total
    total.extend(can_contain)
    return find_container_for(bags, total, *can_contain)


def count_all(bags, color):
    count = 0
    if bags[color] is not None:
        for bag, number in bags[color].items():
            count += number * count_all(bags, bag)
    return count + 1


class TestBoardingPass(unittest.TestCase):
    # def setUp(self):
    #     self.startTime = time.time()

    # def tearDown(self):
    #     t = time.time() - self.startTime
    #     print(f"{self.id()}: {t}")

    def test_extraction(self):
        with open("day7_example1.txt") as example_file:
            example1 = example_file.read()
        bags = extract(example1)
        intended_data_estructure = {
            "bright white": {"shiny gold": 1},
            "dark olive": {"dotted black": 4, "faded blue": 3},
            "dark orange": {"bright white": 3, "muted yellow": 4},
            "dotted black": None,
            "faded blue": None,
            "light red": {"bright white": 1, "muted yellow": 2},
            "muted yellow": {"faded blue": 9, "shiny gold": 2},
            "shiny gold": {"dark olive": 1, "vibrant plum": 2},
            "vibrant plum": {"dotted black": 6, "faded blue": 5},
        }
        self.assertEqual(bags, intended_data_estructure)

    def test_find_container_for(self):
        with open("day7_example1.txt") as example_file:
            example1 = example_file.read()
        bags = extract(example1)
        count_containers = len(set(find_container_for(bags, [], "shiny gold")))
        self.assertEqual(4, count_containers)

    def test_count_all(self):
        with open("day7_example1.txt") as example_file:
            example1 = example_file.read()
        bags = extract(example1)
        count = count_all(bags, "shiny gold") - 1
        self.assertEqual(32, count)

        with open("day7_example2.txt") as example_file:
            example2 = example_file.read()
        bags = extract(example2)
        count = count_all(bags, "shiny gold") - 1
        self.assertEqual(126, count)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Bags rules")
    parser.add_argument(
        "bags_rules",
        type=open,
        help="txt file containing the many rules (your puzzle input) that are being enforced about bags and their contents",
    )

    rules = parser.parse_args().bags_rules
    rules_str = rules.read()
    rules.close()
    bags = extract(rules_str)
    count_containers = len(set(find_container_for(bags, [], "shiny gold")))
    required_bags = count_all(bags, "shiny gold") - 1
    print(
        f"{count_containers} bag colors can eventually contain at least one shiny gold bag"
    )
    print(
        f"{required_bags} individual bags are required inside your single shiny gold bag"
    )