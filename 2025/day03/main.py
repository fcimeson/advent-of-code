#!/usr/bin/env python3
"""Advent of Code - Day 3 (Lobby)

Find the maximum joltage possible from battery banks by selecting
exactly two batteries from each bank.

Usage:
  python3 main.py input01.txt
  python3 main.py input02.txt -d
"""
import argparse
import re


def largest_serial_combination(bank, num_digits=2):
    """Find the largest N-digit number from a string of digits without rearranging.
    
    Recursive greedy algorithm:
    - If M = len(bank), search the first (M - num_digits + 1) positions
    - Choose the largest digit in that window (say at position i)
    - Recursively solve for the remaining (num_digits - 1) digits from bank[i+1:]
    
    Args:
        bank: A string of digits (the battery bank)
        num_digits: Number of digits to select (default: 2)
    
    Returns:
        The largest N-digit number that can be created by selecting N digits
        in their original order.
    """
    # Base case: need 1 digit, return the largest
    if num_digits == 1:
        return int(max(bank))
    
    # Recursive case: find largest digit in valid window, then recurse
    search_window_end = len(bank) - num_digits + 1  # can search positions 0 to (M - num_digits)
    
    # Find the largest digit in the search window
    max_digit = bank[0]
    max_digit_pos = 0
    
    for i in range(1, search_window_end):
        if bank[i] > max_digit:
            max_digit = bank[i]
            max_digit_pos = i
    
    # Recursively solve for the remaining digits after this position
    remaining_result = largest_serial_combination(bank[max_digit_pos + 1:], num_digits - 1)
    
    # Combine: shift the current digit left by (num_digits - 1) positions
    return int(max_digit) * (10 ** (num_digits - 1)) + remaining_result



if __name__ == "__main__":
    # Args
    parser = argparse.ArgumentParser(description="Advent of Code Day 3")
    parser.add_argument("input", help="input file")
    parser.add_argument("-d", "--debug", action="store_true", help="enable debug output")
    args = parser.parse_args()

    # Parse input (shared by both parts)
    data = []
    # Pattern: one or more digits
    bank_pattern = re.compile(r'^\d+$')
    with open(args.input, "r") as f:
        for line_num, line in enumerate(f.readlines(), 1):
            line = line.strip()
            if line:
                match = bank_pattern.match(line)
                assert match, f"Line {line_num}: Invalid bank format (expected digits only): {line}"
                data.append(line)

    # Part 1
    # Problem: For each battery bank (line of digits), select exactly two batteries
    # to maximize the joltage (the two-digit number formed by those batteries).
    # Batteries cannot be rearranged - position matters (left battery forms tens digit).
    # Find the sum of all maximum joltages.
    result1 = 0
    for bank in data:
        max_joltage = largest_serial_combination(bank)
        result1 += max_joltage
        if args.debug:
            print(f"Bank {bank}: max joltage = {max_joltage}")
    
    print(f"Part 1: {result1}")

    # Part 2
    # Problem: Select exactly 12 batteries from each bank to maximize joltage.
    # The joltage is now a 12-digit number formed by the selected batteries.
    # 
    # Solution: Greedy algorithm
    # - For each position in the result (leftmost to rightmost):
    #   - Choose the largest digit from the remaining valid candidates
    #   - Valid candidates are those that leave enough digits to complete the 12-digit number
    # - Example: From "987654321111111" (15 digits, skip 3)
    #   - Position 0: Can search indices 0-3 (must leave 11 more), pick '9' at index 0
    #   - Position 1: Can search indices 1-4 (must leave 10 more), pick '8' at index 1
    #   - Position 2: Can search indices 2-5 (must leave 9 more), pick '7' at index 2
    #   - Continue: 987654321111
    # 
    # This greedy approach works because maximizing the leftmost digits has the 
    # greatest impact on the final number's magnitude.
    result2 = 0
    for bank in data:
        max_joltage = largest_serial_combination(bank, num_digits=12)
        result2 += max_joltage
        if args.debug:
            print(f"Bank {bank}: max 12-digit joltage = {max_joltage}")
    
    print(f"Part 2: {result2}")
