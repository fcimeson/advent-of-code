#!/usr/bin/env python3

import re
import sys
import copy
import math
import enum
import numpy
import pickle
import argparse


class Coordinate:
    def __init__(self, i, j):
        self.i = i
        self.j = j

    def __str__(self):
        return f"({self.i},{self.j})"

    def __add__(self, other):
        return Coordinate(self.i + other.i, self.j + other.j)

    def __sub__(self, other):
        return Coordinate(self.i - other.i, self.j - other.j)

    def __mul__(self, scalar):
        if isinstance(scalar, (int, float)):
            return Coordinate(scalar * self.i, scalar * self.j)
        return NotImplemented

    def __rmul__(self, scalar):
        return self.__mul__(scalar)


def print_map(map, anti_nodes):
    N = len(map)
    M = len(map[0])
    for i in range(N):
        s = ""
        for j in range(M):
            c = "#" if anti_nodes[i][j] else "."
            if map[i][j] != ".":
                c = map[i][j]
            s += c
        print(s)


if __name__ == "__main__":

    # Args
    parser = argparse.ArgumentParser(description="Advent of Code")
    parser.add_argument("input", help="input file")
    parser.add_argument("-d", "--debug", action="store_true")
    args = parser.parse_args()

    map = []
    with open(args.input, "r") as f:
        for line in f.readlines():
            map.append(list(line.strip()))
    N = len(map)
    M = len(map[0])

    antennas = {}
    for i, row in enumerate(map):
        for j, v in enumerate(row):
            if v != ".":
                if v not in antennas:
                    antennas[v] = []
                antennas[v].append(Coordinate(i, j))

    # Part 1
    anti_nodes = [[False] * M for _ in range(N)]
    for frequency, locations in antennas.items():
        for location_01 in locations:
            for location_02 in locations:
                if location_01 != location_02:
                    delta = location_02 - location_01
                    for anti_node in [location_01 - delta, location_02 + delta]:
                        if 0 <= anti_node.i < N and 0 <= anti_node.j < M:
                            anti_nodes[anti_node.i][anti_node.j] = True
    if args.debug:
        print_map(map, anti_nodes)

    result = sum(sum(row) for row in anti_nodes)
    print(f"Part 1: result = {result}")

    # Part 2
    anti_nodes = [[False] * M for _ in range(N)]
    for frequency, locations in antennas.items():
        for location_01 in locations:
            for location_02 in locations:
                if location_01 != location_02:
                    delta = location_02 - location_01
                    candidate_location = location_01
                    while 0 <= candidate_location.i < N and 0 <= candidate_location.j < M:
                        anti_nodes[candidate_location.i][candidate_location.j] = True
                        candidate_location -= delta
                    candidate_location = location_02
                    while 0 <= candidate_location.i < N and 0 <= candidate_location.j < M:
                        anti_nodes[candidate_location.i][candidate_location.j] = True
                        candidate_location += delta
    if args.debug:
        print_map(map, anti_nodes)

    result = sum(sum(row) for row in anti_nodes)
    print(f"Part 2: result = {result}")
