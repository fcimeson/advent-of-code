#!/usr/bin/env python3

import enum
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
        if j + 1 < len(environment[0]):
            neighbours.append((i - 1, j + 1))
        if j > 0:
            neighbours.append((i - 1, j - 1))

    if i + 1 < len(environment):
        neighbours.append((i + 1, j))
        if j + 1 < len(environment[0]):
            neighbours.append((i + 1, j + 1))
        if j > 0:
            neighbours.append((i + 1, j - 1))

    if j > 0:
        neighbours.append((i, j - 1))

    if j + 1 < len(environment[0]):
        neighbours.append((i, j + 1))

    return neighbours


if __name__ == "__main__":

    # Args
    parser = argparse.ArgumentParser(description="Advent of Code")
    parser.add_argument("input", help="input file")
    parser.add_argument("--days", type=int, default=80, help="length of simulation")
    parser.add_argument("-d", "--debug", action="store_true", help="enable debug code")
    args = parser.parse_args()

    # Part 1
    N = 10
    environment = []
    with open(args.input, "r") as f:
        for line in f.readlines():
            if re.match(r"^\d+$", line):
                environment.append(
                    CustomList([int(x) for x in re.findall(r"\d", line)])
                )
                assert len(environment[-1]) == N
        assert len(environment) == N

    number_of_flashes = 0
    for step in range(1, 101):

        # Increase
        queue = [(i, j) for j in range(N) for i in range(N)]
        while len(queue) > 0:
            i, j = queue.pop()
            environment[i][j] += 1
            if environment[i][j] == 10:
                queue.extend(get_neighbours(environment, point=(i, j)))
                number_of_flashes += 1

        # Decrease
        for i, row in enumerate(environment):
            for j, energy in enumerate(row):
                if energy > 9:
                    environment[i][j] = 0

        # Debug
        if args.debug:
            print(f"After step {step}:")
            for row in environment:
                print(row)
            print()

    # Output
    print(f"Part 1: total number of flashes is {number_of_flashes}.")

    # Part 2
    N = 10
    environment = []
    with open(args.input, "r") as f:
        for line in f.readlines():
            if re.match(r"^\d+$", line):
                environment.append(
                    CustomList([int(x) for x in re.findall(r"\d", line)])
                )
                assert len(environment[-1]) == N
        assert len(environment) == N

    step = 1
    while True:

        # Increase
        number_of_flashes = 0
        queue = [(i, j) for j in range(N) for i in range(N)]
        while len(queue) > 0:
            i, j = queue.pop()
            environment[i][j] += 1
            if environment[i][j] == 10:
                queue.extend(get_neighbours(environment, point=(i, j)))
                number_of_flashes += 1

        # Decrease
        for i, row in enumerate(environment):
            for j, energy in enumerate(row):
                if energy > 9:
                    environment[i][j] = 0

        # Debug
        if args.debug:
            print(f"After step {step}:")
            for row in environment:
                print(row)
            print()

        if number_of_flashes == N * N:
            break
        step += 1

    # Output
    print(f"Part 2: the octopi syncronize after step {step}.")

