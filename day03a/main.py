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
        ones = []
        number_of_lines = 0
        for line in f.readlines():
            if re.match(r'^\s*[01]+\s*$', line):
                for i, x in enumerate(re.findall(r'[01]', line)):
                    while i >= len(ones):
                        ones.append(0)
                    if x == '1':
                        ones[i] += 1
                number_of_lines += 1
        gamma = epsilon = ''
        for i, count in enumerate(ones):
            if count >= number_of_lines // 2:
                gamma += '1'
                epsilon += '0'
            else:
                gamma += '0'
                epsilon += '1'
        gamma = int(gamma, 2)
        epsilon = int(epsilon, 2)
        print(f'Gamma = {gamma}, Epsilon = {epsilon}, Power = {gamma*epsilon}')
