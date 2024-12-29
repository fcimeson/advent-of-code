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

    list_01 = []
    list_02 = []
    frequency_02 = {}
    with open(args.input, "r") as f:
        for line in f.readlines():
            if re.match(r"^\d+\s+\d+\s*$", line):
                numbers = re.findall(r"\d+", line)
                list_01.append(int(numbers[0]))
                list_02.append(int(numbers[1]))

                x = list_01[-1]
                if x not in frequency_02:
                    frequency_02[x] = 0

                x = list_02[-1]
                if x not in frequency_02:
                    frequency_02[x] = 0
                frequency_02[x] += 1

    list_01 = sorted(list_01)
    list_02 = sorted(list_02)

    edit_distance_01 = 0
    edit_distance_02 = 0
    for i in range(len(list_01)):
        edit_distance_01 += abs(list_02[i] - list_01[i])
        edit_distance_02 += list_01[i] * frequency_02[list_01[i]]

    print(f"List edit distance 01 = {edit_distance_01}, edit distance 02 = {edit_distance_02}.")
