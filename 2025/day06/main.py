#!/usr/bin/env python3
"""Advent of Code - Day 6 (Trash Compactor)

Solve cephalopod math worksheet problems arranged vertically.

Usage:
  python3 main.py input01.txt
  python3 main.py input02.txt -d
"""
import argparse
import re


def extract_problems(lines):
    """Extract vertical math problems from the input lines.
    
    Problems are arranged vertically in columns separated by spaces.
    Each problem consists of numbers stacked vertically with an operation at the bottom.
    
    Args:
        lines: List of strings representing the input
        
    Returns:
        List of problems, where each problem is a list of strings
        (numbers followed by operation)
    """
    if not lines:
        return []
    
    # Find the width of the input
    max_width = max(len(line) for line in lines)
    
    # Pad all lines to the same width
    padded_lines = [line.ljust(max_width) for line in lines]
    
    # Extract columns (problems)
    problems = []
    col = 0
    while col < max_width:
        # Skip leading spaces
        if all(padded_lines[row][col] == ' ' for row in range(len(padded_lines))):
            col += 1
            continue
        
        # Extract a problem (find the column range)
        problem_start = col
        problem_end = col
        
        # Find the end of this problem (next all-space column or end)
        while problem_end < max_width:
            if all(padded_lines[row][problem_end] == ' ' for row in range(len(padded_lines))):
                break
            problem_end += 1
        
        # Extract the problem column data (preserve spacing!)
        problem_data = []
        for row in range(len(padded_lines)):
            val = padded_lines[row][problem_start:problem_end]
            # Only skip completely empty rows
            if val.strip():
                problem_data.append(val)
        
        if problem_data:
            problems.append(problem_data)
        
        col = problem_end
    
    return problems


def extract_cephalopod_numbers(number_rows):
    """Extract numbers using cephalopod math (right-to-left column reading).
    
    In cephalopod math, numbers are written right-to-left in columns.
    Each number string is read column-by-column (digit positions),
    and each column of digits (top to bottom) forms a new number.
    
    Example: ['64 ', '23 ', '314']
    - Column 0: 6,2,3 → 623
    - Column 1: 4,3,1 → 431
    - Column 2: (space),(space),4 → 4
    - Returns: [623, 431, 4]
    
    Args:
        number_rows: List of number strings (with preserved spacing)
        
    Returns:
        List of integers extracted using cephalopod math rules
    """
    if not number_rows:
        return []
    
    # Numbers are already padded in the input - find max length
    max_digits = max(len(num_str) for num_str in number_rows)
    
    # Read column by column (left to right) to construct numbers
    # Each column's digits (top to bottom) form one number
    numbers = []
    for col_idx in range(max_digits):
        # Read top to bottom in this column to build a number
        digits = []
        for row in number_rows:
            if col_idx < len(row):
                char = row[col_idx]
                if char != ' ':
                    digits.append(char)
        if digits:
            number = int(''.join(digits))
            numbers.append(number)
    
    return numbers

if __name__ == "__main__":
    # Args
    parser = argparse.ArgumentParser(description="Advent of Code Day 6")
    parser.add_argument("input", help="input file")
    parser.add_argument("-d", "--debug", action="store_true", help="enable debug output")
    args = parser.parse_args()

    # Parse input (shared by both parts)
    # Pattern: lines should contain digits, operators (+, *), and spaces
    line_pattern = re.compile(r'^[\d+* ]*$')
    with open(args.input, "r") as f:
        lines = []
        for line_num, line in enumerate(f.readlines(), 1):
            line = line.rstrip('\n')
            match = line_pattern.match(line)
            assert match, f"Line {line_num}: Invalid format (expected digits, +, *, or spaces): {line!r}"
            lines.append(line)

    # Part 1
    # Problem: Math problems are arranged vertically in columns separated by spaces
    # Numbers are vertically stacked, operation is at the bottom
    # Calculate each problem and sum the results
    
    # Extract problems using the extraction method
    problems = extract_problems(lines)
    
    result1 = 0
    for problem in problems:
        assert len(problem) >= 2
        
        # Last element is the operation (strip spaces)
        operation = problem[-1].strip()
        numbers = [int(x.strip()) for x in problem[:-1]]
        
        if operation == '+':
            answer = sum(numbers)
        elif operation == '*':
            answer = 1
            for num in numbers:
                answer *= num
        else:
            answer = 0
        
        result1 += answer
        if args.debug:
            # Format as "123 * 45 * 6 = 33210"
            problem_str = f" {operation} ".join(str(n) for n in numbers)
            print(f"{problem_str} = {answer}")
    
    print(f"Part 1: {result1}")
    if args.debug:
        print()

    # Part 2
    # Cephalopod math is read right-to-left in columns
    # Each number column is read from most significant (top) to least significant (bottom)
    # but the numbers themselves are built reading right-to-left across columns
    
    result2 = 0
    for problem in problems:
        if len(problem) < 2:
            continue
        
        # Last element is the operation (strip spaces)
        operation = problem[-1].strip()
        number_rows = problem[:-1]
        
        # Extract numbers using cephalopod math
        numbers = extract_cephalopod_numbers(number_rows)
        
        # Calculate result
        if operation == '+':
            answer = sum(numbers)
        elif operation == '*':
            answer = 1
            for num in numbers:
                answer *= num
        else:
            answer = 0
        
        result2 += answer
        if args.debug:
            # Format as "4 + 431 + 623 = 1058"
            problem_str = f" {operation} ".join(str(n) for n in numbers)
            print(f"{problem_str} = {answer}")
    
    print(f"Part 2: {result2}")
