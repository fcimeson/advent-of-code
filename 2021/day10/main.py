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

    # Part 1
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
                            print(f"{line} - Expected {expected}, but found {char} instead.")
                        illegals[char] += 1
                        break

    # Calculate
    points = illegals[")"] * 3 + illegals["]"] * 57 + illegals["}"] * 1197 + illegals[">"] * 25137
    print(f"Part 1: total syntax score is {points}")

    # Part 2
    total = 0
    scores = []
    score_map = {")": 1, "]": 2, "}": 3, ">": 4}
    autocompletes = {")": 0, "]": 0, "}": 0, ">": 0}
    end_bracket_map = {"(": ")", "[": "]", "{": "}", "<": ">"}
    with open(args.input, "r") as f:
        for line in f.readlines():
            score = 0
            line = line.strip()
            if re.match(r"^[\(\[{<\)\]}>]+$", line):
                stack = []
                corrupted = False
                for char in list(line):
                    if char in "([{<":
                        stack.append(char)
                        continue

                    expected = end_bracket_map[stack[-1]]
                    if char == expected:
                        stack.pop()
                    else:
                        corrupted = True
                        break
                missing = ""
                while not corrupted and len(stack) > 0:
                    char = stack.pop()
                    assert char in "([{<"
                    bracket = end_bracket_map[char]
                    missing += bracket
                    autocompletes[bracket] += 1
                    score = score * 5 + score_map[bracket]
                if len(missing) > 0:
                    if args.debug:
                        print(f"{line} - Completed by adding {missing}, score = {score}.")
                    scores.append(score)
                    total += score

    # Calculate
    scores = sorted(scores)
    print(f"Part 2: total syntax score is {total} and the middle score is {scores[len(scores)//2]}.")
