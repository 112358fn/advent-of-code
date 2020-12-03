#!/usr/bin/env python3

## --- Part One ---
# --- Day 2: Password Philosophy ---
# Your flight departs in a few days from the coastal airport; the easiest way down to the coast from here is via toboggan.
# The shopkeeper at the North Pole Toboggan Rental Shop is having a bad day. "Something's wrong with our computers; we can't log in!" You ask if you can take a look.
# Their password database seems to be a little corrupted: some of the passwords wouldn't have been allowed by the Official Toboggan Corporate Policy that was in effect when they were chosen.
# To try to debug the problem, they have created a list (your puzzle input) of passwords (according to the corrupted database) and the corporate policy when that password was set.
# For example, suppose you have the following list:
## 1-3 a: abcde
## 1-3 b: cdefg
## 2-9 c: ccccccccc
# Each line gives the password policy and then the password. The password policy indicates the lowest and highest number of times a given letter must appear for the password to be valid. For example, 1-3 a means that the password must contain a at least 1 time and at most 3 times.
# In the above example, 2 passwords are valid. The middle password, cdefg, is not; it contains no instances of b, but needs at least 1. The first and third passwords are valid: they contain one a or nine c, both within the limits of their respective policies.
# How many passwords are valid according to their policies?
#
## TEST: python -m unittest day2_password.py
## RUN: ./day2_password.py $(cat day2_passwds_policies.txt )
#


##--- Part Two ---
# While it appears you validated the passwords correctly, they don't seem to be what the Official Toboggan Corporate Authentication System is expecting.
# The shopkeeper suddenly realizes that he just accidentally explained the password policy rules from his old job at the sled rental place down the street! The Official Toboggan Corporate Policy actually works a little differently.
# Each policy actually describes two positions in the password, where 1 means the first character, 2 means the second character, and so on. (Be careful; Toboggan Corporate Policies have no concept of "index zero"!) Exactly one of these positions must contain the given letter. Other occurrences of the letter are irrelevant for the purposes of policy enforcement.
# Given the same example list from above:
# 1-3 a: abcde is valid: position 1 contains a and position 3 does not.
# 1-3 b: cdefg is invalid: neither position 1 nor position 3 contains b.
# 2-9 c: ccccccccc is invalid: both position 2 and position 9 contain c.
# How many passwords are valid according to the new interpretation of the policies?
#
## TEST: python -m unittest day2_password.py
## RUN: ./day2_password.py $(cat day2_passwds_policies.txt ) --new
#

import unittest
import time


def password_is_valid(policy_passwd, new_interpretation=False):
    if not new_interpretation:
        return [
            int(val.split("-")[0]) <= passwd.count(letter[0]) <= int(val.split("-")[1])
            for val, letter, passwd in policy_passwd
        ]
    else:
        return [
            (passwd[int(val.split("-")[0]) - 1] == letter[0])
            ^ (passwd[int(val.split("-")[1]) - 1] == letter[0])
            for val, letter, passwd in policy_passwd
        ]


class TestPasswd(unittest.TestCase):
    def setUp(self):
        self.startTime = time.time()

    def tearDown(self):
        t = time.time() - self.startTime
        print(f"{self.id()}: {t}")

    def test_password_valid(self):
        example_data = [
            ["1-3", "a:", "abcde"],
            ["1-3", "b:", "cdefg"],
            ["2-9", "c:", "ccccccccc"],
        ]
        self.assertEqual(password_is_valid(example_data), [True, False, True])
        self.assertEqual(sum(password_is_valid(example_data)), 2)

    def test_new_password_valid(self):
        example_data = [
            ["1-3", "a:", "abcde"],
            ["1-3", "b:", "cdefg"],
            ["2-9", "c:", "ccccccccc"],
        ]
        result = password_is_valid(example_data, new_interpretation=True)
        self.assertEqual(
            result,
            [True, False, False],
        )
        self.assertEqual(sum(result), 1)


if __name__ == "__main__":
    import argparse
    from itertools import compress
    from pprint import pprint

    parser = argparse.ArgumentParser(description="Repair this expense report")
    parser.add_argument("entries", type=str, nargs="+", help="expense report entries")
    parser.add_argument(
        "--new",
        dest="new_policy",
        action="store_const",
        const=True,
        default=False,
        help="enable new password policy",
    )
    entries = parser.parse_args().entries
    new_interpretation = parser.parse_args().new_policy
    policy_passwd = [entries[x : x + 3] for x in range(0, len(entries), 3)]
    valid_passwd = password_is_valid(policy_passwd, new_interpretation)
    print(
        f"In the above example, {sum(valid_passwd)} of {len(policy_passwd)} passwords are valid"
    )
    print("\n# Examples of invalid passwords:")
    wrong = list(compress(policy_passwd, [not valid for valid in valid_passwd]))
    pprint(wrong[:5])
    print("\n# Examples of valid passwords:")
    right = list(compress(policy_passwd, valid_passwd))
    pprint(right[:5])
