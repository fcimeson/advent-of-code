#!/usr/bin/env python3

import re
import copy
import argparse


def filter(data, index, msb=True, debug=False):
    ones_count = zeros_count = 0
    for x in data:
        assert isinstance(index, int) and index < len(x)
        ones_count += x[index] == "1"
    zeros_count = len(data) - ones_count
    ms_char = "1" if ones_count >= zeros_count else "0"
    if msb:
        match_char = ms_char
    else:
        if ms_char == "1":
            match_char = "0"
        else:
            match_char = "1"
    output = [x for x in data if x[index] == match_char]
    if debug:
        print(
            f"filter: index = {index}, ones = {ones_count}/{len(data)}, match = {match_char}, output = {output}"
        )
    return output


if __name__ == "__main__":

    # Args
    parser = argparse.ArgumentParser(description="Advent of Code")
    parser.add_argument("input", help="input file")
    parser.add_argument("-d", "--debug", action="store_true", help="enable debug code")
    args = parser.parse_args()

    # Data
    with open(args.input, "r") as f:
        # Get input data
        data00 = []
        for line in f.readlines():
            if re.match(r"^\s*[01]+\s*$", line):
                data00.append(line.strip())

    # Oxygen
    index = 0
    data01 = copy.copy(data00)
    while len(data01) > 1:
        data01 = filter(data01, index, msb=True)
        index += 1
    oxygen = int(data01[0], 2)

    # CO2
    index = 0
    data02 = copy.copy(data00)
    while len(data02) > 1:
        data02 = filter(data02, index, msb=False, debug=args.debug)
        index += 1
    co2 = int(data02[0], 2)

    # Output
    print(f"Oxygen = {oxygen}, CO2 = {co2}, Product = {oxygen*co2}")
