#!/usr/bin/env python3

import re
import sys
import copy
import argparse

INF = float("inf")


class CustomList(list):
    def __str__(self):
        s = ""
        it = super().__iter__()
        while True:
            try:
                x = next(it)
                s += str(x)
            except StopIteration:
                break
        return s


if __name__ == "__main__":

    # Args
    parser = argparse.ArgumentParser(description="Advent of Code")
    parser.add_argument("input", help="input file")
    parser.add_argument("--days", type=int, default=80, help="length of simulation")
    parser.add_argument("-d", "--debug", action="store_true", help="enable debug code")
    args = parser.parse_args()

    # Data
    illegals = {")": 0, "]": 0, "}": 0, ">": 0}
    end_bracket_map = {"(": ")", "[": "]", "{": "}", "<": ">"}
    with open(args.input, "r") as f:
        for line in f.readlines():
            line = line.strip()
            if re.match(r"^[\(\[{<\)\]}>]+$", line):
                stack = []
                for char in list(line):
                    if char in "([{<":
                        stack.append(char)
                        continue

                    expected = end_bracket_map[stack[-1]]
                    if char == expected:
                        stack.pop()
                    else:
                        if args.debug:
                            print(
                                f"{line} - Expected {expected}, but found {char} instead."
                            )
                        illegals[char] += 1
                        break

    # Calculate
    points = (
        illegals[")"] * 3
        + illegals["]"] * 57
        + illegals["}"] * 1197
        + illegals[">"] * 25137
    )
    print(f"Total syntax score is {points}")
