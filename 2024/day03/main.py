#!/usr/bin/env python3

import re
import sys
import copy
import math
import enum
import numpy
import pickle
import argparse

INF = float("inf")
RE_NUMBER = r"-?\d+"

if __name__ == "__main__":

    # Args
    parser = argparse.ArgumentParser(description="Advent of Code")
    parser.add_argument("input", default="input.txt", help="input file")
    args = parser.parse_args()

    result = 0
    with open(args.input, "r") as f:
        for line in f.readlines():
            for instruction in re.findall(r"mul\(\d{1,3},\d{1,3}\)", line):
                numbers = [int(x) for x in re.findall(r"\d+", instruction)]
                result += numbers[0] * numbers[1]
    print(f"Part 1: result = {result}")

    result = 0
    enabled = True
    with open(args.input, "r") as f:
        for line in f.readlines():
            for instruction in re.findall(
                r"mul\(\d{1,3},\d{1,3}\)|do\(\)|don't\(\)", line
            ):
                if instruction == "do()":
                    enabled = True
                    continue
                if instruction == "don't()":
                    enabled = False
                if enabled:
                    numbers = [int(x) for x in re.findall(r"\d+", instruction)]
                    result += numbers[0] * numbers[1]
    print(f"Part 2: result = {result}")
