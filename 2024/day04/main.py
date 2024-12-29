#!/usr/bin/env python3

import re
import sys
import copy
import math
import enum
import numpy
import pickle
import argparse

INF = float("inf")
RE_NUMBER = r"-?\d+"


def print_filtered(word_search, used):
    for i, line in enumerate(word_search):
        filtered_line = ""
        for j, c in enumerate(line):
            filtered_line += c if used[i][j] else "."
        print(filtered_line)


if __name__ == "__main__":

    # Args
    parser = argparse.ArgumentParser(description="Advent of Code")
    parser.add_argument("input", help="input file")
    parser.add_argument("-d", "--debug", action="store_true")
    args = parser.parse_args()

    word_search = []
    with open(args.input, "r") as f:
        for line in f.readlines():
            line = line.strip()
            word_search.append(line)

    N, M = len(word_search), len(word_search[0])

    class Direction(enum.Enum):
        LEFT = enum.auto()
        RIGHT = enum.auto()
        UP = enum.auto()
        DOWN = enum.auto()
        LEFT_AND_UP = enum.auto()
        LEFT_AND_DOWN = enum.auto()
        RIGHT_AND_UP = enum.auto()
        RIGHT_AND_DOWN = enum.auto()

    def move_from(i, j, direction, increment=1):
        if i is None or j is None or not (0 <= i < N) or not (0 <= j < M):
            return None, None
        if direction == Direction.LEFT and j - increment >= 0:
            return i, j - increment
        if direction == Direction.RIGHT and j + increment < M:
            return i, j + increment
        if direction == Direction.UP and i - increment >= 0:
            return i - increment, j
        if direction == Direction.DOWN and i + increment < N:
            return i + increment, j
        if direction == Direction.LEFT_AND_UP:
            return move_from(*move_from(i, j, Direction.LEFT), Direction.UP, increment=increment)
        if direction == Direction.LEFT_AND_DOWN:
            return move_from(*move_from(i, j, Direction.LEFT), Direction.DOWN, increment=increment)
        if direction == Direction.RIGHT_AND_UP:
            return move_from(*move_from(i, j, Direction.RIGHT), Direction.UP, increment=increment)
        if direction == Direction.RIGHT_AND_DOWN:
            return move_from(*move_from(i, j, Direction.RIGHT), Direction.DOWN, increment=increment)
        return None, None

    starting_points = {}
    starting_points[Direction.LEFT] = set([(i, M - 1) for i in range(N)])
    starting_points[Direction.RIGHT] = set([(i, 0) for i in range(N)])
    starting_points[Direction.UP] = set([(N - 1, j) for j in range(M)])
    starting_points[Direction.DOWN] = set([(0, j) for j in range(M)])
    starting_points[Direction.LEFT_AND_UP] = starting_points[Direction.LEFT] | starting_points[Direction.UP]
    starting_points[Direction.LEFT_AND_DOWN] = starting_points[Direction.LEFT] | starting_points[Direction.DOWN]
    starting_points[Direction.RIGHT_AND_UP] = starting_points[Direction.RIGHT] | starting_points[Direction.UP]
    starting_points[Direction.RIGHT_AND_DOWN] = starting_points[Direction.RIGHT] | starting_points[Direction.DOWN]

    # Part 1
    count = 0
    used = [[False] * len(line) for line in word_search]
    for direction in [
        Direction.LEFT,
        Direction.RIGHT,
        Direction.UP,
        Direction.DOWN,
        Direction.LEFT_AND_UP,
        Direction.LEFT_AND_DOWN,
        Direction.RIGHT_AND_DOWN,
        Direction.RIGHT_AND_UP,
    ]:
        for i0, j0 in starting_points[direction]:
            line = ""
            i, j = i0, j0
            while i is not None and j is not None:
                line += word_search[i][j]
                i, j = move_from(i, j, direction)
            for match in re.finditer("XMAS", line):
                i, j = i0, j0
                for _ in range(match.start()):
                    i, j = move_from(i, j, direction)
                for _ in range(4):
                    used[i][j] |= True
                    i, j = move_from(i, j, direction)
                count += 1

    if args.debug:
        print_filtered(word_search, used)
    print(f"Part 1: count = {count}")

    # Part 2
    used = [[False] * len(line) for line in word_search]
    for direction in [
        Direction.LEFT_AND_UP,
        Direction.LEFT_AND_DOWN,
        Direction.RIGHT_AND_DOWN,
        Direction.RIGHT_AND_UP,
    ]:
        for i0, j0 in starting_points[direction]:
            line = ""
            i, j = i0, j0
            while i is not None and j is not None:
                line += word_search[i][j]
                i, j = move_from(i, j, direction)
            for match in re.finditer("MAS", line):
                i, j = i0, j0
                for _ in range(match.start()):
                    i, j = move_from(i, j, direction)
                for _ in range(3):
                    used[i][j] |= True
                    i, j = move_from(i, j, direction)

    count = 0
    for i in range(N):
        for j in range(M):
            if used[i][j] and word_search[i][j] == "A":
                i01, j01 = move_from(i, j, Direction.LEFT_AND_DOWN)
                i02, j02 = move_from(i, j, Direction.RIGHT_AND_UP)
                if i01 is None or i02 is None or j01 is None or j02 is None:
                    continue
                candiate = word_search[i01][j01] + "A" + word_search[i02][j02]
                if candiate not in ["MAS", "SAM"]:
                    continue
                i01, j01 = move_from(i, j, Direction.RIGHT_AND_DOWN)
                i02, j02 = move_from(i, j, Direction.LEFT_AND_UP)
                if i01 is None or i02 is None or j01 is None or j02 is None:
                    continue
                candiate = word_search[i01][j01] + "A" + word_search[i02][j02]
                if candiate not in ["MAS", "SAM"]:
                    continue
                count += 1

    if args.debug:
        print_filtered(word_search, used)
    print(f"Part 2: count = {count}")
