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
    game_boards = []
    numbers_to_call = []
    with open(args.input, "r") as f:
        state = "parse_numbers_to_call"
        for line in f.readlines():
            if state == "parse_numbers_to_call":
                if re.match(r"^\s*[\d,\s]+\s*$", line):
                    numbers_to_call = [int(x) for x in re.findall(r"\d+", line)]
                    state = "parse_board"
            elif state == "parse_board":
                if re.match(r"^\s*$", line):
                    game_boards.append([])
                elif re.match(r"^[\d\s]+$", line):
                    game_boards[-1].append([int(x) for x in re.findall(r"\d+", line)])

    # Part 1
    winner = False
    called_numbers = []
    games = [{"board": game_board, "row_count": [], "col_count": []} for game_board in game_boards]
    for called_number in numbers_to_call:
        called_numbers.append(called_number)
        for i, game in enumerate(games):
            if play(game, called_number):
                game_score = score(game, called_numbers)
                print(f"Part 1: player {i} won with a score of {game_score}")
                if args.debug:
                    print(f"        called numbers {called_numbers}.")
                winner = True
                break
        if winner:
            break

    # Part 2
    winners = []
    called_numbers = []
    games = [{"board": game_board, "row_count": [], "col_count": []} for game_board in game_boards]
    while len(games) > 0:
        called_number = numbers_to_call.pop(0)
        called_numbers.append(called_number)
        active = []
        while games:
            game = games.pop(0)
            if play(game, called_number):
                winners.append(game)
            else:
                active.append(game)
        games = active
    looser = winners[-1]
    game_score = score(looser, called_numbers)
    print(f"Part 2: the last game won with a of {game_score}")
    if args.debug:
        print(f"        called numbers {called_numbers}.")
