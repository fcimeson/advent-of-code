#!/usr/bin/env python3
"""Advent of Code - Day 11 (Reactor)

Count all different paths from 'you' to 'out' in a device network.

Usage:
  python3 main.py input01.txt
  python3 main.py input02.txt -d
"""
import argparse
import re


class DeviceNetwork:
    """Represents a network of interconnected devices.
    
    Each device outputs to zero or more other devices, forming a directed graph.
    Data flows from device to device along these connections.
    
    This implementation assumes the graph is a DAG (Directed Acyclic Graph).
    """
    
    def __init__(self, edges):
        """Initialize the device network from a list of edges.
        
        Args:
            edges: List of tuples (device_name, [output1, output2, ...])
        
        Raises:
            AssertionError: If the graph contains cycles (not a DAG)
        """
        self.connections = {}
        self.reachability = {}  # Pre-computed reachability: reachability[i] = set of nodes reachable from i
        
        # Build the graph
        for device_name, outputs in edges:
            self.connections[device_name] = outputs
        
        # Verify it's a DAG
        assert self.is_dag(), "Graph contains cycles - must be a DAG"
    
    def get_outputs(self, device_name):
        """Get the list of devices this device outputs to.
        
        Args:
            device_name: Name of the device
        
        Returns:
            List of output device names, or empty list if device has no outputs
        """
        return self.connections.get(device_name, [])
    
    def is_reachable(self, start, end, cache=None):
        """Check if end is reachable from start using BFS.
        
        Args:
            start: Starting device name
            end: Target device name
            cache: Dictionary cache for reachability results (deprecated, use pre-computed)
        
        Returns:
            True if end is reachable from start, False otherwise
        """
        # Compute reachability if not already done
        if not self.reachability:
            self.compute_reachability()
        
        # Use pre-computed reachability
        return end in self.reachability.get(start, set())
    
    def compute_reachability(self):
        """Pre-compute reachability for all nodes using BFS from each node.
        
        After calling this, self.reachability[node] contains the set of all
        nodes reachable from 'node'.
        """
        from collections import deque
        
        # Get all nodes
        all_nodes = set(self.connections.keys())
        for outputs in self.connections.values():
            all_nodes.update(outputs)
        
        # BFS from each node to find all reachable nodes
        for start_node in all_nodes:
            reachable = set()
            queue = deque([start_node])
            visited = {start_node}
            
            while queue:
                current = queue.popleft()
                
                for neighbor in self.get_outputs(current):
                    if neighbor not in visited:
                        visited.add(neighbor)
                        reachable.add(neighbor)
                        queue.append(neighbor)
            
            self.reachability[start_node] = reachable
    
    def is_dag(self):
        """Check if the graph is a Directed Acyclic Graph (DAG).
        
        Uses DFS with three-color marking:
        - White (0): Unvisited
        - Gray (1): Currently being processed (in the DFS stack)
        - Black (2): Fully processed
        
        If we encounter a gray node, we've found a back edge (cycle).
        
        Returns:
            True if the graph is a DAG (no cycles), False otherwise
        """
        from collections import deque
        
        # Get all nodes
        all_nodes = set(self.connections.keys())
        for outputs in self.connections.values():
            all_nodes.update(outputs)
        
        # Color states: 0=white (unvisited), 1=gray (processing), 2=black (done)
        color = {node: 0 for node in all_nodes}
        
        def dfs(node):
            """DFS to detect cycles. Returns True if cycle found."""
            color[node] = 1  # Mark as being processed (gray)
            
            for neighbor in self.get_outputs(node):
                if color.get(neighbor, 0) == 1:  # Back edge to gray node = cycle!
                    return True
                if color.get(neighbor, 0) == 0:  # Unvisited
                    if dfs(neighbor):
                        return True
            
            color[node] = 2  # Mark as done (black)
            return False
        
        # Check all nodes (graph might be disconnected)
        for node in all_nodes:
            if color[node] == 0:
                if dfs(node):
                    return False  # Cycle found
        
        return True  # No cycles found - it's a DAG!
    
    def count_paths(self, start, end, cache=None):
        """Count all different paths from start device to end device.
        
        Optimized for DAGs (Directed Acyclic Graphs) - no cycle detection needed.
        Uses simple cache key (start, end) for maximum performance.
        
        Args:
            start: Starting device name
            end: Target device name
            cache: Dictionary cache for memoization
        
        Returns:
            Number of distinct paths from start to end
        
        Examples:
            If 'you' connects to ['a', 'b'] and both 'a' and 'b' connect to 'out',
            then count_paths('you', 'out') returns 2.
        """
        if cache is None:
            cache = {}
        
        # Base case: reached the destination
        if start == end:
            return 1
        
        # Simple cache key for DAGs: just (start, end)
        cache_key = (start, end)
        if cache_key in cache:
            return cache[cache_key]
        
        # Early termination: check if end is reachable from start (using pre-computed)
        if not self.is_reachable(start, end):
            cache[cache_key] = 0
            return 0
        
        # Recursively count paths through all outputs
        total_paths = 0
        for output_device in self.get_outputs(start):
            total_paths += self.count_paths(output_device, end, cache)
        
        # Cache the result
        cache[cache_key] = total_paths
        
        return total_paths


