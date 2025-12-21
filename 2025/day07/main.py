#!/usr/bin/env python3
"""Advent of Code - Day 7 (Laboratories)

Count how many times a tachyon beam is split by splitters.

Usage:
  python3 main.py input01.txt
  python3 main.py input02.txt -d
"""
import argparse
import re
from collections import deque


class TachyonManifold:
    """Represents the physical environment where tachyon beams propagate.
    
    The manifold contains splitters (^) that cause beams to split into
    left and right components. Beams naturally propagate downward.
    """
    
    def __init__(self, grid, start_col):
        """Initialize the tachyon manifold.
        
        Args:
            grid: 2D grid representing the manifold layout
            start_col: Column where the initial beam enters (at row 0)
        """
        self.grid = grid
        self.start_col = start_col
        self.rows = len(grid)
        self.cols = len(grid[0]) if self.rows > 0 else 0
    
    def is_in_bounds(self, row, col):
        """Check if position is within manifold bounds."""
        return 0 <= row < self.rows and 0 <= col < self.cols
    
    def is_splitter(self, row, col):
        """Check if position contains a splitter (^)."""
        if self.is_in_bounds(row, col):
            return self.grid[row][col] == '^'
        return False
    
    def propagate_one_step(self, position):
        """Propagate a beam one step from its current position.
        
        Beams move downward until they hit a splitter or exit the manifold.
        When a beam hits a splitter, it splits into left and right beams.
        
        Args:
            position: Tuple of (row, col) representing beam position
        
        Returns:
            Set of new beam positions after one propagation step:
            - Empty set if beam exits the manifold
            - One position if beam continues downward
            - Two positions if beam hits a splitter (left and right)
        
        Examples:
            >>> manifold.propagate_one_step((0, 2))  # Empty space below
            {(1, 2)}
            
            >>> manifold.propagate_one_step((2, 2))  # Splitter at (3, 2)
            {(3, 1), (3, 3)}
            
            >>> manifold.propagate_one_step((9, 2))  # Exits at row 10
            set()
        """
        row, col = position
        next_row = row + 1
        
        # Check if beam exits the bottom of the manifold
        if not self.is_in_bounds(next_row, col):
            return set()
        
        # Check if beam hits a splitter at next position
        if self.is_splitter(next_row, col):
            # Split into left and right beams
            new_beams = set()
            
            # Left beam
            if self.is_in_bounds(next_row, col - 1):
                new_beams.add((next_row, col - 1))
            
            # Right beam
            if self.is_in_bounds(next_row, col + 1):
                new_beams.add((next_row, col + 1))
            
            return new_beams
        
        # Beam continues downward
        return {(next_row, col)}
    
    def propagate(self, position, depth=None, debug=False):
        """Propagate beams from starting position until they exit the manifold.
        
        Tracks beams row-by-row as they propagate downward, splitting when
        they encounter splitters. Counts the total number of splits that occur.
        
        Important: We cannot independently propagate and count splits using recursion
        because beams can merge (multiple beams at same position). If we counted
        splits recursively per beam, we would double-count splits when beams merge.
        Instead, we use an iterative row-by-row approach with sets to track unique
        beam positions at each row, ensuring each split is counted exactly once.
        
        Args:
            position: Starting (row, col) tuple for initial beam
            depth: Maximum depth (row) to propagate to. If None, propagate to bottom.
                   Only splits that occur before reaching this depth are counted.
            debug: If True, print debug visualization
        
        Returns:
            Total number of splits that occurred during propagation up to depth
        
        Examples:
            >>> manifold.propagate((0, 2), depth=4)
            1  # Only 1 split occurred before reaching depth 4
        """
        # Determine max depth to propagate
        max_depth = depth if depth is not None else self.rows
        
        # Track beams at each row (use sets to avoid duplicates)
        beams_by_row = [set() for _ in range(max_depth)]
        beams_by_row[position[0]].add(position)
        
        # Track total number of splits
        total_splits = 0
        
        # Propagate beams row by row up to max_depth - 1
        # (we don't propagate FROM the last row, we only display it)
        for row in range(max_depth - 1):
            for beam_pos in beams_by_row[row]:
                # Propagate this beam one step
                next_positions = self.propagate_one_step(beam_pos)
                
                # Count splits: when 1 beam becomes 2 beams
                if len(next_positions) == 2:
                    total_splits += 1
                
                # Add beams to their respective rows (if within depth limit)
                if next_positions:
                    for next_pos in next_positions:
                        next_row = next_pos[0]
                        if next_row < max_depth:
                            beams_by_row[next_row].add(next_pos)
        
        # Print debug visualization if requested
        if debug:
            self._print_beam_visualization(beams_by_row, max_depth)
        
        # Return total number of splits
        return total_splits
    
    def count_timelines(self, position):
        """Count distinct timelines in quantum propagation.
        
        In quantum mode, a single particle takes ALL paths through the manifold.
        Each unique complete path from start to exit represents a distinct timeline.
        
        Args:
            position: Starting (row, col) tuple for the particle
        
        Returns:
            Total number of distinct timelines (complete paths through manifold)
        """
        # Memoization cache to avoid recalculating paths from same position
        memo = {}
        
        def count_paths_recursive(pos):
            """Recursively count all paths from position to exit."""
            # Check if we've already calculated paths from this position
            if pos in memo:
                return memo[pos]
            
            # Propagate one step
            next_positions = self.propagate_one_step(pos)
            
            # Base case: particle exited the manifold
            if not next_positions:
                return 1
            
            # Recursive case: sum paths from each next position
            total_paths = 0
            for next_pos in next_positions:
                total_paths += count_paths_recursive(next_pos)
            
            # Cache the result
            memo[pos] = total_paths
            return total_paths
        
        return count_paths_recursive(position)
    
    def _print_beam_visualization(self, beams_by_row, max_depth):
        """Print visualization of beam paths through the manifold.
        
        Args:
            beams_by_row: List of beam positions at each row
            max_depth: Maximum depth to visualize
        """
        for row in range(min(max_depth, self.rows)):
            line = list(self.grid[row])
            
            # Mark all beam positions in this row
            if row < len(beams_by_row):
                beam_cols = set(col for _, col in beams_by_row[row])
                for col in beam_cols:
                    if line[col] == '.':
                        line[col] = '|'
                    elif line[col] == ' ':
                        line[col] = '|'
            
            print(''.join(line))


