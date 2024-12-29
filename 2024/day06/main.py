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


def print_map(map):
    for i, row in enumerate(map):
        s = ""
        for j, c in enumerate(row):
            s += c
        print(s)


def print_visited(map, visited):
    for i, row in enumerate(map):
        s = ""
        for j, c in enumerate(row):
            if isinstance(visited[i][j], bool):
                s += "X" if visited[i][j] else c
            else:
                assert isinstance(visited[i][j], set), f"type = {type(visited[i][j])}, visited = {visited[i][j]}"
                if len(visited[i][j]) == 0:
                    s += c
                elif len(visited[i][j]) == 1:
                    if Direction.UP in visited[i][j] or Direction.DOWN in visited[i][j]:
                        s += "|"
                    elif Direction.LEFT in visited[i][j] or Direction.RIGHT in visited[i][j]:
                        s += "-"
                    else:
                        assert False, f"type = {type(visited[i][j])}, visited = {visited[i][j]}"
                elif len(visited[i][j]) == 2:
                    if Direction.UP in visited[i][j] and Direction.DOWN in visited[i][j]:
                        s += "|"
                    elif Direction.LEFT in visited[i][j] and Direction.RIGHT in visited[i][j]:
                        s += "-"
                    else:
                        s += "+"
                else:
                    s += "+"
        print(s)


def has_loop(map, debug=False):
    N = len(map)
    M = len(map[0])
    i, j = find_starting_point(map)
    direction = get_direction(map, i, j)
    visited = [[set() for _ in range(M)] for _ in range(N)]
    while i is not None and j is not None:
        if direction in visited[i][j]:
            if debug:
                print("Found loop in:")
                print_visited(map, visited)
                print("\n")
            return True
        visited[i][j].add(direction)
        while True:
            next_i, next_j = move_from(i, j, direction)
            if next_i is not None and next_j is not None and map[next_i][next_j] in ["#", "O"]:
                direction = rotate(direction)
            else:
                break
        i, j = next_i, next_j
    if debug:
        print("No loop in:")
        print_visited(map, visited)
        print("\n")
    return False


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
        while True:
            next_i, next_j = move_from(i, j, direction)
            if next_i is not None and next_j is not None and map[next_i][next_j] == "#":
                direction = rotate(direction)
            else:
                break
        i, j = next_i, next_j

    if args.debug:
        print_visited(map, visited)
        print("\n")
    result = sum(sum(visited, []))
    print(f"Part 1: result = {result}")

    # Part 2
    count = 0
    i00, j00 = find_starting_point(map)
    for i01 in range(N):
        for j01 in range(M):
            if not (i01 == i00 and j01 == j00) and visited[i01][j01]:
                new_map = copy.deepcopy(map)
                new_map[i01][j01] = "O"
                if has_loop(new_map, args.debug):
                    count += 1
    print(f"Part 2: count = {count}")
