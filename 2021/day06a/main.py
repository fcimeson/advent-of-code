#!/usr/bin/env python3

import re
import sys
import argparse


class CustomList(list):
    def __init__(self, size=0):
        super().__init__([0] * size)

    def __str__(self):
        return super().__str__().strip("[").rstrip("]")


if __name__ == "__main__":

    # Args
    parser = argparse.ArgumentParser(description="Advent of Code")
    parser.add_argument("input", help="input file")
    parser.add_argument("--days", type=int, default=80, help="length of simulation")
    parser.add_argument("-d", "--debug", action="store_true", help="enable debug code")
    args = parser.parse_args()

    # Data
    fish = CustomList()
    with open(args.input, "r") as f:
        for line in f.readlines():
            if re.match(r"^[\s\d,]+$", line):
                fish.extend([int(x) for x in re.findall(r"\d+", line)])

    # Simulate
    if args.debug:
        print(f"After 0 days: {fish}")
    for day in range(1, args.days + 1):
        new_fish = []
        for i, timer in enumerate(fish):
            if timer == 0:
                new_fish.append(8)
                fish[i] = 6
            else:
                fish[i] = timer - 1
        fish.extend(new_fish)
        if args.debug:
            print(f"After {day} days: {fish}")
    print(f"Number of fish = {len(fish)}")
