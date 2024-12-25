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


def is_report_safe(report, dampener=False):
    increasing = False
    decreasing = False
    for i, _ in enumerate(report[:-1]):
        delta = report[i + 1] - report[i]
        if not (1 <= abs(delta) <= 3):
            if dampener:
                report_01 = copy.copy(report)
                report_02 = copy.copy(report)
                report_01.pop(i + 1)
                report_02.pop(i)
                return is_report_safe(report_01) or is_report_safe(report_02)
            return False
        increasing |= delta > 0
        decreasing |= delta < 0
        if increasing and decreasing:
            if dampener:
                report_01 = copy.copy(report)
                report_02 = copy.copy(report)
                report_03 = copy.copy(report)
                report_01.pop(i - 1)
                report_02.pop(i)
                report_03.pop(i + 1)
                return (
                    is_report_safe(report_01)
                    or is_report_safe(report_02)
                    or is_report_safe(report_03)
                )
            return False
    return True


if __name__ == "__main__":

    # Args
    parser = argparse.ArgumentParser(description="Advent of Code")
    parser.add_argument("input", default="input.txt", help="input file")
    args = parser.parse_args()

    # Part 1
    reports = []
    number_of_safe_reports = 0
    number_of_safe_reports_with_dampeners = 0
    with open(args.input, "r") as f:
        for line in f.readlines():
            if re.match(r"^(\d+\s*)+$", line):
                report = [int(x) for x in re.findall(r"\d+", line)]
                reports.append(report)
                if is_report_safe(report):
                    number_of_safe_reports += 1

    print(f"Part 1: Number of safe reports = {number_of_safe_reports}")

    # Part 2
    reports = []
    number_of_safe_reports = 0
    number_of_safe_reports_with_dampeners = 0
    with open(args.input, "r") as f:
        for line in f.readlines():
            if re.match(r"^(\d+\s*)+$", line):
                report = [int(x) for x in re.findall(r"\d+", line)]
                reports.append(report)
                if is_report_safe(report, dampener=True):
                    number_of_safe_reports_with_dampeners += 1

    print(
        f"Part 2: Number of safe reports with dampeners = {number_of_safe_reports_with_dampeners}"
    )
