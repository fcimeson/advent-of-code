#!/usr/bin/env python3

import re
import sys
import copy
import math
import enum
import numpy
import pickle
import argparse


def blink(stone):
    if stone == 0:
        return [1]
    n = len(str(stone))
    if n >= 2 and n % 2 == 0:
        return [int(str(stone)[0 : n // 2]), int(str(stone)[n // 2 :])]
    return [stone * 2024]


if __name__ == "__main__":

    # Args
    parser = argparse.ArgumentParser(description="Advent of Code")
    parser.add_argument("input", help="input file")
    parser.add_argument("-d", "--debug", action="store_true")
    args = parser.parse_args()

    stones_00 = []
    with open(args.input, "r") as f:
        for line in f.readlines():
            stones_00 = [int(x) for x in re.findall(r"\d+", line)]

    # Part 1
    stones = copy.deepcopy(stones_00)
    for _ in range(25):
        new_stones = []
        for stone in stones:
            new_stones += blink(stone)
        stones = new_stones
        if args.debug:
            print(stones)

    print(f"Part 1: result = {len(stones)}")

    # Part 2
    stones = {}
    for stone in stones_00:
        if stone not in stones:
            stones[stone] = 0
        stones[stone] += 1

    for _ in range(75):
        new_stones = {}
        for stone, count in stones.items():
            for new_stone in blink(stone):
                if new_stone not in new_stones:
                    new_stones[new_stone] = 0
                new_stones[new_stone] += count
        stones = new_stones
        if args.debug:
            print(stones)
    result = sum([count for count in stones.values()])

    print(f"Part 2: result = {result}")
