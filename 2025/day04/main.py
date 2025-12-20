#!/usr/bin/env python3
"""Advent of Code - Day 4 (Printing Department)

Count how many paper rolls can be accessed by forklifts.
A roll is accessible if it has fewer than 4 adjacent rolls.

Usage:
  python3 main.py input01.txt
  python3 main.py input02.txt -d
"""
import argparse
import re


def count_neighbours(grid, row, col, target='@'):
    """Count neighbours of a specific character at a given location.
    
    Args:
        grid: 2D list of characters representing the warehouse layout
        row: Row index of the location to check
        col: Column index of the location to check
        target: Character to count in neighbours (default '@')
        
    Returns:
        Number of neighbours matching the target character
    """
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    
    count = 0
    for delta_row in [-1, 0, 1]:
        for delta_col in [-1, 0, 1]:
            if delta_row == 0 and delta_col == 0:
                continue
            neighbour_row = row + delta_row
            neighbour_col = col + delta_col
            if 0 <= neighbour_row < rows and 0 <= neighbour_col < cols:
                if grid[neighbour_row][neighbour_col] == target:
                    count += 1
    
    return count


def identify_accessible_rolls(grid):
    """Identify accessible rolls in the grid.
    
    Args:
        grid: 2D list of characters representing the warehouse layout
        
    Returns:
        2D list of characters with 'x' marking accessible rolls, '.' for everything else
    """
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    
    # Create result grid filled with '.'
    accessible = [['.' for _ in range(cols)] for _ in range(rows)]
    
    for row in range(rows):
        for col in range(cols):
            if grid[row][col] == '@':
                # Count adjacent rolls using count_neighbours
                adjacent_count = count_neighbours(grid, row, col, '@')
                
                # Mark as accessible if fewer than 4 adjacent rolls
                if adjacent_count < 4:
                    accessible[row][col] = 'x'
    
    return accessible


def print_debug_output(grid, accessible):
    """Print debug output showing original grid with accessible rolls marked.
    
    Args:
        grid: Original 2D grid
        accessible: 2D grid with 'x' marking accessible rolls
    """
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    
    print("\nDebug Output:")
    print("=" * cols)
    for row in range(rows):
        line = ""
        for col in range(cols):
            if accessible[row][col] == 'x':
                line += 'x'
            else:
                line += grid[row][col]
        print(line)
    print("=" * cols)
    print("(x = accessible roll, @ = inaccessible roll, . = empty space)\n")


if __name__ == "__main__":
    # Args
    parser = argparse.ArgumentParser(description="Advent of Code Day 4")
    parser.add_argument("input", help="input file")
    parser.add_argument("-d", "--debug", action="store_true", help="enable debug output")
    args = parser.parse_args()

    # Parse input (shared by both parts)
    grid = []
    # Pattern: one or more @ or . characters
    grid_pattern = re.compile(r'^[@.]+$')
    with open(args.input, "r") as f:
        for line_num, line in enumerate(f.readlines(), 1):
            line = line.strip()
            if line:
                match = grid_pattern.match(line)
                assert match, f"Line {line_num}: Invalid grid format (expected only '@' or '.' characters): {line}"
                grid.append(list(line))

    # Part 1
    # Problem: Count paper rolls (@) that have fewer than 4 adjacent rolls
    # Adjacent means the 8 positions around a cell (including diagonals)
    accessible_rolls = identify_accessible_rolls(grid)
    
    # Count accessible rolls
    result1 = sum(row.count('x') for row in accessible_rolls)
    
    # Debug output
    if args.debug:
        print_debug_output(grid, accessible_rolls)
    
    print(f"Part 1: {result1}")

    # Part 2
    # Problem: Keep removing accessible rolls until no more can be removed
    # Make a copy of the grid so we don't modify the original
    import copy
    working_grid = copy.deepcopy(grid)
    
    total_removed = 0
    iteration = 0
    
    while True:
        # Find accessible rolls in current state
        accessible_rolls = identify_accessible_rolls(working_grid)
        
        # Count how many accessible rolls we found
        accessible_count = sum(row.count('x') for row in accessible_rolls)
        
        if accessible_count == 0:
            # No more accessible rolls, we're done
            break
        
        iteration += 1
        total_removed += accessible_count
        
        if args.debug:
            print(f"\nIteration {iteration}: Removing {accessible_count} rolls")
            print_debug_output(working_grid, accessible_rolls)
        
        # Remove accessible rolls (replace '@' with '.' where accessible)
        rows = len(working_grid)
        cols = len(working_grid[0]) if rows > 0 else 0
        for row in range(rows):
            for col in range(cols):
                if accessible_rolls[row][col] == 'x':
                    working_grid[row][col] = '.'
    
    if args.debug:
        print(f"\nFinal state after {iteration} iterations:")
        # Show final grid
        for row in working_grid:
            print(''.join(row))
        print()
    
    result2 = total_removed
    print(f"Part 2: {result2}")
