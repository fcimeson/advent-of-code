#!/usr/bin/env python3

import re
import sys
import copy
import argparse

INF = float("inf")
RE_DIGIT = r"[abcdefg]{1,7}"


class CustomList(list):
    def __str__(self):
        s = ""
        it = super().__iter__()
        while True:
            try:
                x = next(it)
                s += str(x) + " "
            except StopIteration:
                break
        return s


class CharSet(set):
    def __init__(self, input_string):
        super().__init__(sorted(list(input_string)))

    def __str__(self):
        s = ""
        it = super().__iter__()
        while True:
            try:
                s += next(it)
            except StopIteration:
                break
        return s

    def __hash__(self):
        return hash(self.__str__())


if __name__ == "__main__":

    # Args
    parser = argparse.ArgumentParser(description="Advent of Code")
    parser.add_argument("input", help="input file")
    parser.add_argument("--days", type=int, default=80, help="length of simulation")
    parser.add_argument("-d", "--debug", action="store_true", help="enable debug code")
    args = parser.parse_args()

    # Data
    data = []
    input_rx = r"^(\s*%s\s{1,}){10}\|(\s{1,}%s\s*){4}$" % (RE_DIGIT, RE_DIGIT)
    with open(args.input, "r") as f:
        for line in f.readlines():
            if re.match(input_rx, line):
                s = line.split("|")
                data.append(
                    {
                        "signals": CustomList(
                            [CharSet(s) for s in re.findall(RE_DIGIT, s[0])]
                        ),
                        "output": CustomList(
                            [CharSet(s) for s in re.findall(RE_DIGIT, s[1])]
                        ),
                    }
                )
            else:
                raise ValueError(f"Incorrectly formated input: {line}")

    # Solve
    total = 0
    for x in data:
        signal_to_digit = {}
        digit_to_signal = [None] * 10

        left_segments = None
        top_right_segment = None
        unknown_signals = copy.copy(x["signals"])
        while len(unknown_signals):
            # Remove from front and add back to the end if we can't identify
            signal = unknown_signals.pop(0)
            number_of_segments = len(signal)

            # The only 2 segment digit is 1
            if number_of_segments == 2:
                signal_to_digit[signal] = 1
                digit_to_signal[1] = signal
                continue

            # The only 3 segment digit is 7
            if number_of_segments == 3:
                signal_to_digit[signal] = 7
                digit_to_signal[7] = signal
                continue

            # The only 4 segment digit is 4
            if number_of_segments == 4:
                signal_to_digit[signal] = 4
                digit_to_signal[4] = signal
                continue

            # The only 7 segment digit is 8
            if number_of_segments == 7:
                signal_to_digit[signal] = 8
                digit_to_signal[8] = signal
                continue

            # The top right segment can be found by subtracking 6 from 1
            if not top_right_segment and digit_to_signal[1] and digit_to_signal[6]:
                top_right_segment = digit_to_signal[1] - digit_to_signal[6]

            # The left segments can be found by subtracting 3 from 8
            if not left_segments and digit_to_signal[3] and digit_to_signal[8]:
                left_segments = digit_to_signal[8] - digit_to_signal[3]

            # Characters with 5 segments: 2, 3, 5
            if number_of_segments == 5:

                # 3 is the only 5 segments digit that doesn't has perfect overlap with the 1 digit
                if (
                    not digit_to_signal[3]
                    and digit_to_signal[1]
                    and signal >= digit_to_signal[1]
                ):
                    signal_to_digit[signal] = 3
                    digit_to_signal[3] = signal
                    continue

                # 5 is the only 5 segment digit with the top right missing
                if (
                    not digit_to_signal[5]
                    and top_right_segment
                    and signal.isdisjoint(top_right_segment)
                ):
                    signal_to_digit[signal] = 5
                    digit_to_signal[5] = signal
                    continue

                # After 3 and 5 have been identified, 2 is the only digit with 5 segments
                if not digit_to_signal[2] and digit_to_signal[3] and digit_to_signal[5]:
                    signal_to_digit[signal] = 2
                    digit_to_signal[2] = signal
                    continue

            # Characters with 6 segments: 0, 6, 9
            if number_of_segments == 6:

                # 6 is the only 6 segments digit that doesn't have perfect overlap with the 1 digit
                if (
                    not digit_to_signal[6]
                    and digit_to_signal[1]
                    and not signal >= digit_to_signal[1]
                ):
                    signal_to_digit[signal] = 6
                    digit_to_signal[6] = signal
                    continue

                # 9 is the only 6 segment digit without perfect overlap of the left segments
                if (
                    not digit_to_signal[9]
                    and left_segments
                    and not signal >= left_segments
                ):
                    signal_to_digit[signal] = 9
                    digit_to_signal[9] = signal
                    continue

                # After 6 and 9 have been identified, 0 is the only digit with 6 segments
                if not digit_to_signal[0] and digit_to_signal[6] and digit_to_signal[9]:
                    signal_to_digit[signal] = 0
                    digit_to_signal[0] = signal
                    continue

            # Could not identify, need to look at other numbers
            unknown_signals.append(signal)

        # Convert the pattern to digits and and tally the total
        x["solution"] = 0
        for i, signal in enumerate(x["output"]):
            x["solution"] += signal_to_digit[signal] * 10 ** (3 - i)
        total += x["solution"]
        if args.debug:
            print(f"{x['output']}: {x['solution']}")

    print(f"The total is {total}")
