#!/usr/bin/env python3
"""Advent of Code - Day 5 (Cafeteria)

Check which ingredient IDs fall within fresh ranges.

Usage:
  python3 main.py input01.txt
  python3 main.py input02.txt -d
"""
import argparse
import re


class FreshnessChecker:
    """Stores ranges and checks if an ingredient ID is fresh."""
    
    def __init__(self):
        self.ranges = []
    
    def add_range(self, start, end):
        """Add a fresh range (inclusive)."""
        self.ranges.append((start, end))
    
    def is_fresh(self, ingredient_id):
        """Check if an ingredient ID falls within any fresh range."""
        for start, end in self.ranges:
            if start <= ingredient_id <= end:
                return True
        return False
    
    def count_all_fresh_ids(self):
        """Count total unique ingredient IDs covered by all ranges."""
        if not self.ranges:
            return 0
        
        # Sort ranges by start position
        sorted_ranges = sorted(self.ranges)
        
        # Merge overlapping ranges
        merged = []
        current_start, current_end = sorted_ranges[0]
        
        for start, end in sorted_ranges[1:]:
            if start <= current_end + 1:
                # Overlapping or adjacent - merge
                current_end = max(current_end, end)
            else:
                # Non-overlapping - save current and start new
                merged.append((current_start, current_end))
                current_start, current_end = start, end
        
        # Don't forget the last range
        merged.append((current_start, current_end))
        
        # Count total IDs in merged ranges
        total = 0
        for start, end in merged:
            total += end - start + 1  # +1 because ranges are inclusive
        
        return total

if __name__ == "__main__":
    # Args
    parser = argparse.ArgumentParser(description="Advent of Code Day 5")
    parser.add_argument("input", help="input file")
    parser.add_argument("-d", "--debug", action="store_true", help="enable debug output")
    args = parser.parse_args()

    # Parse input (shared by both parts)
    freshness_checker = FreshnessChecker()
    ingredient_ids = []
    
    # Patterns
    range_pattern = re.compile(r'^(\d+)-(\d+)$')
    id_pattern = re.compile(r'^\d+$')
    
    with open(args.input, "r") as f:
        lines = f.read().strip().split('\n\n')
        
        assert len(lines) == 2, f"Expected 2 sections separated by blank line, got {len(lines)}"
        
        # Parse ranges
        for line_num, line in enumerate(lines[0].split('\n'), 1):
            line = line.strip()
            if line:
                match = range_pattern.match(line)
                assert match, f"Range section line {line_num}: Invalid format (expected 'num-num'): {line}"
                start, end = int(match.group(1)), int(match.group(2))
                freshness_checker.add_range(start, end)
        
        # Parse ingredient IDs
        for line_num, line in enumerate(lines[1].split('\n'), 1):
            line = line.strip()
            if line:
                match = id_pattern.match(line)
                assert match, f"ID section line {line_num}: Invalid format (expected number): {line}"
                ingredient_ids.append(int(line))

    # Part 1
    # Problem: Count how many ingredient IDs fall within any of the fresh ranges
    # Ranges are inclusive and can overlap
    result1 = 0
    for ingredient_id in ingredient_ids:
        if freshness_checker.is_fresh(ingredient_id):
            result1 += 1
            if args.debug:
                print(f"Ingredient ID {ingredient_id} is fresh")
        elif args.debug:
            print(f"Ingredient ID {ingredient_id} is spoiled")
    
    print(f"Part 1: {result1}")

    # Part 2
    # Problem: Count all unique ingredient IDs covered by the fresh ranges
    # (merge overlapping ranges and count total coverage)
    result2 = freshness_checker.count_all_fresh_ids()
    print(f"Part 2: {result2}")
