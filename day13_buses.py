#!/usr/bin/env python3

# Credit to https://github.com/amhk/advent-of-code/tree/master/aoc-2020-12-13/src

import unittest
from functools import reduce
from math import prod


def part_one(earliest, buses_times):
    timestamp = int(earliest)
    buses_times = [int(bus) for bus in buses_times.split(",") if bus != "x"]
    possible_times = [(bus - (timestamp % bus)) % bus for bus in buses_times]
    min_time, bus = [
        (bus, time)
        for bus, time in zip(buses_times, possible_times)
        if time == min(possible_times)
    ][0]
    return bus, min_time


def lcm(n, m):
    # Our input is guaranteed to be only prime numbers, so lcm(n, m) == n * m.
    return n * m


def get_aligned(accumulated, next_gear):
    # Period and timestamp that previous gears sync
    period, timestamp = accumulated
    # Period and offset of gear to sync
    gear_period, gear_offset = next_gear
    # Calculate new period needed to align visited gears.
    new_period = lcm(period, gear_period)
    # Find timestamp when visited gears become aligned with current gear.
    # Start counting from current timestamp.
    i = 0
    new_timestamp = timestamp
    # Two gears allign (the accumulated and the new one)
    # at timestamp when the sum of timestamp and gearoffset
    # is multiple of the gear period
    while (new_timestamp + gear_offset) % gear_period != 0:
        i += 1
        # this is the new time all the previous gears sync again
        new_timestamp = period * i + timestamp
    # Finally new_timestamp is the time when
    # all the previous gears and the new one are in sync
    # AND they will be in sync with a period=new_period
    return new_period, new_timestamp


def part_two(buses_times):
    buses_times = [
        (int(period), offset)
        for offset, period in enumerate(buses_times.split(","))
        if period != "x"
    ]
    # References: [1] https://en.wikipedia.org/wiki/Least_common_multiple#Gears_problem
    #
    # Think of the buses as gears on the same axis. The gears have different number of teeth (the
    # bus IDs). Each gear has one marked tooth. At timestamp == 0 the gears are offset from each
    # other so that none of the marked teeth are aligned. Find the lowest timestamp when all gears
    # are aligned.
    #
    # According to [1], two gears with m and n teeth re-align after lcm(m, n) rotations.
    _, timestamp = reduce(get_aligned, buses_times, (1, 0))
    return timestamp


class TestBuses(unittest.TestCase):
    def test_partone(self):
        result = part_one("939", "7,13,x,x,59,x,31,19")
        self.assertEqual(prod(result), 295)

    def test_parttwo(self):
        self.assertEqual(part_two("7,13,x,x,59,x,31,19"), 1068781)
        self.assertEqual(part_two("17,x,13,19"), 3417)
        self.assertEqual(part_two("67,7,59,61"), 754018)
        self.assertEqual(part_two("67,x,7,59,61"), 779210)
        self.assertEqual(part_two("67,7,x,59,61"), 1261476)
        self.assertEqual(part_two("1789,37,47,1889"), 1202161486)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Analize your notes about bus departures"
    )
    parser.add_argument(
        "notes",
        type=open,
        help="Your notes (your puzzle input) consist of two lines.",
    )

    notes = parser.parse_args().notes
    notes_str = notes.read()
    notes.close()
    earliest, buses_times = notes_str.split("\n")
    bus, min_time = part_one(earliest, buses_times)
    print(
        f" {bus} is the ID of the earliest bus you can take to the airport\nmultiplied by {min_time} number of minutes you'll need to wait for that bus\nis {bus*min_time}"
    )
    timestamp = part_two(buses_times)
    print(
        f"At {timestamp} is the earliest timestamp such that all of the listed bus IDs depart at offsets matching their positions in the list"
    )
