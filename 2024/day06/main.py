#!/usr/bin/env python3

import re
import sys
import copy
import math
import enum
import numpy
import pickle
import argparse


class Direction(enum.Enum):
    UP = enum.auto()
    DOWN = enum.auto()
    LEFT = enum.auto()
    RIGHT = enum.auto()


def get_direction(map, i, j):
    if map[i][j] == "^":
        return Direction.UP
    if map[i][j] == "v":
        return Direction.DOWN
    if map[i][j] == "<":
        return Direction.LEFT
    if map[i][j] == ">":
        return Direction.RIGHT
    return None


def rotate(direction):
    if direction == Direction.UP:
        return Direction.RIGHT
    if direction == Direction.RIGHT:
        return Direction.DOWN
    if direction == Direction.DOWN:
        return Direction.LEFT
    if direction == Direction.LEFT:
        return Direction.UP
    return None


def find_starting_point(map):
    for i, row in enumerate(map):
        for j, location in enumerate(row):
            if get_direction(map, i, j):
                return i, j


def print_visited(map, visited):
    for i, row in enumerate(map):
        s = ""
        for j, c in enumerate(row):
            s += "X" if visited[i][j] else c
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
            map.append(line.strip())
    N = len(map)
    M = len(map[0])

    def move_from(i, j, direction):
        if i is None or j is None or not (0 <= i < N) or not (0 <= j < M):
            return None, None
        if direction == Direction.LEFT and j > 0:
            return i, j - 1
        if direction == Direction.RIGHT and j + 1 < M:
            return i, j + 1
        if direction == Direction.UP and i > 0:
            return i - 1, j
        if direction == Direction.DOWN and i + 1 < N:
            return i + 1, j
        return None, None

    # Part 1
    i, j = find_starting_point(map)
    direction = get_direction(map, i, j)

    visited = [[False] * M for _ in range(N)]
    while i is not None and j is not None:
        visited[i][j] = True
        if args.debug:
            print_visited(map, visited)
        while True:
            next_i, next_j = move_from(i, j, direction)
            if next_i is not None and next_j is not None and map[next_i][next_j] == "#":
                direction = rotate(direction)
            else:
                break
        i, j = next_i, next_j

    result = sum(sum(visited, []))
    print(f"Part 1: result = {result}")
