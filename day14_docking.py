#!/usr/bin/env python3

import re


def part_one(prog_str):
    mem = {}
    p = re.compile(r"mem\[(\d+)\] = (\d+)\n")
    for instructions_str in prog_str.split("mask = "):
        if instructions_str != "":
            mask, _, write_ops = instructions_str.partition("\n")
            a, b = int(mask.replace("X", "1"), 2), int(mask.replace("X", "0"), 2)
            for i, j in p.findall(write_ops):
                addr, value = int(i), int(j)
                mem[addr] = (value & a) | b
    return sum(mem.values())


def part_two(prog_str):
    mem = {}
    p = re.compile(r"mem\[(\d+)\] = (\d+)\n")
    for instructions_str in prog_str.split("mask = "):
        if instructions_str != "":
            mask, _, write_ops = instructions_str.partition("\n")
            a, x_loc, x_count = (
                int(mask.replace("X", "1"), 2),
                [i for i, v in enumerate(mask) if v == "X"],
                mask.count("X"),
            )
            for i, j in p.findall(write_ops):
                addr, value = f"{int(i) | a:036b}", int(j)
                addrs = []
                for var in range(pow(2, x_count)):
                    temp_mask = addr
                    for loc, val in zip(x_loc, f"{var:0{x_count}b}"):
                        temp_mask = temp_mask[:loc] + val + temp_mask[loc + 1 :]
                    addrs.append(temp_mask)
                for i in addrs:
                    mem[int(i, 2)] = value
    return sum(mem.values())


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Emulation in software of the decoder chip"
    )
    parser.add_argument(
        "program",
        type=open,
        help="The initialization program (your puzzle input).",
    )

    program = parser.parse_args().program
    prog_str = program.read()
    program.close()
    result = part_one(prog_str)
    print(f"Part one: {result}")
    result2 = part_two(prog_str)
    print(f"Part two: {result2}")