if __name__ == "__main__":
    # Args
    parser = argparse.ArgumentParser(description="Advent of Code Day 7")
    parser.add_argument("input", help="input file")
    parser.add_argument("-d", "--debug", action="store_true", help="enable debug output")
    parser.add_argument("--depth", type=int, default=None, help="maximum depth (row) to propagate beams")
    args = parser.parse_args()

    # Parse input (shared by both parts)
    grid = []
    start_col = None
    # Pattern: lines should contain S, ^, ., or spaces
    line_pattern = re.compile(r'^[S^. ]*$')
    with open(args.input, "r") as f:
        for line_num, line in enumerate(f.readlines(), 1):
            line = line.rstrip('\n')
            match = line_pattern.match(line)
            assert match, f"Line {line_num}: Invalid format (expected 'S', '^', '.', or spaces): {line!r}"
            if 'S' in line:
                assert start_col is None, f"Line {line_num}: Multiple 'S' markers found (already at line with col {start_col})"
                start_col = line.index('S')
            grid.append(line)
    
    assert start_col is not None, "No 'S' start marker found in input"

    # Part 1
    # Problem: Tachyon beam starts at S and moves downward
    # When it hits a splitter (^), it stops and two new beams emit left and right
    # Count total number of times beams are split
    #
    # Example:
    #   S....
    #   .....
    #   ..^..  <- Beam hits splitter, emits left and right
    #   .....
    #   .^.^.  <- Two new beams hit two more splitters
    #   Total: 3 splits
    
    manifold = TachyonManifold(grid, start_col)
    initial_position = (0, start_col)
    result1 = manifold.propagate(initial_position, depth=args.depth, debug=args.debug)
    
    print(f"Part 1: {result1}")

    # Part 2
    # Problem: Quantum tachyon manifold - single particle takes ALL paths
    # Each time particle hits a splitter, reality splits into two timelines
    # Count total number of distinct timelines (complete paths from start to exit)
    #
    # In quantum mode, the particle simultaneously goes left AND right at each splitter
    # This creates a branching tree of timelines
    # Each unique path from S to bottom represents one timeline
    
    result2 = manifold.count_timelines(initial_position)
    print(f"Part 2: {result2}")
