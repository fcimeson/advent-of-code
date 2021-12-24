#!/usr/bin/env python3

import enum
import re
import sys
import copy
import math
import numpy
import pickle
import argparse

INF = float('inf')
RE_NUMBER = r'-?\d+'

def delta(point01, point02):
    dx = point02[0] - point01[0]
    dy = point02[1] - point01[1]
    dz = point02[2] - point01[2]
    return dx,dy,dz    

def dist(point01, point02):
    # PRECISION = 10
    dx,dy,dz = delta(point01, point02)
    # d = math.sqrt(dx**2 + dy**2 + dz**2)
    # d = int(10**PRECISION * round(d, PRECISION))
    return dx**2 + dy**2 + dz**2

class Edge:
    def __init__(self, i, j, weight):
        self.i = i
        self.j = j
        self.weight = weight
    
    def __str__(self):
        return f"({self.weight}, {self.i}, {self.j})"

class Scanner:
    def __init__(self, index):
        self.index = index
        self.translation = numpy.zeros((3,1), dtype=int)
        self.rotation_matrix = numpy.identity(3, dtype=int)

        self.scans = []
        self.graph = None
        self.unique_edges_by_weight = None
    
    def __str__(self):
        s = f"Scanner {self.index}\n"
        data = []
        for i in range(len(self.scans)):
            data.append([self.get_scan(i), i])
        data = sorted(data, key = lambda x : list(x[0]) + [x[1]])
        for scan, index in data:
            s += f"  {scan}, index = {index}\n"
        return s

    def size(self):
        return len(self.scans)
    
    def get_scan(self, index):
        x = self.rotation_matrix.dot(self.scans[index].T).T + self.translation.T
        return x.reshape(3)

    def get_scans(self):
        scans = []
        for i in range(len(self.scans)):
            scans.append(self.get_scan(i))
        scans = sorted(scans, key = lambda x: tuple(x))
        return scans
    
    def set_rotation(self, rotation_matrix):
        self.rotation_matrix = rotation_matrix

    def set_translation(self, translation):
        self.translation = translation

    def reset_rotation(self):
        self.rotation_matrix = numpy.identity(3, dtype=int)
    
    def reset_translation(self):
        self.translation = numpy.zeros((3,1), dtype=int)
    
    def add_scan(self,x,y,z):
        self.scans.append(numpy.array([x,y,z], dtype=int))
    
    def build_graph(self, debug=False):
        N = len(self.scans)
        self.scans = sorted(self.scans, key=lambda x: tuple(x))
        self.unique_edges_by_weight = []
        self.graph = numpy.zeros(shape=(N,N), dtype=int)
        for index01, point01 in enumerate(self.scans):
            for index02 in range(index01,N):
                point02 = self.scans[index02]
                d = dist(point01, point02)
                self.graph[index01,index02] = d
                self.graph[index02,index01] = d
                if d > 0:
                    self.unique_edges_by_weight.append(Edge(index01, index02, d))
        self.unique_edges_by_weight = sorted(self.unique_edges_by_weight, key=lambda edge: edge.weight)
        if debug:
            for edge in self.unique_edges_by_weight:
                print(edge)

class SubGraphIsomorphism:
    def __init__(self, scanner01, scanner02):
        self.scanner01 = scanner01
        self.scanner02 = scanner02
        self.map = {}

    def __str__(self):
        s = f"Scanner {self.scanner01.index} => Scanner {self.scanner02.index} (size = {self.size()})\n"
        for i01, i02 in self.map.items():
            s += f"  {i01} => {i02}\n"
        return s
    
    def get_map(self, i01=None):
        if i01 is not None:
            if i01 in self.map:
                return self.map[i01]
            return None
        return self.map
    
    def get_coordinates(self):
        coordinates = []
        for i01 in self.map:
            coordinates.append(self.scanner01.scans[i01])
        return coordinates

    def size(self):
        return len(self.map)

    def add(self, j01, j02):
        self.map[j01] = j02

    def test_edge_addition(self, j01, j02):
        if j01 in self.map:
            if self.map[j01] == j02:
                return True
            else:
                return False
        for i01, i02 in self.map.items():
            if self.scanner01.graph[i01][j01] != self.scanner02.graph[i02][j02]:
                return False
        return True            


