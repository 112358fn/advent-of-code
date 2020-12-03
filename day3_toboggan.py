#!/usr/bin/env python3

# --- Day 3: Toboggan Trajectory ---
# With the toboggan login problems resolved, you set off toward the airport. While travel by toboggan might be easy, it's certainly not safe: there's very minimal steering and the area is covered in trees. You'll need to see which angles will take you near the fewest trees.
# Due to the local geology, trees in this area only grow on exact integer coordinates in a grid. You make a map (your puzzle input) of the open squares (.) and trees (#) you can see. For example:
## ..##.......
## #...#...#..
## .#....#..#.
## ..#.#...#.#
## .#...##..#.
## ..#.##.....
## .#.#.#....#
## .#........#
## #.##...#...
## #...##....#
## .#..#...#.#
# These aren't the only trees, though; due to something you read about once involving arboreal genetics and biome stability, the same pattern repeats to the right many times:
## ..##.........##.........##.........##.........##.........##.......  --->
## #...#...#..#...#...#..#...#...#..#...#...#..#...#...#..#...#...#..
## .#....#..#..#....#..#..#....#..#..#....#..#..#....#..#..#....#..#.
## ..#.#...#.#..#.#...#.#..#.#...#.#..#.#...#.#..#.#...#.#..#.#...#.#
## .#...##..#..#...##..#..#...##..#..#...##..#..#...##..#..#...##..#.
## ..#.##.......#.##.......#.##.......#.##.......#.##.......#.##.....  --->
## .#.#.#....#.#.#.#....#.#.#.#....#.#.#.#....#.#.#.#....#.#.#.#....#
## .#........#.#........#.#........#.#........#.#........#.#........#
## #.##...#...#.##...#...#.##...#...#.##...#...#.##...#...#.##...#...
## #...##....##...##....##...##....##...##....##...##....##...##....#
## .#..#...#.#.#..#...#.#.#..#...#.#.#..#...#.#.#..#...#.#.#..#...#.#  --->
# You start on the open square (.) in the top-left corner and need to reach the bottom (below the bottom-most row on your map).
# The toboggan can only follow a few specific slopes (you opted for a cheaper model that prefers rational numbers); start by counting all the trees you would encounter for the slope right 3, down 1:
# From your starting position at the top-left, check the position that is right 3 and down 1. Then, check the position that is right 3 and down 1 from there, and so on until you go past the bottom of the map.
# The locations you'd check in the above example are marked here with O where there was an open square and X where there was a tree:
## ..##.........##.........##.........##.........##.........##.......  --->
## #..O#...#..#...#...#..#...#...#..#...#...#..#...#...#..#...#...#..
## .#....X..#..#....#..#..#....#..#..#....#..#..#....#..#..#....#..#.
## ..#.#...#O#..#.#...#.#..#.#...#.#..#.#...#.#..#.#...#.#..#.#...#.#
## .#...##..#..X...##..#..#...##..#..#...##..#..#...##..#..#...##..#.
## ..#.##.......#.X#.......#.##.......#.##.......#.##.......#.##.....  --->
## .#.#.#....#.#.#.#.O..#.#.#.#....#.#.#.#....#.#.#.#....#.#.#.#....#
## .#........#.#........X.#........#.#........#.#........#.#........#
## #.##...#...#.##...#...#.X#...#...#.##...#...#.##...#...#.##...#...
## #...##....##...##....##...#X....##...##....##...##....##...##....#
## .#..#...#.#.#..#...#.#.#..#...X.#.#..#...#.#.#..#...#.#.#..#...#.#  --->
# In this example, traversing the map using this slope would cause you to encounter 7 trees.
# Starting at the top-left corner of your map and following a slope of right 3 and down 1, how many trees would you encounter?
#
## TEST: python -m unittest day3_toboggan.py
## RUN: ./day3_toboggan.py $(cat day3_map_pattern.txt )
#
# --- Part Two ---
# Time to check the rest of the slopes - you need to minimize the probability of a sudden arboreal stop, after all.
# Determine the number of trees you would encounter if, for each of the following slopes, you start at the top-left corner and traverse the map all the way to the bottom:
# Right 1, down 1.
# Right 3, down 1. (This is the slope you already checked.)
# Right 5, down 1.
# Right 7, down 1.
# Right 1, down 2.
# In the above example, these slopes would find 2, 7, 3, 4, and 2 tree(s) respectively; multiplied together, these produce the answer 336.
# What do you get if you multiply together the number of trees encountered on each of the listed slopes?

import unittest
import time
from math import ceil, floor, prod
from pprint import pprint


def trees_in_path(map_pattern, right=3, down=1):
    pattern_width = len(map_pattern[0])
    pattern_length = len(map_pattern)
    slope = right / down
    initial_position = 0
    final_position = ((pattern_length - 1) * slope) + initial_position
    num_patterns = ceil(final_position / pattern_width)
    complete_map = [x * num_patterns for x in map_pattern]
    tree_in_slope = [
        True if complete_map[c][floor(c * slope)] == "#" else False
        for c in range(down, pattern_length, down)
    ]
    # This is just to get a nice map
    for c in range(down, pattern_length, down):
        map_slice = complete_map[c]
        lat_pos = floor(c * slope)
        if map_slice[lat_pos] == "#":
            marker = "X"
        else:
            marker = "O"
        complete_map[c] = map_slice[:lat_pos] + marker + map_slice[lat_pos + 1 :]
    # Uncomment just to debug
    # pprint(complete_map)
    return sum(tree_in_slope)


class TestTreeCounter(unittest.TestCase):
    def setUp(self):
        self.startTime = time.time()

    def tearDown(self):
        t = time.time() - self.startTime
        print(f"{self.id()}: {t}")

    def test_tree_count(self):
        example_data = [
            "..##.......",
            "#...#...#..",
            ".#....#..#.",
            "..#.#...#.#",
            ".#...##..#.",
            "..#.##.....",
            ".#.#.#....#",
            ".#........#",
            "#.##...#...",
            "#...##....#",
            ".#..#...#.#",
        ]
        result = trees_in_path(map_pattern=example_data)
        self.assertEqual(result, 7)

    def test_tree_count(self):
        example_data = [
            "..##.......",
            "#...#...#..",
            ".#....#..#.",
            "..#.#...#.#",
            ".#...##..#.",
            "..#.##.....",
            ".#.#.#....#",
            ".#........#",
            "#.##...#...",
            "#...##....#",
            ".#..#...#.#",
        ]
        slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
        result = [trees_in_path(example_data, *slope) for slope in slopes]
        self.assertEqual(result, [2, 7, 3, 4, 2])
        self.assertEqual(prod(result), 336)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Count the trees in the slope")
    parser.add_argument("map_pattern", type=str, nargs="+", help="map pattern")
    parser.add_argument(
        "--verify",
        dest="verify",
        action="store_const",
        const=True,
        default=False,
        help="Check other slopes",
    )

    map_pattern = parser.parse_args().map_pattern
    verify = parser.parse_args().verify
    if not verify:
        result = trees_in_path(map_pattern)
        print(
            f"In this example, traversing the map using this slope would cause you to encounter {result} trees."
        )
    else:
        slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
        result = [trees_in_path(map_pattern, *slope) for slope in slopes]
        print(
            f"In the above example, these slopes would find {result} tree(s) respectively; multiplied together, these produce the answer {prod(result)}."
        )
