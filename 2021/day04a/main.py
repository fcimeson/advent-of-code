#!/usr/bin/env python3

import re
import copy
import argparse


def play(game, called_number):
    N = len(game["board"])
    while N > len(game["row_count"]):
        game["row_count"].append(0)
    while N > len(game["col_count"]):
        game["col_count"].append(0)
    for i, row in enumerate(game["board"]):
        for j, board_number in enumerate(row):
            if board_number == called_number:
                game["row_count"][i] += 1
                game["col_count"][j] += 1
                if game["row_count"][i] == N or game["col_count"][j] == N:
                    return True
    return False


def score(game, called_numbers):
    N = len(game["board"])
    winner = False
    for i in range(N):
        if game["row_count"][i] == N or game["col_count"][i] == N:
            winner = True
            break
    assert winner

    total = 0
    for row in game["board"]:
        for value in row:
            if value not in called_numbers:
                total += value
    return total * called_numbers[-1]


if __name__ == "__main__":

    # Args
    parser = argparse.ArgumentParser(description="Advent of Code")
    parser.add_argument("input", help="input file")
    parser.add_argument("-d", "--debug", action="store_true", help="enable debug code")
    args = parser.parse_args()

    # Data
    with open(args.input, "r") as f:
        numbers_to_call = []
        games = []
        state = "parse_numbers_to_call"
        for line in f.readlines():
            if state == "parse_numbers_to_call":
                if re.match(r"^\s*[\d,\s]+\s*$", line):
                    numbers_to_call = [int(x) for x in re.findall(r"\d+", line)]
                    state = "parse_board"
            elif state == "parse_board":
                if re.match(r"^\s*$", line):
                    games.append({"board": [], "row_count": [], "col_count": []})
                elif re.match(r"^[\d\s]+$", line):
                    games[-1]["board"].append(
                        [int(x) for x in re.findall(r"\d+", line)]
                    )

    # Play
    winner = False
    called_numbers = []
    for called_number in numbers_to_call:
        called_numbers.append(called_number)
        for i, game in enumerate(games):
            if play(game, called_number):
                game_score = score(game, called_numbers)
                print(
                    f"Player {i} won with a score of {game_score}. Called numbers {called_numbers}."
                )
                winner = True
                break
        if winner:
            break