def find_subgraph_isomorphism(scanner01, scanner02, debug=False):
    """Assume a matched weigth => a matched edge"""

    matched_edges = []
    index02 = 0
    edge02 = scanner02.unique_edges_by_weight[index02]
    for index01, edge01 in enumerate(scanner01.unique_edges_by_weight):
        while edge02.weight < edge01.weight and index02+1 < len(scanner02.unique_edges_by_weight):
            index02 += 1
            edge02 = scanner02.unique_edges_by_weight[index02]
        if edge01.weight == edge02.weight:
            matched_edges.append((edge01, edge02))
            if scanner01.index == 1 and scanner02.index == 9 and edge01.weight == 1613013:
                print(160, edge01, edge02)

    maps = []
    for edge01, edge02 in matched_edges:
        i01 = edge01.i
        j01 = edge01.j 
        i02 = edge02.i
        j02 = edge02.j
        
        mapped = False
        new_maps = []
        while len(maps) > 0:
            map = maps.pop()
            
            if map.get_map(i01) == i02 and map.get_map(j01) == j02:
                new_maps.append(map)
                mapped = True
                continue
            
            if map.get_map(i01) == j02 and map.get_map(j01) == i02:
                new_maps.append(map)
                mapped = True
                continue
            
            if map.get_map(i01) is None or map.get_map(j01) is None:
                
                # i => i
                new_map = copy.deepcopy(map)
                if new_map.test_edge_addition(i01, i02):
                    new_map.add(i01, i02)
                    if new_map.test_edge_addition(j01, j02):
                        new_map.add(j01, j02)
                        new_maps.append(new_map)
                        mapped = True

                # i => j
                new_map = copy.deepcopy(map)
                if new_map.test_edge_addition(i01, j02):
                    new_map.add(i01, j02)
                    if new_map.test_edge_addition(j01, i02):
                        new_map.add(j01, i02)
                        mapped = True
                
            if mapped: continue
            new_maps.append(map)

        if not mapped:
            new_map = SubGraphIsomorphism(scanner01, scanner02)
            new_map.add(i01,i02)
            new_map.add(j01,j02)
            maps.append(new_map)
            new_map = SubGraphIsomorphism(scanner01, scanner02)
            new_map.add(i01,j02)
            new_map.add(j01,i02)
            new_maps.append(new_map)
        maps.extend(new_maps)
        
        # if debug:
        #     print(f"Found maps for edges {edge01} and {edge02}")
        #     for map in maps:
        #         print(map)
        #     input("Press any key")
    
    # Find the map with the most matches
    if len(maps) > 0:
        largest_map = maps[0]
        for map in maps[1:]:
            if map.size() > largest_map.size():
                largest_map = map
        return largest_map
    return SubGraphIsomorphism(scanner01, scanner02)

def orient_02_to_01(scanner01, scanner02, isomorphisim):
    assert scanner01.index == isomorphisim.scanner01.index
    assert scanner02.index == isomorphisim.scanner02.index
    scanner01.reset_rotation()
    scanner01.reset_translation()

    # Find rotation
    x_rotated = y_rotated = z_rotated = False
    rotation_matrix = numpy.zeros((3,3), dtype=int)
    for i01, i02 in isomorphisim.map.items():
        for j01, j02 in isomorphisim.map.items():
            if i01 != i02:
                dx01, dy01, dz01 = delta(scanner01.scans[i01], scanner01.scans[j01])
                dx02, dy02, dz02 = delta(scanner02.scans[i02], scanner02.scans[j02])
                
                # Use unique x deltas to understand which axis is actually the x-axis
                if not x_rotated and abs(dx01) > 0 and abs(dx01) != abs(dy01) and abs(dx01) != abs(dz01):
                    assert abs(dx01) == abs(dx02) or abs(dx01) == abs(dy02) or abs(dx01) == abs(dz02)
                    if abs(dx01) == abs(dx02):
                        rotation_matrix[0][0] = dx02//dx01
                    elif abs(dx01) == abs(dy02):
                        rotation_matrix[0][1] = dy02//dx01
                    elif abs(dx01) == abs(dz02):
                        rotation_matrix[0][2] = dz02//dx01
                    x_rotated = True

                # Use unique y deltas to understand which axis is actually the y-axis
                if not y_rotated and abs(dy01) > 0 and abs(dy01) != abs(dx01) and abs(dy01) != abs(dz01):
                    assert abs(dy01) == abs(dx02) or abs(dy01) == abs(dy02) or abs(dy01) == abs(dz02)
                    if abs(dy01) == abs(dx02):
                        rotation_matrix[1][0] = dx02//dy01
                    elif abs(dy01) == abs(dy02):
                        rotation_matrix[1][1] = dy02//dy01
                    elif abs(dy01) == abs(dz02):
                        rotation_matrix[1][2] = dz02//dy01
                    y_rotated = True

                # Use unique z deltas to understand which axis is actually the z-axis
                if not z_rotated and abs(dz01) > 0 and abs(dz01) != abs(dx01) and abs(dz01) != abs(dy01):
                    assert abs(dz01) == abs(dx02) or abs(dz01) == abs(dy02) or abs(dz01) == abs(dz02)
                    if abs(dz01) == abs(dx02):
                        rotation_matrix[2][0] = dx02//dz01
                    elif abs(dz01) == abs(dy02):
                        rotation_matrix[2][1] = dy02//dz01
                    elif abs(dz01) == abs(dz02):
                        rotation_matrix[2][2] = dz02//dz01
                    z_rotated = True

            if x_rotated and y_rotated and z_rotated:
                break
        if x_rotated and y_rotated and z_rotated:
            break
    assert x_rotated and y_rotated and z_rotated
    scanner02.set_rotation(rotation_matrix)

    # Find translation
    translation = None
    for i01, i02 in isomorphisim.map.items():
        scan02 = scanner02.get_scan(i02)
        dx, dy, dz = delta(scanner01.scans[i01], scan02)
        translation = numpy.array([-dx,-dy,-dz], dtype=int)
        break
    scanner02.set_translation(translation)
    
    # Check
    for i01, i02 in isomorphisim.map.items():
        scan02 = scanner02.get_scan(i02)
        dx, dy, dz = delta(scanner01.scans[i01], scan02)
        assert dx == 0 and dy == 0 and dz == 0

