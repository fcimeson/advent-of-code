#!/usr/bin/env python3

import re
import argparse

if __name__ == '__main__':

    # Args
    parser = argparse.ArgumentParser(description='Advent of Code')
    parser.add_argument('input', help='input file')
    parser.add_argument('-d', '--debug', action='store_true', help='enable debug code')
    args = parser.parse_args()

    # Solve
    with open(args.input, 'r') as f:
        total = 0
        prev = None
        for line in f.readlines():
            if re.match(r'^\s*\d+\s*$', line):
                new = int(line)
                if prev is not None and new > prev:
                    total += 1
                prev = new
        print(f'There are {total} measurements larger than the previous measurements.')
