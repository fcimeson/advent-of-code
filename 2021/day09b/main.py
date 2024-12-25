#!/usr/bin/env python3

import re
import sys
import copy
import argparse

INF = float("inf")


class CustomList(list):
    def __str__(self):
        s = ""
        it = super().__iter__()
        while True:
            try:
                x = next(it)
                s += str(x)
            except StopIteration:
                break
        return s


def get_neighbours(environment, point):
    neighbours = []
    i, j = point
    if i > 0:
        neighbours.append((i - 1, j))
    if j > 0:
        neighbours.append((i, j - 1))
    if i + 1 < len(environment):
        neighbours.append((i + 1, j))
    if j + 1 < len(environment[0]):
        neighbours.append((i, j + 1))
    return neighbours


def get_basin(environment, point, basin=None):
    if basin is None:
        basin = set()
    i, j = point
    if environment[i][j] < 9:
        basin.add(point)
    for neighbour in get_neighbours(environment, point):
        a, b = neighbour
        if environment[a][b] < 9:
            if neighbour not in basin:
                get_basin(environment, neighbour, basin)
    return basin


def print_basin(environment, basin):
    s = ""
    for i, row in enumerate(environment):
        for j, height in enumerate(row):
            if (i, j) in basin:
                s += str(height)
            else:
                s += "."
        s += "\n"
    print(s)


if __name__ == "__main__":

    # Args
    parser = argparse.ArgumentParser(description="Advent of Code")
    parser.add_argument("input", help="input file")
    parser.add_argument("--days", type=int, default=80, help="length of simulation")
    parser.add_argument("-d", "--debug", action="store_true", help="enable debug code")
    args = parser.parse_args()

    # Data
    width = None
    environment = []
    with open(args.input, "r") as f:
        for line in f.readlines():
            if re.match(r"^\d+$", line):
                environment.append([int(x) for x in re.findall(r"\d", line)])
                if width == None:
                    width = len(environment[-1])
                assert len(environment[-1]) == width

    # Solve
    basins = []
    for i, row in enumerate(environment):
        for j, height in enumerate(row):
            if height < 9:
                covered = False
                for basin in basins:
                    if (i, j) in basin:
                        covered = True
                        continue
                if covered:
                    continue

                basins.append(get_basin(environment, (i, j)))
                if args.debug:
                    print(f"Found a new basin:")
                    print_basin(environment, basins[-1])

    largest_basins = sorted(basins, key=len, reverse=True)[:3]
    if args.debug:
        print("Largest Basins:")
        for basin in largest_basins:
            print_basin(environment, basin)

    solution = 1
    for basin in largest_basins:
        solution *= len(basin)
    print(f"The solution is {solution}")
