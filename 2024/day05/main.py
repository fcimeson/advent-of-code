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


def print_filtered(word_search, used):
    for i, line in enumerate(word_search):
        filtered_line = ""
        for j, c in enumerate(line):
            filtered_line += c if used[i][j] else "."
        print(filtered_line)


def is_valid(update, rules):
    printed = set()
    for page in update:
        for rule in rules:
            if page == rule[0] and rule[1] in printed:
                return False
        printed.add(page)
    return True


if __name__ == "__main__":

    # Args
    parser = argparse.ArgumentParser(description="Advent of Code")
    parser.add_argument("input", help="input file")
    parser.add_argument("-d", "--debug", action="store_true")
    args = parser.parse_args()

    rules = []
    updates = []
    with open(args.input, "r") as f:
        for line in f.readlines():
            if re.match(r"^\d+\|\d+$", line):
                rules.append([int(x) for x in re.findall(r"\d+", line)])
            elif re.match(r"^[\d,]+$", line):
                updates.append([int(x) for x in re.findall(r"\d+", line)])

    # Part 1
    sum = 0
    invalid_updates = []
    for update in updates:
        if is_valid(update, rules):
            sum += update[len(update) // 2]
            if args.debug:
                print(f"Update ({update}) is valid")
        else:
            invalid_updates.append(update)

    print(f"Part 1: sum = {sum}")

    # Part 2
    sum = 0
    for update in invalid_updates:
        if args.debug:
            print(f"Invalid update: {update}")
        while not is_valid(update, rules):
            visited = set()
            changed = False
            for i, page in enumerate(update):
                for rule in rules:
                    if page == rule[0] and rule[1] in visited:
                        update.pop(i)
                        update.insert(i - 1, page)
                        changed = True
                        break
                if changed:
                    break
                visited.add(page)
        sum += update[len(update) // 2]
        if args.debug:
            print(f"Re-ordered update = {update}")

    print(f"Part 2: sum = {sum}")
