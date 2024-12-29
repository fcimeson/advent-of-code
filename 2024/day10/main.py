#!/usr/bin/env python3

import re
import sys
import copy
import math
import enum
import numpy
import pickle
import argparse

# Globals
N = None
M = None
map = None


class Direction(enum.Enum):
    LEFT = enum.auto()
    RIGHT = enum.auto()
    UP = enum.auto()
    DOWN = enum.auto()


class Coordinate:
    def __init__(self, i, j):
        self.i = i
        self.j = j

    def __hash__(self):
        return hash(self.__str__())

    def __str__(self):
        return f"({self.i},{self.j})"

    def __eq__(self, other):
        return self.i == other.i and self.j == other.j

    def __lt__(self, other):
        if self.i < other.i:
            return True
        if self.i <= other.i and self.j < other.j:
            return True
        return False

    def elevation(self):
        global map
        return map[self.i][self.j]

    def move(self, direction, increment=1):
        global N, M
        if (
            self.i is None
            or self.j is None
            or not (0 <= self.i < N)
            or not (0 <= self.j < M)
        ):
            return None
        if direction == Direction.LEFT and self.j - increment >= 0:
            return Coordinate(self.i, self.j - increment)
        if direction == Direction.RIGHT and self.j + increment < M:
            return Coordinate(self.i, self.j + increment)
        if direction == Direction.UP and self.i - increment >= 0:
            return Coordinate(self.i - increment, self.j)
        if direction == Direction.DOWN and self.i + increment < N:
            return Coordinate(self.i + increment, self.j)
        return None


def get_trailhead_score(trails):
    end_points = set()
    for trail in trails:
        end_points.add(trail[-1])
    return len(end_points)


def map2str(map):
    N = len(map)
    M = len(map[0])
    s = ""
    for i in range(N):
        for j in range(M):
            s += str(map[i][j])
        s += "\n"
    return s


def trail2str(trail):
    global map, N, M

    s = ""
    for i in range(N):
        for j in range(M):
            if Coordinate(i, j) in trail:
                s += str(map[i][j])
            else:
                s += "."
        s += "\n"
    return s


def trails2str(trails):
    global map, N, M

    s = ""
    for i in range(N):
        for j in range(M):
            visited = False
            for trail in trails:
                if Coordinate(i, j) in trail:
                    visited = True
            s += str(map[i][j]) if visited else "."
        s += "\n"
    for trail in trails:
        for x in trail:
            s += f"{x}->"
        s = s.strip("->")
        s += "\n"
    return s


def get_trails(start):
    global map
    if start.elevation() == 9:
        return [[start]]
    trails = []
    for next in [
        start.move(direction)
        for direction in [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]
    ]:
        if next is None:
            continue
        if next.elevation() == start.elevation() + 1:
            for sub_trail in get_trails(next):
                trail = [start] + sub_trail
                if trail[-1].elevation() == 9:
                    trails.append(trail)
                    # print(trail2str(trail))
    return sorted(trails)


if __name__ == "__main__":

    # Args
    parser = argparse.ArgumentParser(description="Advent of Code")
    parser.add_argument("input", help="input file")
    parser.add_argument("-d", "--debug", action="store_true")
    args = parser.parse_args()

    map = []
    with open(args.input, "r") as f:
        for line in f.readlines():
            map.append([int(x) for x in line.strip()])
    N = len(map)
    M = len(map[0])

    starting_candidates = []
    for i, row in enumerate(map):
        for j, l in enumerate(row):
            if l == 0:
                starting_candidates.append(Coordinate(i, j))

    # Part 1
    result_01 = 0
    result_02 = 0
    for start in starting_candidates:
        trails = get_trails(start)
        score = get_trailhead_score(trails)
        rating = len(trails)
        result_01 += score
        result_02 += rating
        if args.debug:
            print(f"{trails2str(trails)}\nscore = {score}")

    print(f"Part 1: result = {result_01}")
    print(f"Part 2: result = {result_02}")
