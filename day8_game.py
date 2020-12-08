#!/usr/bin/env python3

import unittest


def extract(data):
    return [[line.split()[0], int(line.split()[1])] for line in data.split("\n")]


def count_until_loop(instructions):
    program_pointer = 0
    pointer_prev_locations = []
    accumulator = 0
    while program_pointer not in pointer_prev_locations:
        if program_pointer >= len(instructions):
            break
        pointer_prev_locations.append(program_pointer)
        instruction = instructions[program_pointer]
        if instruction[0] == "acc":
            accumulator += instruction[1]
            program_pointer += 1
            continue
        elif instruction[0] == "jmp":
            program_pointer += instruction[1]
            continue
        elif instruction[0] == "nop":
            program_pointer += 1
            continue
    return accumulator, pointer_prev_locations


from copy import copy


def break_loop(instructions):
    # print(instructions)
    for index, instruction in enumerate(instructions):
        if instruction[0] == "nop":
            new_in = ["jmp", instruction[1]]
        elif instruction[0] == "jmp":
            new_in = ["nop", instruction[1]]
        else:
            new_in = instruction
        new_ins = [
            new_in if i == index else old_in for i, old_in in enumerate(instructions)
        ]
        # print(new_ins)
        counter, locations = count_until_loop(new_ins)
        if locations[-1] == (len(instructions) - 1):
            break
    return counter, locations


class TestBoardingPass(unittest.TestCase):
    # def setUp(self):
    #     self.startTime = time.time()

    # def tearDown(self):
    #     t = time.time() - self.startTime
    #     print(f"{self.id()}: {t}")

    def test_extraction(self):
        with open("day8_example.txt") as example_file:
            example1 = example_file.read()
        codes = extract(example1)
        intended_data_estructure = [
            ["nop", +0],
            ["acc", +1],
            ["jmp", +4],
            ["acc", +3],
            ["jmp", -3],
            ["acc", -99],
            ["acc", +1],
            ["jmp", -4],
            ["acc", +6],
        ]
        self.assertEqual(codes, intended_data_estructure)

    def test_count_until_loop(self):
        with open("day8_example.txt") as example_file:
            example1 = example_file.read()
        codes = extract(example1)
        count = count_until_loop(codes)[0]
        self.assertEqual(count, 5)

    def test_break_loop(self):
        with open("day8_example.txt") as example_file:
            example1 = example_file.read()
        codes = extract(example1)
        count, _ = break_loop(codes)
        self.assertEqual(8, count)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Analize the boot code (your puzzle input) of the device"
    )
    parser.add_argument(
        "boot_code",
        type=open,
        help="txt file containing the boot code (your puzzle input) of the device",
    )

    boot_code = parser.parse_args().boot_code
    boot_code_str = boot_code.read()
    boot_code.close()
    codes = extract(boot_code_str)
    count, steps = count_until_loop(codes)
    print(
        f"Immediately before any instruction is executed a second time, the {count} value is in the accumulator"
    )
    count, _ = break_loop(codes)
    print(f"{count} is the value of the accumulator after the program terminates")
