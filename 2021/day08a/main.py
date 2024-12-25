#!/usr/bin/env python3

import re
import sys
import argparse

INF = float("inf")
RE_DIGIT = r"[abcdefg]{1,7}"


class CustomList(list):
    def __init__(self, size):
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
    data = []
    input_rx = r"^(\s*%s\s{1,}){10}\|(\s{1,}%s\s*){4}$" % (RE_DIGIT, RE_DIGIT)
    with open(args.input, "r") as f:
        for line in f.readlines():
            if re.match(input_rx, line):
                s = line.split("|")
                data.append(
                    {
                        "signals": re.findall(RE_DIGIT, s[0]),
                        "output": re.findall(RE_DIGIT, s[1]),
                    }
                )
            else:
                raise ValueError(f"Incorrectly formated input: {line}")

    # Solve
    number_of_digits = CustomList(10)
    for x in data:
        s = ""
        for digit in x["output"]:
            prev_total = sum(number_of_digits)
            if len(digit) == 2:
                number_of_digits[1] += 1
            elif len(digit) == 4:
                number_of_digits[4] += 1
            elif len(digit) == 3:
                number_of_digits[7] += 1
            elif len(digit) == 7:
                number_of_digits[8] += 1
            if args.debug and prev_total != sum(number_of_digits):
                s += digit + " "
        if args.debug:
            print(s)
    print(
        f"The number of 1s, 4s, 7s, and 8s is {number_of_digits[1]}, {number_of_digits[4]}, {number_of_digits[7]}, {number_of_digits[8]} respectively ({number_of_digits[1] + number_of_digits[4] + number_of_digits[7] + number_of_digits[8]} in total)"
    )
