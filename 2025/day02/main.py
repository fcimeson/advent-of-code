#!/usr/bin/env python3
"""Advent of Code - Day 2 (Gift Shop)

Find invalid product IDs (numbers formed by repeating a digit sequence twice)
in given ranges and sum them.

Usage:
  python3 main.py input01.txt
  python3 main.py input02.txt -d
"""
import argparse
import re


def is_valid(num, exactly_twice=False):
    """Check if a number is valid (NOT a repeated pattern).
    
    Returns True if valid, False if invalid (repeated pattern).
    
    Args:
        num: The number to check
        exactly_twice: If True, invalid only if repeated exactly twice (Part 1)
                      If False, invalid if repeated at least twice (Part 2)
    
    Examples of invalid numbers:
    - 11 (1 repeated 2 times)
    - 6464 (64 repeated 2 times)
    - 123123123 (123 repeated 3 times)
    - 1212121212 (12 repeated 5 times)
    """
    id_string = str(num)
    length = len(id_string)
    
    # Try each possible pattern length (divisor of total length)
    # Pattern must repeat at least 2 times, so max pattern length is length // 2
    for pattern_len in range(1, length // 2 + 1):
        # Number of repetitions
        repititions = length // pattern_len

        # Check if length is divisible by pattern length and it must repeat at least twice
        if length % pattern_len != 0 or repititions < 2:
            continue
        if exactly_twice and repititions != 2:
            continue
        
        # Check if the entire string is this pattern repeated
        pattern = id_string[0:pattern_len]
        if pattern * repititions == id_string:
            return False  # Invalid
    
    return True  # Valid (no matching repeated pattern found)


if __name__ == "__main__":
    # Args
    parser = argparse.ArgumentParser(description="Advent of Code Day 2")
    parser.add_argument("input", help="input file")
    parser.add_argument("-d", "--debug", action="store_true", help="enable debug output")
    args = parser.parse_args()

    # Parse input (shared by both parts)
    with open(args.input, "r") as f:
        content = f.read().strip()
    
    # Split by commas and parse each range
    # Pattern: exactly digits-digits (anchored to match entire string)
    ranges = []
    range_pattern = r'^(\d+)-(\d+)$'   
    for part in content.split(','):
        part = part.strip()
        match = re.match(range_pattern, part)
        assert match, f"Invalid range format: '{part}'"
        start, end = int(match.group(1)), int(match.group(2))
        ranges.append((start, end))
    if args.debug:
        print(f"Found {len(ranges)} ranges")

    # Part 1: Find and sum all invalid IDs (repeated exactly twice)
    # 
    # Problem: Gift shop database has invalid product IDs from a young Elf playing.
    # Invalid IDs are numbers made of some digit sequence repeated exactly twice.
    # 
    # Examples of invalid IDs:
    #   - 55 (5 repeated twice)
    #   - 6464 (64 repeated twice)
    #   - 123123 (123 repeated twice)
    # 
    # Valid IDs (not repeated exactly twice):
    #   - 101 (not a repeating pattern)
    #   - 0101 (has leading zeros, not a valid ID)
    # 
    # Task: Check each ID range, find all invalid IDs, and sum them.
    # 
    # Example ranges:
    #   11-22 -> invalid IDs: 11, 22
    #   95-115 -> invalid IDs: 99
    #   998-1012 -> invalid IDs: 1010
    #
    result1 = 0
    invalid_count = 0
    for start, end in ranges:
        range_invalids = []
        for num in range(start, end + 1):
            if not is_valid(num, exactly_twice=True):
                result1 += num
                invalid_count += 1
                range_invalids.append(num)
        if args.debug and range_invalids:
            print(f"Range {start}-{end}: {range_invalids}")
    if args.debug:
        print(f"Found {invalid_count} invalid IDs")
    
    print(f"Part 1: {result1}")

    # Part 2: Find and sum all invalid IDs (repeated at least twice)
    # 
    # Problem: The young Elf was doing more silly patterns! Now check for IDs
    # that are made of digit sequences repeated at least twice (not just exactly twice).
    # 
    # Examples of invalid IDs:
    #   - 12341234 (1234 repeated 2 times)
    #   - 123123123 (123 repeated 3 times)
    #   - 1212121212 (12 repeated 5 times)
    #   - 1111111 (1 repeated 7 times)
    # 
    # This expands on Part 1 to include patterns repeated 2+ times, not just exactly 2.
    # 
    # Example changes from Part 1:
    #   95-115 -> now also includes 111 (1 repeated 3 times)
    #   998-1012 -> now also includes 999 (9 repeated 3 times)
    #   565653-565659 -> now includes 565656 (56 repeated 3 times)
    #
    result2 = 0
    invalid_count2 = 0
    for start, end in ranges:
        range_invalids = []
        for num in range(start, end + 1):
            if not is_valid(num, exactly_twice=False):
                result2 += num
                invalid_count2 += 1
                range_invalids.append(num)
        if args.debug and range_invalids:
            print(f"Range {start}-{end} (Part 2): {range_invalids}")
    if args.debug:
        print(f"Found {invalid_count2} invalid IDs (Part 2)")
    
    print(f"Part 2: {result2}")
