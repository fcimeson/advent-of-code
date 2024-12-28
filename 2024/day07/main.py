#!/usr/bin/env python3

import re
import sys
import copy
import math
import enum
import numpy
import pickle
import argparse


def concatenate(x, y):
    return int(str(x) + str(y))


def is_feasible_01(result, test_inputs, test_output):
    if len(test_inputs) == 0:
        return result == test_output
    if is_feasible_01(result + test_inputs[0], test_inputs[1:], test_output):
        return True
    if is_feasible_01(result * test_inputs[0], test_inputs[1:], test_output):
        return True
    return False


def is_feasible_02(result, test_inputs, test_output):
    if len(test_inputs) == 0:
        return result == test_output
    if is_feasible_02(result + test_inputs[0], test_inputs[1:], test_output):
        return True
    if is_feasible_02(result * test_inputs[0], test_inputs[1:], test_output):
        return True
    if is_feasible_02(
        concatenate(result, test_inputs[0]), test_inputs[1:], test_output
    ):
        return True
    return False


if __name__ == "__main__":

    # Args
    parser = argparse.ArgumentParser(description="Advent of Code")
    parser.add_argument("input", help="input file")
    parser.add_argument("-d", "--debug", action="store_true")
    args = parser.parse_args()

    test_inputs = []
    test_outputs = []
    with open(args.input, "r") as f:
        for line in f.readlines():
            values = [int(x) for x in re.findall(r"\d+", line)]
            test_inputs.append(values[1:])
            test_outputs.append(values[0])
    N = len(test_outputs)

    # Part 1
    result = 0
    for i in range(N):
        if is_feasible_01(0, test_inputs[i], test_outputs[i]):
            result += test_outputs[i]

    print(f"Part 1: result = {result}")

    # Part 2
    result = 0
    for i in range(N):
        if is_feasible_02(0, test_inputs[i], test_outputs[i]):
            result += test_outputs[i]

    print(f"Part 2: result = {result}")
