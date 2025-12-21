#!/usr/bin/env python3
"""Advent of Code - Day 8 (Playground)

Connect junction boxes to form circuits using a union-find approach.
Make 1000 shortest connections and find product of 3 largest circuit sizes.

Usage:
  python3 main.py input01.txt
  python3 main.py input02.txt -d
"""
import argparse
import math
import re


class JunctionBoxes:
    """Container for junction box positions with distance calculations.
    
    Stores 3D coordinates of junction boxes and provides methods to query
    positions and calculate distances between boxes.
    """
    
    def __init__(self, positions):
        """Initialize with list of junction box positions.
        
        Args:
            positions: List of (x, y, z) tuples representing box coordinates
        """
        self.positions = list(positions)
    
    def __len__(self):
        """Return number of junction boxes."""
        return len(self.positions)
    
    def distance(self, i, j):
        """Calculate distance between two junction boxes.
        
        Args:
            i: Index of first junction box
            j: Index of second junction box
        
        Returns:
            Euclidean distance between boxes i and j
        """
        return math.sqrt(sum((a - b) ** 2 for a, b in zip(self.positions[i], self.positions[j])))
    
    def get_position(self, i):
        """Get position of a junction box.
        
        Args:
            i: Index of junction box
        
        Returns:
            Tuple (x, y, z) of junction box coordinates
        """
        return self.positions[i]


class Graph:
    """Graph of junction box connections.
    
    Tracks edges between junction boxes as they are connected.
    Provides method to find connected components.
    """
    
    def __init__(self, n):
        """Initialize graph for n junction boxes.
        
        Args:
            n: Number of junction boxes (nodes)
        """
        self.n = n
        self.adjacency = [set() for _ in range(n)]
    
    def add_edge(self, i, j):
        """Add an edge between two junction boxes.
        
        Args:
            i: First junction box index
            j: Second junction box index
        """
        self.adjacency[i].add(j)
        self.adjacency[j].add(i)
    
    def get_connected_component(self, start_node):
        """Get all nodes in the connected component containing start_node.
        
        Uses BFS to find all nodes reachable from start_node.
        
        Args:
            start_node: Node to start search from
        
        Returns:
            Set of node indices in the connected component
        """
        visited = set()
        queue = [start_node]
        visited.add(start_node)
        
        while queue:
            node = queue.pop(0)
            
            for neighbor in self.adjacency[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        
        return visited
    
    def is_fully_connected(self):
        """Check if all nodes are in a single connected component.
        
        Returns:
            True if all nodes are connected, False otherwise
        """
        if self.n == 0:
            return True
        
        # Get component starting from node 0
        component = self.get_connected_component(0)
        
        # If component contains all nodes, graph is fully connected
        return len(component) == self.n


if __name__ == "__main__":
    # Args
    parser = argparse.ArgumentParser(description="Advent of Code Day 8")
    parser.add_argument("input", help="input file")
    parser.add_argument("-d", "--debug", action="store_true", help="enable debug output")
    args = parser.parse_args()

    # Parse input (shared by both parts)
    positions = []
    # Pattern: x,y,z where x, y, z are integers (can be negative)
    coord_pattern = re.compile(r'^(-?\d+),(-?\d+),(-?\d+)$')
    with open(args.input, "r") as f:
        for line_num, line in enumerate(f.readlines(), 1):
            line = line.strip()
            if line:
                match = coord_pattern.match(line)
                assert match, f"Line {line_num}: Invalid coordinate format (expected 'x,y,z'): {line}"
                x, y, z = int(match.group(1)), int(match.group(2)), int(match.group(3))
                positions.append((x, y, z))

    # Create junction boxes container
    junctions = JunctionBoxes(positions)

    # Part 1
    # Problem: Connect the 1000 closest pairs of junction boxes
    # Build graph of connections, then find all circuits (connected components)
    # Find product of 3 largest circuit sizes
    
    n = len(junctions)
    graph = Graph(n)
    
    # Calculate all pairwise distances
    distances = []
    for i in range(n):
        for j in range(i + 1, n):
            dist = junctions.distance(i, j)
            distances.append((dist, i, j))
    
    # Sort by distance
    distances.sort()
    
    # Make connections (up to 1000 or until we run out)
    # For sample input (20 boxes), use 10 connections as shown in problem
    connections_made = 0
    if n <= 20:
        num_connections = min(10, len(distances))
    else:
        num_connections = min(1000, len(distances))
    
    for dist, i, j in distances:
        if connections_made >= num_connections:
            break
        
        graph.add_edge(i, j)
        connections_made += 1
        
        if args.debug and connections_made <= 10:
            print(f"Connection {connections_made}: {i} <-> {j} (dist={dist:.2f})")
    
    # Find all circuits (connected components)
    circuits = []
    open_nodes = set(range(n))
    
    while open_nodes:
        # Pick any node from open_nodes
        start_node = open_nodes.pop()
        
        # Get all nodes in this connected component
        circuit = graph.get_connected_component(start_node)
        
        # Remove all nodes in this circuit from open_nodes
        open_nodes -= circuit
        
        # Add circuit to list
        circuits.append(circuit)
    
    # Get circuit sizes and find product of 3 largest (or all if fewer than 3)
    sizes = [len(c) for c in circuits]
    sizes.sort(reverse=True)
    
    # Multiply the 3 largest, or all circuits if fewer than 3
    result1 = 1
    for size in sizes[:3]:
        result1 *= size
    
    if args.debug:
        print(f"Circuit sizes: {sizes}")
    
    print(f"Part 1: {result1}")

    # Part 2
    # Continue adding edges until all boxes form a single circuit
    # Return product of X coordinates of the last edge added
    
    # Reset graph and rebuild from scratch
    graph2 = Graph(n)
    last_edge = None
    
    # Add edges in distance order until fully connected
    for dist, i, j in distances:
        graph2.add_edge(i, j)
        last_edge = (i, j)
        
        if graph2.is_fully_connected():
            break
    
    if last_edge is not None:
        i, j = last_edge
        x_i = junctions.get_position(i)[0]  # X coordinate of node i
        x_j = junctions.get_position(j)[0]  # X coordinate of node j
        result2 = x_i * x_j
        
        if args.debug:
            print(f"Last edge to connect all: {i} <-> {j}")
            print(f"Positions: {junctions.get_position(i)} and {junctions.get_position(j)}")
            print(f"X coordinates: {x_i} * {x_j} = {result2}")
    else:
        result2 = 0
    
    print(f"Part 2: {result2}")
