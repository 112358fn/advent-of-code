#!/usr/bin/env python3

import unittest
import re
from functools import reduce
from copy import deepcopy
from time import time


def parse_decks(decks_str):
    regex = re.compile(
        r"Player 1:\n((?:\d+\n?)+)\nPlayer 2:\n((?:\d+\n?)+)", re.MULTILINE
    )
    d1, d2 = regex.search(decks_str).group(1, 2)
    d1 = [int(card) for card in d1.split("\n") if card != ""]
    d2 = [int(card) for card in d2.split("\n") if card != ""]
    return d1, d2


def calculate_score(winner_deck):
    return reduce(
        lambda count, element: count + (element[0] + 1) * element[1],
        enumerate(winner_deck[::-1]),
        0,
    )


def part_one(decks_str):
    deck1, deck2 = parse_decks(decks_str)
    while (len(deck1) > 0) and (len(deck2) > 0):
        c1, c2 = deck1.pop(0), deck2.pop(0)
        if c1 > c2:
            deck1.extend([c1, c2])
        else:
            deck2.extend([c2, c1])
    return calculate_score(deck1 if len(deck1) > 0 else deck2)


# Tried using memoize techniques but didn't improve performance
# very few hits in comparision with the number of miss
# @lru_cache(maxsize=None)
def combat_game(deck1, deck2):
    prevs = []
    while (len(deck1) > 0) and (len(deck2) > 0):
        # Verified this two decks have not played before
        current = hash((tuple(deck1), tuple(deck2)))
        if current in prevs:
            return deck1, []
        else:
            prevs.append(current)
        # Find the winner deck
        c1, c2 = deck1.pop(0), deck2.pop(0)
        if (len(deck1) >= c1) and (len(deck2) >= c2):
            dr1, _ = combat_game(deepcopy(deck1[:c1]), deepcopy(deck2[:c2]))
            p1_wins = len(dr1) > 0
        else:
            p1_wins = c1 > c2
        # Update the winner deck
        if p1_wins:
            deck1.extend([c1, c2])
        else:
            deck2.extend([c2, c1])
    return deck1, deck2


def part_two(decks_str):
    deck1, deck2 = parse_decks(decks_str)
    start_t = time()
    deck1, deck2 = combat_game(deck1, deck2)
    print(f"PART 2: Elapse time {time()-start_t}")
    return calculate_score(deck1 if len(deck1) > 0 else deck2)


class TestDay22(unittest.TestCase):
    def test_part_one(self):
        print("Test part one")
        decks_str = """Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10"""
        result = part_one(decks_str)
        self.assertEqual(result, 306)

    def test_part_two(self):
        print("Test part two")
        decks_str = """Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10"""
        score = part_two(decks_str)
        self.assertEqual(score, 291)

    def test_infinite(self):
        print("Test part two-infinite loop")
        decks_str = """Player 1:
43
19

Player 2:
2
29
14"""
        score = part_two(decks_str)
        self.assertEqual(score, 105)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Play a game of Combat ")
    parser.add_argument(
        "decks",
        type=open,
        help="Each player has their own deck (your puzzle input).",
    )

    decks = parser.parse_args().decks
    decks_str = decks.read()
    decks.close()
    result = part_one(decks_str)
    print(f"PART 1: The winning player's score is {result}")
    result = part_two(decks_str)
    print(f"PART 2: The winning player's score is {result}")