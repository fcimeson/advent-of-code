#!/usr/bin/env python3

import re
import argparse

if __name__ == "__main__":

    # Args
    parser = argparse.ArgumentParser(description="Advent of Code")
    parser.add_argument("input", help="input file")
    parser.add_argument("-d", "--debug", action="store_true", help="enable debug code")
    args = parser.parse_args()

    # Data
    data = None
    with open(args.input, "r") as f:
        data = [int(line) for line in f.readlines() if re.match(r"^\s*\d+\s*$", line)]

    # Part 1
    total = 0
    prev = None
    for new in data:
        if prev is not None and new > prev:
            total += 1
        prev = new
    print(f"Part 1: There are {total} measurements larger than the previous measurements.")

    # Part 2
    total = 0
    prev = None
    for i in range(len(data) - 2):
        new = sum(data[i : i + 3])
        if prev is not None and new > prev:
            total += 1
        prev = new
    print(f"Part 2: There are {total} measurements larger than the previous measurements.")
