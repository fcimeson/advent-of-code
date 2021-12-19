#!/usr/bin/env python3

import re
import sys
import copy
import argparse

INF = float('inf')

class CustomList(list):
    def __str__(self):
        s = ''
        it = super().__iter__()
        while True:
            try:
                x = next(it)
                s += str(x)
            except StopIteration:
                break
        return s

def get_neighbours(environment, i, j):
    neighbours = []
    if i > 0:
        neighbours.append((i-1,j))
    if j > 0:
        neighbours.append((i,j-1))
    if i+1 < len(environment):
        neighbours.append((i+1,j))
    if j+1 < len(environment[0]):
        neighbours.append((i,j+1))
    return neighbours

if __name__ == "__main__":
    
    # Args
    parser = argparse.ArgumentParser(description='Advent of Code')
    parser.add_argument('input', help='input file')
    parser.add_argument('--days', type=int, default=80, help='length of simulation')
    parser.add_argument('-d', '--debug', action='store_true', help='enable debug code')
    args = parser.parse_args()

    # Data
    width = None
    environment = []
    with open(args.input, 'r') as f:
        for line in f.readlines():
            if re.match(r'^\d+$', line):
                environment.append([int(x) for x in re.findall(r'\d', line)])
                if width == None:
                    width = len(environment[-1])
                assert len(environment[-1]) == width

    # Solve
    risk = 0
    low_points = []
    for i, row in enumerate(environment):
        for j, height in enumerate(row):
            point_is_low = True
            for a,b in get_neighbours(environment, i, j):
                if environment[a][b] <= height:
                    point_is_low = False
                    break
            if point_is_low:
                low_points.append((i,j))
                risk += height + 1
                
                if args.debug:
                    print(f"Found low point: {(i,j)} with risk {height+1}")

    print(f"The total risk is {risk}")