def merge_02_into_01(scanner01, scanner02):
    for scan02 in scanner02.get_scans():
        duplicate = None
        for scan01 in scanner01.get_scans():
            if (scan01 == scan02).all():
                duplicate = scan01
                break
        if duplicate is not None:
            continue
        scanner01.add_scan(scan02[0], scan02[1], scan02[2])
    scanner01.build_graph()


if __name__ == "__main__":
    
    # Args
    parser = argparse.ArgumentParser(description='Advent of Code')
    parser.add_argument('input', help='input file')
    parser.add_argument('--days', type=int, default=80, help='length of simulation')
    parser.add_argument('--pickle', choices=['load', 'save', None], default=None, help='Pickle RICK!!!')
    parser.add_argument('-d', '--debug', action='store_true', help='enable debug code')
    args = parser.parse_args()

    # Data
    scanners = []
    scanner = None
    with open(args.input, 'r') as f:
        for line in f.readlines():
            if re.match(r'--- scanner \d+ ---', line):
                index = int(re.findall('\d+', line)[0])
                scanner = Scanner(index)
                scanners.append(scanner)
            elif re.match(r'^%s,%s,%s$' % (RE_NUMBER,RE_NUMBER,RE_NUMBER), line):
                coordinates = [int(x) for x in re.findall(RE_NUMBER, line)]
                scanner.add_scan(coordinates[0], coordinates[1], coordinates[2])
            elif not re.match(r'^\s*$', line):
                print("ERROR", line)
                sys.exit()
    for scanner in scanners:
        scanner.build_graph()

    # Solve
    unoriented_scanners = []
    number_of_scanners = len(scanners)
    while len(scanners) + len(unoriented_scanners) > 1:
        scanner01 = scanners.pop(0)
        for i02, scanner02 in enumerate(scanners):
            if scanner02.index == 0:
                continue
            # Debug (load problem instance)
            if args.pickle == 'load':
                with open('scanner01.pickle', 'rb') as f:
                    scanner01 = pickle.load(f)
                with open('scanner09.pickle', 'rb') as f:
                    scanner02 = pickle.load(f)
            isomorphism = find_subgraph_isomorphism(scanner01, scanner02, args.debug)
            if args.debug:
                print(isomorphism)
            if isomorphism.size() >= 12:

                # Debug (save problem instance)
                if args.pickle == 'save' and scanner01.index == 1 and scanner02.index == 9:
                    with open('scanner01.pickle', 'wb') as f:
                        pickle.dump(scanner01, f)
                    with open('scanner09.pickle', 'wb') as f:
                        pickle.dump(scanner02, f)

                # Debug
                # if args.debug and scanner01.index == 1 and scanner02.index == 9:
                #     print(scanner01)
                #     print(scanner02)
                #     print("Scanner01 Edges")
                #     for edge in scanner01.unique_edges_by_weight:
                #         print("  ", edge)
                #     print("Scanner02 Edges")
                #     for edge in scanner02.unique_edges_by_weight:
                #         print("  ", edge)
                #     sys.exit()
                
                orient_02_to_01(scanner01, scanner02, isomorphism)
                expected_size = scanner01.size() + scanner02.size() - isomorphism.size()
                merge_02_into_01(scanner01, scanner02)
                scanners.pop(i02)

                # Debug
                if scanner01.size() != expected_size:
                    print(f"scanner01.size() = {scanner01.size()}, expected = {expected_size}")
                    print(isomorphism)
                    print(scanner01)
                    print(scanner02)
                assert scanner01.size() == expected_size

                if args.debug:
                    print(f"Merged {scanner02.index} into {scanner01.index}")
                break

        unoriented_scanners.append(scanner01)
        if len(scanners) == 0:
            scanners.extend(unoriented_scanners)
            unoriented_scanners = []
            if len(scanners) == number_of_scanners:
                break
            number_of_scanners = len(scanners)
        if args.debug:
            print(f"len(scanners) = {len(scanners)}, len(unoriented) = {len(unoriented_scanners)}")

    # Count the number of beacons
    number_of_beacons = 0
    for scanner in scanners:
        number_of_beacons += scanner.size()
    print(f"There are {number_of_beacons} beacons and {len(scanners)} disconnected environments.")

# Bug (the following coordinates are not matched)
    # Scanner 1
    # [-894 -241 1720], index = 45
    # [-840 -340 1746], index = 50
    # [-795 -232 1790], index = 56

    # Scanner 9
    # [-894 -241 1720], index = 66
    # [-840 -340 1746], index = 63
    # [-795 -232 1790], index = 60