if __name__ == "__main__":
    # Args
    parser = argparse.ArgumentParser(description="Advent of Code Day 11")
    parser.add_argument("input", help="input file")
    parser.add_argument("-d", "--debug", action="store_true", help="enable debug output")
    args = parser.parse_args()

    # Parse input (shared by both parts)
    # Pattern: device_name: output1 output2 ...
    # Device names are alphanumeric strings
    edges = []
    line_pattern = re.compile(r'^([a-zA-Z0-9]+):\s+(.+)$')
    with open(args.input, "r") as f:
        for line_num, line in enumerate(f.readlines(), 1):
            line = line.strip()
            if line:
                match = line_pattern.match(line)
                assert match, f"Line {line_num}: Invalid format (expected 'device: output1 output2 ...'): {line}"
                device = match.group(1)
                outputs_str = match.group(2)
                # Validate output names are alphanumeric
                outputs = outputs_str.split()
                for output in outputs:
                    assert re.match(r'^[a-zA-Z0-9]+$', output), f"Line {line_num}: Invalid output name '{output}'"
                edges.append((device, outputs))
    
    # Create network (will assert if not a DAG)
    network = DeviceNetwork(edges)

    # Part 1
    # Problem: Count all different paths from 'you' to 'out'
    # Data flows from device through its outputs (directed graph)
    #
    # Example network:
    #   you: a b
    #   a: out
    #   b: c
    #   c: out
    #
    # Paths: you → a → out, you → b → c → out
    # Total: 2 paths
    
    result1 = network.count_paths('you', 'out')
    
    if args.debug:
        print(f"Paths from 'you' to 'out': {result1}")
    
    print(f"Part 1: {result1}")

    # Part 2
    # Problem: Count paths from 'svr' to 'out' that visit both 'dac' and 'fft'
    # The path must pass through both devices (in any order) to be counted
    #
    # Solution: Break into segments and use multiplication principle
    # Paths = (svr→dac) × (dac→fft) × (fft→out) + (svr→fft) × (fft→dac) × (dac→out)
    
    # Paths that go through dac first, then fft
    paths_dac_first = (
        network.count_paths('svr', 'dac') *
        network.count_paths('dac', 'fft') *
        network.count_paths('fft', 'out')
    )
    
    # Paths that go through fft first, then dac
    paths_fft_first = (
        network.count_paths('svr', 'fft') *
        network.count_paths('fft', 'dac') *
        network.count_paths('dac', 'out')
    )
    
    result2 = paths_dac_first + paths_fft_first
    
    if args.debug:
        print("")
        print(f"Paths (svr→dac→fft→out): {paths_dac_first}")
        print(f"Paths (svr→fft→dac→out): {paths_fft_first}")
        print(f"Total paths: {result2}")
    
    print(f"Part 2: {result2}")
