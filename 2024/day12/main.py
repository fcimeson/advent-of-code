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

    def plant(self):
        global map, N, M
        if 0 <= self.i < N and 0 <= self.j < M:
            return map[self.i][self.j]
        return None

    def move(self, direction, increment=1, inside_map=True):
        global N, M
        if self.i is None or self.j is None or (inside_map and not (0 <= self.i < N and 0 <= self.j < M)):
            return None
        if direction == Direction.LEFT:
            if inside_map and self.j - increment < 0:
                return None
            return Coordinate(self.i, self.j - increment)
        if direction == Direction.RIGHT:
            if inside_map and self.j + increment >= M:
                return None
            return Coordinate(self.i, self.j + increment)
        if direction == Direction.UP:
            if inside_map and self.i - increment < 0:
                return None
            return Coordinate(self.i - increment, self.j)
        if direction == Direction.DOWN:
            if inside_map and self.i + increment >= N:
                return None
            return Coordinate(self.i + increment, self.j)
        return None


def get_region(start):
    global map
    queue = [start]
    region = set()
    while len(queue) > 0:
        location = queue.pop()
        region.add(location)
        for next in [
            location.move(direction)
            for direction in [
                Direction.UP,
                Direction.DOWN,
                Direction.LEFT,
                Direction.RIGHT,
            ]
        ]:
            if next is not None and next not in region and next.plant() == start.plant():
                queue.append(next)
    return sorted(list(region))


def get_area(region):
    return len(region)


def get_perimeter(region):
    global map
    perimeter = 0
    for location in region:
        for adjacent in [
            location.move(direction)
            for direction in [
                Direction.UP,
                Direction.DOWN,
                Direction.LEFT,
                Direction.RIGHT,
            ]
        ]:
            if adjacent is None or adjacent.plant() != location.plant():
                perimeter += 1
    return perimeter


def get_number_of_sides(region):
    num_sides = 0
    fenced = {}
    for adjacent_direction in [
        Direction.UP,
        Direction.DOWN,
        Direction.LEFT,
        Direction.RIGHT,
    ]:
        for location in sorted(region):
            if location.move(adjacent_direction, inside_map=False).plant() == location.plant():
                continue
            if location not in fenced:
                fenced[location] = set()
            if adjacent_direction in fenced[location]:
                continue
            fenced[location].add(adjacent_direction)
            num_sides += 1

            fence_directions = (
                [Direction.LEFT, Direction.RIGHT]
                if adjacent_direction in [Direction.UP, Direction.DOWN]
                else [Direction.UP, Direction.DOWN]
            )
            for fence_direction in fence_directions:
                next = location
                while True:
                    next = next.move(fence_direction, inside_map=False)
                    if next.plant() != location.plant():
                        break
                    if next.move(adjacent_direction, inside_map=False).plant() == location.plant():
                        break
                    if next not in fenced:
                        fenced[next] = set()
                    assert (
                        adjacent_direction not in fenced[next]
                    ), f"next = {next}, adjacent_direction = {adjacent_direction}"
                    fenced[next].add(adjacent_direction)
    return num_sides


def get_regions():
    global N, M
    regions = []
    for i in range(N):
        for j in range(M):
            mapped = False
            location = Coordinate(i, j)
            for region in regions:
                if location in region:
                    mapped = True
                    break
            if not mapped:
                regions.append(get_region(location))
    return regions


def map_to_str(map):
    N = len(map)
    M = len(map[0])
    s = ""
    for i in range(N):
        for j in range(M):
            s += str(map[i][j])
        s += "\n"
    return s


def region_to_str(region):
    global map, N, M
    s = ""
    for i in range(N):
        for j in range(M):
            l = Coordinate(i, j)
            if l in region:
                s += map[i][j]
            else:
                s += "."
        s += "\n"
    return s


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
    regions = get_regions()

    # Part 1
    result = 0
    for region in regions:
        area = get_area(region)
        perimeter = get_perimeter(region)
        result += area * perimeter
        if args.debug:
            print(f"area = {area}, perimeter = {perimeter}")
            print(region_to_str(region))

    print(f"Part 1: result = {result}")

    # Part 2
    result = 0
    for region in regions:
        area = get_area(region)
        sides = get_number_of_sides(region)
        result += area * sides
        if args.debug:
            print(f"area = {area}, sides = {sides}")
            print(region_to_str(region))

    print(f"Part 2: result = {result}")
