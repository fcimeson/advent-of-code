#!/usr/bin/env python3

import re
import argparse


class Line:

    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __str__(self):
        return f"{self.start[0]},{self.start[1]} -> {self.end[0]},{self.end[1]}"

    def is_horizontal(self):
        return self.start[1] == self.end[1]

    def is_vertical(self):
        return self.start[0] == self.end[0]

    def get_points(self):
        di = dj = 0
        if self.start[0] != self.end[0]:
            di = 1 if self.start[0] < self.end[0] else -1
        if self.start[1] != self.end[1]:
            dj = 1 if self.start[1] < self.end[1] else -1

        point = self.start
        points = [point]
        while point != self.end:
            point = (point[0] + di, point[1] + dj)
            points.append(point)
        return points


class Environment:

    def __init__(self):
        self.coverage = []
        self.num_rows = 0
        self.num_cols = 0

    def __str__(self):
        s = ""
        for row in self.coverage:
            for x in row:
                if x == 0:
                    s += "."
                else:
                    s += str(x)
            s += "\n"
        return s

    def update_size(self):
        while self.num_rows > len(self.coverage):
            self.coverage.append([0] * self.num_cols)
        for row in self.coverage:
            diff = self.num_cols - len(row)
            if diff > 0:
                row.extend([0] * diff)

    def add(self, i, j):
        if i + 1 > self.num_rows or j + 1 > self.num_cols:
            self.num_rows = max(self.num_rows, i + 1)
            self.num_cols = max(self.num_cols, j + 1)
            self.update_size()
        self.coverage[i][j] += 1

    def count(self, gt_value=1):
        count = 0
        for row in self.coverage:
            for x in row:
                if x > gt_value:
                    count += 1
        return count


if __name__ == "__main__":

    # Args
    parser = argparse.ArgumentParser(description="Advent of Code")
    parser.add_argument("input", help="input file")
    parser.add_argument("-d", "--debug", action="store_true", help="enable debug code")
    args = parser.parse_args()

    # Data
    with open(args.input, "r") as f:
        lines = []
        for line in f.readlines():
            if re.match(r"^\s*\d+,\d+\s*->\s*\d+,\d+\s*$", line):
                points = [int(x) for x in re.findall(r"\d+", line)]
                lines.append(Line((points[1], points[0]), (points[3], points[2])))

    # Part 1
    environment = Environment()
    for line in lines:
        if line.is_horizontal() or line.is_vertical():
            for i, j in line.get_points():
                environment.add(i, j)
    if args.debug:
        print(environment)
    print(f"Part 1: count = {environment.count()}")

    # Part 2
    environment = Environment()
    for line in lines:
        for i, j in line.get_points():
            environment.add(i, j)
    if args.debug:
        print(environment)
    print(f"Part 2: count = {environment.count()}")
