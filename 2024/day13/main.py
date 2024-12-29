#!/usr/bin/env python3

import re
import z3
import sys
import copy
import math
import enum
import pulp
import numpy
import pickle
import argparse

if __name__ == "__main__":

    # Args
    parser = argparse.ArgumentParser(description="Advent of Code")
    parser.add_argument("input", help="input file")
    parser.add_argument("-d", "--debug", action="store_true")
    args = parser.parse_args()

    class ParserState(enum.Enum):
        WAITING_FOR_BUTTON_A = enum.auto()
        WAITING_FOR_BUTTON_B = enum.auto()
        WAITING_FOR_GOAL = enum.auto()

    games = []
    parser = ParserState.WAITING_FOR_BUTTON_A
    with open(args.input, "r") as f:
        for line in f.readlines():
            if parser == ParserState.WAITING_FOR_BUTTON_A and re.match(r"^Button A: X[+-]\d+, Y[+-]\d+$", line):
                games.append({})
                ints = [int(x) for x in re.findall(r"[+-]\d+", line)]
                games[-1]["A"] = {"x": ints[0], "y": ints[1], "cost": 3}
                parser = ParserState.WAITING_FOR_BUTTON_B
            elif parser == ParserState.WAITING_FOR_BUTTON_B and re.match(r"^Button B: X[+-]\d+, Y[+-]\d+$", line):
                ints = [int(x) for x in re.findall(r"[+-]\d+", line)]
                games[-1]["B"] = {"x": ints[0], "y": ints[1], "cost": 1}
                parser = ParserState.WAITING_FOR_GOAL
            elif parser == ParserState.WAITING_FOR_GOAL and re.match(r"^Prize: X=\d+, Y=\d+$", line):
                ints = [int(x) for x in re.findall(r"\d+", line)]
                games[-1]["goal"] = {"x": ints[0], "y": ints[1], "cost": 1}
                parser = ParserState.WAITING_FOR_BUTTON_A
            else:
                assert re.match(r"^\s*$", line), line

    # Part 1
    result = 0
    for game in games:
        problem = pulp.LpProblem("Part01", pulp.LpMinimize)
        a = pulp.LpVariable("a", cat="Integer")
        b = pulp.LpVariable("b", cat="Integer")

        # Objective
        problem += game["A"]["cost"] * a + game["B"]["cost"] * b

        # Constraints
        problem += a * game["A"]["x"] + b * game["B"]["x"] == game["goal"]["x"]
        problem += a * game["A"]["y"] + b * game["B"]["y"] == game["goal"]["y"]

        pulp.PULP_CBC_CMD(msg=0).solve(problem)
        if problem.status == 1:  # optimal
            result += game["A"]["cost"] * a.value() + game["B"]["cost"] * b.value()
            if args.debug:
                print(f"{pulp.LpStatus[problem.status]}, a = {a.value()}, b = {b.value()}")

    print(f"Part 1: result = {result}")

    # Part 2
    result = 0
    for game in games:
        solver = z3.Solver()

        a = z3.Int("a")
        b = z3.Int("b")
        constaints = [
            game["A"]["x"] * a + game["B"]["x"] * b == 10000000000000 + game["goal"]["x"],
            game["A"]["y"] * a + game["B"]["y"] * b == 10000000000000 + game["goal"]["y"],
        ]
        solver.add(constaints)

        if solver.check() == z3.sat:
            # Get the solution
            model = solver.model()
            result += game["A"]["cost"] * model[a].as_long() + game["B"]["cost"] * model[b].as_long()
            if args.debug:
                print(solver.sexpr())
                print(f"a = {model[a]}, b = {model[b]}")

    print(f"Part 2: result = {result}")
