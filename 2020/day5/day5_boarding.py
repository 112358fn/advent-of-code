#!/usr/bin/env python3

# --- Day 5: Binary Boarding ---
# You board your plane only to discover a new problem: you dropped your boarding pass! You aren't sure which seat is yours, and all of the flight attendants are busy with the flood of people that suddenly made it through passport control.
# You write a quick program to use your phone's camera to scan all of the nearby boarding passes (your puzzle input); perhaps you can find your seat through process of elimination.
# Instead of zones or groups, this airline uses binary space partitioning to seat people. A seat might be specified like FBFBBFFRLR, where F means "front", B means "back", L means "left", and R means "right".
# The first 7 characters will either be F or B; these specify exactly one of the 128 rows on the plane (numbered 0 through 127). Each letter tells you which half of a region the given seat is in. Start with the whole list of rows; the first letter indicates whether the seat is in the front (0 through 63) or the back (64 through 127). The next letter indicates which half of that region the seat is in, and so on until you're left with exactly one row.
# For example, consider just the first seven characters of FBFBBFFRLR:
# Start by considering the whole range, rows 0 through 127.
# F means to take the lower half, keeping rows 0 through 63.
# B means to take the upper half, keeping rows 32 through 63.
# F means to take the lower half, keeping rows 32 through 47.
# B means to take the upper half, keeping rows 40 through 47.
# B keeps rows 44 through 47.
# F keeps rows 44 through 45.
# The final F keeps the lower of the two, row 44.
# The last three characters will be either L or R; these specify exactly one of the 8 columns of seats on the plane (numbered 0 through 7). The same process as above proceeds again, this time with only three steps. L means to keep the lower half, while R means to keep the upper half.
# For example, consider just the last 3 characters of FBFBBFFRLR:
# Start by considering the whole range, columns 0 through 7.
# R means to take the upper half, keeping columns 4 through 7.
# L means to take the lower half, keeping columns 4 through 5.
# The final R keeps the upper of the two, column 5.
# So, decoding FBFBBFFRLR reveals that it is the seat at row 44, column 5.
# Every seat also has a unique seat ID: multiply the row by 8, then add the column. In this example, the seat has ID 44 * 8 + 5 = 357.
# Here are some other boarding passes:
# BFFFBBFRRR: row 70, column 7, seat ID 567.
# FFFBBBFRRR: row 14, column 7, seat ID 119.
# BBFFBBFRLL: row 102, column 4, seat ID 820.
# As a sanity check, look through your list of boarding passes. What is the highest seat ID on a boarding pass?
#
## TEST python -m unittest day5_boarding.py
## RUN ./day5_boarding.py $(cat day5_boarding_passes.txt )


# --- Part Two ---
# Ding! The "fasten seat belt" signs have turned on. Time to find your seat.
# It's a completely full flight, so your seat should be the only missing boarding pass in your list. However, there's a catch: some of the seats at the very front and back of the plane don't exist on this aircraft, so they'll be missing from your list as well.
# Your seat wasn't at the very front or back, though; the seats with IDs +1 and -1 from yours will be in your list.
# What is the ID of your seat?
#
## RUN ./day5_boarding.py $(cat day5_boarding_passes.txt )

import unittest
import time


def decode(code, positive="F"):
    lenght_code = len(code)
    values = list(range(0, pow(2, lenght_code)))
    for index, char in enumerate(code):
        step = pow(2, (lenght_code - 1 - index))
        values = values[0:step] if char == positive else values[step:]
    return values[0]


def findseat(boarding_pass):
    boarding_pass = boarding_pass.strip()
    # row = decode(boarding_pass[:7], positive="F")
    # column = decode(boarding_pass[7:], positive="L")
    row = int(boarding_pass[:7].replace("F", "0").replace("B", "1"), 2)
    column = int(boarding_pass[7:].replace("L", "0").replace("R", "1"), 2)
    seat_id = (row * 8) + column
    return row, column, seat_id


class TestBoardingPass(unittest.TestCase):
    def setUp(self):
        self.startTime = time.time()

    def tearDown(self):
        t = time.time() - self.startTime
        print(f"{self.id()}: {t}")

    def test_one_boarding_pass(self):
        test_str = "BFFFBBFRRR"
        result = findseat(boarding_pass=test_str)
        self.assertEqual(result, (70, 7, 567))
        test_str = "FFFBBBFRRR"
        result = findseat(boarding_pass=test_str)
        self.assertEqual(result, (14, 7, 119))
        test_str = "BBFFBBFRLL"
        result = findseat(boarding_pass=test_str)
        self.assertEqual(result, (102, 4, 820))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Find seat by code")
    parser.add_argument(
        "boarding_passes",
        type=str,
        nargs="+",
        help="boarding pass code",
    )

    boarding_passes = parser.parse_args().boarding_passes
    seat_IDs = [findseat(boarding_pass)[2] for boarding_pass in boarding_passes]
    seat_IDs.sort(reverse=True)
    highest_seat_id = seat_IDs[0]
    lowest_seat_id = seat_IDs[-1]
    print(
        f"The highest seat ID on a boarding pass is {highest_seat_id} and the lowest {lowest_seat_id}"
    )
    seat_IDs = set(seat_IDs)
    seat_range = set(range(lowest_seat_id, highest_seat_id + 1))
    seat_id = seat_range.difference(seat_IDs)
    print("The ID of your seat is", *seat_id)
    # This  might be more memory efficient: using range we generate
    for seat_id in range(lowest_seat_id, highest_seat_id + 1):
        if seat_id not in seat_IDs:
            print(f"The ID of your seat is {seat_id}")
            break
