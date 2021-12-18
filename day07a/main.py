#!/usr/bin/env python3

import re
import sys
import argparse

INF = float('inf')

if __name__ == "__main__":
    
    # Args
    parser = argparse.ArgumentParser(description='Advent of Code')
    parser.add_argument('input', help='input file')
    parser.add_argument('--days', type=int, default=80, help='length of simulation')
    parser.add_argument('-d', '--debug', action='store_true', help='enable debug code')
    args = parser.parse_args()

    # Data
    crabs = []
    with open(args.input, 'r') as f:
        for line in f.readlines():
            if re.match(r'^[\s\d,]+$', line):
                crabs.extend([int(x) for x in re.findall(r'\d+', line)])

    # Solve
    min_pos = min(crabs)
    max_position = max(crabs)
    solution = {'position':None, 'cost':INF}
    for target_position in range(min_pos, max_position+1):
        cost = 0
        for crab_position in crabs:
            cost += abs(target_position-crab_position)
        if cost < solution['cost']:
            solution['position'] = target_position
            solution['cost'] = cost
            if args.debug:
                print(f"Found new solution at {solution['position']} of {solution['cost']} cost")
    print(f"The optimal solution is at {solution['position']} and spends {solution['cost']} fuel")
