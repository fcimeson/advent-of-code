#!/usr/bin/env python3
"""Advent of Code - Day 1 (Secret Entrance)

The safe has a dial (0-99) that starts at 50. Follow rotation instructions (L/R + distance)
and count how many times the dial lands on 0.

Usage:
  python3 main.py input01.txt
  python3 main.py input02.txt -d
"""
import argparse
import re


def rotate_dial(current_pos, direction, distance):
    """Rotate the dial and return the new position.
    
    Args:
        current_pos: Current dial position (0-99)
        direction: 'L' for left (decrease) or 'R' for right (increase)
        distance: Number of positions to rotate
    
    Returns:
        New position after rotation (0-99)
    """
    if direction == 'L':
        return (current_pos - distance) % 100
    elif direction == 'R':
        return (current_pos + distance) % 100
    else:
        return current_pos

if __name__ == "__main__":
    # Args
    parser = argparse.ArgumentParser(description="Advent of Code Day 1")
    parser.add_argument("input", help="input file")
    parser.add_argument("-d", "--debug", action="store_true", help="enable debug output")
    args = parser.parse_args()

    # Parse input (shared by both parts)
    rotations = []
    line_pattern = re.compile(r'^([LRlr])(\d+)$')
    with open(args.input, "r") as f:
        for line in f.readlines():
            line = line.strip()
            if not line:
                continue
            match = line_pattern.match(line)
            assert match, f"Invalid line format: {line}"
            dir_char = match.group(1).upper()
            dist = int(match.group(2))
            rotations.append((dir_char, dist))

    # Part 1: Count times dial points at 0 after any rotation
    # 
    # Problem: Need to open a safe to get the password for the North Pole entrance.
    # The safe has a dial with numbers 0-99 arranged in a circle.
    # 
    # Dial mechanics:
    #   - Starts at position 50
    #   - Rotations: L (left/decrease) or R (right/increase) + distance
    #   - Circular: L from 0 goes to 99, R from 99 goes to 0
    # 
    # Examples:
    #   - From 11, R8 → points at 19
    #   - From 19, L19 → points at 0
    #   - From 5, L10 → points at 95
    #   - From 95, R5 → points at 0
    # 
    # The password: Count how many times the dial points at 0 AFTER completing
    # any rotation (not during the rotation, only at the end).
    #
    # Example sequence: L68, L30, R48, L5, R60, L55, L1, L99, R14, L82
    #   50 → L68 → 82 → L30 → 52 → R48 → 0* → L5 → 95 → R60 → 55 
    #   → L55 → 0* → L1 → 99 → L99 → 0* → R14 → 14 → L82 → 32
    #   Password = 3 (dial pointed at 0 three times after rotations)
    #
    pos = 50
    count = 0
    for dir_char, dist in rotations:
        pos = rotate_dial(pos, dir_char, dist)
        if pos == 0:
            count += 1
        if args.debug:
            print(f"After {dir_char}{dist}: pos = {pos}")

    result1 = count
    print(f"Part 1: {result1}")
    if args.debug:
        print("\n")

    # Part 2: Count ALL times dial points at 0 (including during rotations)
    # 
    # Problem: Found another security document! Password method 0x434C49434B
    # means we must count EVERY time the dial crosses 0, not just at the end
    # of rotations.
    # 
    # Key difference from Part 1:
    #   - Part 1: Only count when dial ENDS at 0 after a rotation
    #   - Part 2: Count EVERY TIME dial passes through or lands on 0
    # 
    # Examples from same sequence:
    #   50 → L68 → 82 (passes 0 once during rotation*) → L30 → 52
    #   → R48 → 0* → L5 → 95 → R60 → 55 (passes 0 once during rotation*)
    #   → L55 → 0* → L1 → 99 → L99 → 0* → R14 → 14 
    #   → L82 → 32 (passes 0 once during rotation*)
    # 
    #   Password = 6 (3 times at end of rotation + 3 times during rotation)
    # 
    # Important edge case:
    #   - From 50, R1000 would pass through 0 ten times (makes 10 full circles)
    #     before returning to 50
    #
    pos = 50
    count_all = 0    
    for dir_char, dist in rotations:
        if args.debug:
            print(f"Postion = {pos}, Rotation = {dir_char}{dist}")

        remaining = dist        
        while remaining > 0:
            # Calculate distance to next zero crossing
            if dir_char == 'L':
                # Going left: distance to 0 is current position
                # If pos is 10, we hit 0 after 10 clicks left
                distance_to_zero = pos if pos > 0 else 100
            else:  # dir_char == 'R'
                # Going right: distance to 0 is (100 - pos)
                # If pos is 90, we hit 0 after 10 clicks right
                distance_to_zero = (100 - pos) if pos > 0 else 100
            
            # If we cross zero with remaining rotation, rotate to zero and count it
            if remaining >= distance_to_zero:
                pos = rotate_dial(pos, dir_char, distance_to_zero)
                remaining -= distance_to_zero
                count_all += 1
                if args.debug:
                    print(f"  Crossed zero at pos {pos}, remaining: {remaining}")
            else:
                # Otherwise, just do the remaining rotation
                pos = rotate_dial(pos, dir_char, remaining)
                if args.debug:
                    print(f"  Final rotation: {remaining}, pos now {pos}")
                remaining = 0
        
        if args.debug:
            print(f"After {dir_char}{dist}: pos = {pos}, count_all = {count_all}")

    result2 = count_all
    print(f"Part 2: {result2}")
