#!/usr/bin/env python3

import re
import sys
import argparse

class CustomList(list):
    def __init__(self, size):
        super().__init__([0]*size)
        
    def __str__(self):
        return super().__str__().strip('[').rstrip(']')

if __name__ == "__main__":
    
    # Args
    parser = argparse.ArgumentParser(description='Advent of Code')
    parser.add_argument('input', help='input file')
    parser.add_argument('--days', type=int, default=256, help='length of simulation')
    parser.add_argument('-d', '--debug', action='store_true', help='enable debug code')
    args = parser.parse_args()

    # Data
    MAX_AGE = 9
    fish_age_matrix = CustomList(MAX_AGE)
    with open(args.input, 'r') as f:
        for line in f.readlines():
            if re.match(r'^[\s\d,]+$', line):
                for age in re.findall(r'\d+', line):
                    fish_age_matrix[int(age)] += 1

    # Simulate
    if args.debug:
        print(f"After 0 days: {fish_age_matrix}")
    for day in range(1, args.days+1):
        new_fish_age_matrix = CustomList(MAX_AGE)
        for age, num_fish in enumerate(fish_age_matrix):
            if age == 0:
                new_fish_age_matrix[6] += num_fish
                new_fish_age_matrix[8] += num_fish
            else:
                new_fish_age_matrix[age-1] += num_fish
        fish_age_matrix = new_fish_age_matrix
        if args.debug:
            print(f"After {day} days: {fish_age_matrix}")
    print(f"Number of fish = {sum(fish_age_matrix)}")
        