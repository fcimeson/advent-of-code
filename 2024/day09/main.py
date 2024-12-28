#!/usr/bin/env python3

import re
import sys
import copy
import math
import enum
import numpy
import pickle
import argparse


def disk_to_str(disk):
    s = ""
    for block in disk:
        if block is None:
            s += "."
        else:
            s += str(block)
    return s


def checksum(disk):
    sum = 0
    for i, x in enumerate(disk):
        if x is not None:
            sum += i * x
    return sum


def free_space(disk, i):
    j = i
    while j < len(disk) and disk[j] is None:
        j += 1
    return j - i


def defrag(disk, file_start, file_end, initial_i=0):
    i = initial_i
    file_size = file_end - file_start + 1
    while i < file_start:
        while disk[i] is not None and i < file_start:
            i += 1
        if free_space(disk, i) >= file_size:
            disk[i : i + file_size] = disk[file_start : file_end + 1]
            disk[file_start : file_end + 1] = [None] * file_size
            return disk
        while disk[i] is None:
            i += 1
    return disk


if __name__ == "__main__":

    # Args
    parser = argparse.ArgumentParser(description="Advent of Code")
    parser.add_argument("input", help="input file")
    parser.add_argument("-d", "--debug", action="store_true")
    args = parser.parse_args()

    class Parser(enum.Enum):
        INDEX = enum.auto()
        FREE = enum.auto()
        DONE = enum.auto()

    disk = []
    index = 0
    parser_state = Parser.INDEX
    with open(args.input, "r") as f:
        for line in f.readlines():
            assert parser_state == Parser.INDEX
            for n in line:
                if parser_state == Parser.INDEX:
                    disk += [index] * int(n)
                    parser_state = Parser.FREE
                    index += 1
                elif parser_state == Parser.FREE:
                    disk += [None] * int(n)
                    parser_state = Parser.INDEX
                else:
                    assert False
            parser_state = Parser.DONE

    # Part 1
    i = 0
    j = len(disk) - 1
    defragged = copy.deepcopy(disk)
    while i < j:
        if args.debug:
            print(disk_to_str(defragged))
        while defragged[i] is not None and i < j:
            i += 1
        while defragged[j] is None and i < j:
            j -= 1
        defragged[i] = defragged[j]
        defragged[j] = None

    print(f"Part 1: checksum = {checksum(defragged)}")

    # Part 2
    j01 = j02 = len(disk) - 1
    defragged = copy.deepcopy(disk)
    moved = set()
    while j01 > 0:
        if args.debug:
            print(disk_to_str(defragged))
        while defragged[j02] is None and j02 > 0:
            j02 -= 1
        if defragged[j02] is None:
            break
        index = defragged[j02]
        j01 = j02
        while j01 - 1 >= 0 and defragged[j01 - 1] == index:
            j01 -= 1
        if index not in moved:
            defragged = defrag(defragged, j01, j02)
        while defragged[j02] == index:
            j02 -= 1
        moved.add(index)

    print(f"Part 2: checksum = {checksum(defragged)}")
