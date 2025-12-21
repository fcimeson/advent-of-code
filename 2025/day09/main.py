#!/usr/bin/env python3
"""Advent of Code - Day 9 (Movie Theater)

Find the largest rectangle area using two red tiles as opposite corners.

Usage:
  python3 main.py input01.txt
  python3 main.py input02.txt -d
"""
import argparse
import re


class Tiles:
    """Store tile locations and provide visualization."""
    
    def __init__(self, tiles):
        """Initialize with a list of (x, y) coordinate tuples.
        
        Args:
            tiles: List of (x, y) coordinate tuples
        """
        self.tiles = list(tiles)
        self.tile_set = set(tiles)
        self._green_tiles_cache = None  # Cache for green tiles
        self._polygon_cache = None  # Cache for the polygon boundary
        self._is_green_cache = {}  # Cache for is_tile_green results
        self._green_rectangles = None  # Cache for rectangle decomposition
    
    def _render_grid(self, overlay_func=None):
        """Render the grid with optional overlay function.
        
        Args:
            overlay_func: Optional function(x, y) -> char or None
                         If returns a char, use it; if None, use default tile/empty
        
        Returns:
            String representation of the grid with border
        """
        if not self.tiles:
            return "No tiles"
        
        # Find bounds
        min_x = min(x for x, y in self.tiles)
        max_x = max(x for x, y in self.tiles)
        min_y = min(y for x, y in self.tiles)
        max_y = max(y for x, y in self.tiles)
        
        lines = []
        
        # Add top border
        width = max_x - min_x + 1
        lines.append("." * (width + 2))
        
        # Show grid (y increases downward in display)
        for y in range(min_y, max_y + 1):
            row = ['.']  # Left border
            for x in range(min_x, max_x + 1):
                # Check if overlay function provides a character
                if overlay_func:
                    overlay_char = overlay_func(x, y)
                    if overlay_char is not None:
                        row.append(overlay_char)
                        continue
                
                # Default: show tile or empty space
                if (x, y) in self.tile_set:
                    row.append('#')
                else:
                    row.append('.')
            row.append('.')  # Right border
            lines.append(''.join(row))
        
        # Add bottom border
        lines.append("." * (width + 2))
        
        return '\n'.join(lines)
    
    def __str__(self):
        """Return a string representation of the tile grid.
        
        Creates a visual grid where tiles are marked with '#' and empty spaces with '.'.
        Includes a border of '.' around the entire grid.
        Shows coordinate axes for reference.
        """
        if not self.tiles:
            return "No tiles"
        
        min_x = min(x for x, y in self.tiles)
        max_x = max(x for x, y in self.tiles)
        min_y = min(y for x, y in self.tiles)
        max_y = max(y for x, y in self.tiles)
        
        header = f"Tiles: {len(self.tiles)} tiles spanning x=[{min_x}, {max_x}], y=[{min_y}, {max_y}]\n\n"
        return header + self._render_grid()
    
    def show_rectangle(self, corner1, corner2):
        """Return a string visualization with a rectangle overlay.
        
        Shows tiles (#), empty spaces (.), and the selected rectangle area (O).
        The corner tiles are shown as 'X' for clarity.
        Includes a border of '.' around the entire grid.
        
        Args:
            corner1: First corner (x, y)
            corner2: Second corner (x, y)
        
        Returns:
            String representation with rectangle overlay
        """
        if not self.tiles:
            return "No tiles"
        
        x1, y1 = corner1
        x2, y2 = corner2
        
        # Normalize corners (min/max)
        rect_min_x = min(x1, x2)
        rect_max_x = max(x1, x2)
        rect_min_y = min(y1, y2)
        rect_max_y = max(y1, y2)
        
        # Calculate area
        area = (rect_max_x - rect_min_x + 1) * (rect_max_y - rect_min_y + 1)
        
        # Define overlay function for rectangle
        def overlay(x, y):
            # Check if this position is a corner
            if (x, y) == corner1 or (x, y) == corner2:
                return 'X'
            # Check if inside rectangle
            elif rect_min_x <= x <= rect_max_x and rect_min_y <= y <= rect_max_y:
                return 'O'
            # No overlay, use default
            return None
        
        header = f"Rectangle: corners {corner1} and {corner2}, area = {area}\n\n"
        return header + self._render_grid(overlay_func=overlay)
    
    def show_with_green(self):
        """Return a string visualization showing red and green tiles.
        
        Uses the class's tile data to compute green tiles.
        
        Returns:
            String representation with green tiles shown as 'X'
        """
        if not self.tiles:
            return "No tiles"
        
        # Get green tiles
        green_tiles = self.get_green_tiles()
        
        # Define overlay function for green tiles
        def overlay(x, y):
            if (x, y) in green_tiles:
                return 'X'  # Show green as X
            return None
        
        header = f"Red and Green tiles (Green shown as X):\n\n"
        return header + self._render_grid(overlay_func=overlay)
    
    def get_green_tiles(self):
        """Identify all green tiles based on red tile connections.
        
        Red tiles form a closed loop, connected by straight lines of green tiles.
        The order in self.tiles defines the connections (with wraparound).
        All tiles inside the loop are also green.
        
        Returns:
            Set of (x, y) coordinates of all green tiles
        """
        # Return cached result if available
        if self._green_tiles_cache is not None:
            return self._green_tiles_cache
        def is_inside_polygon(point, polygon):
            """Check if a point is inside a polygon using ray casting algorithm.
            
            Args:
                point: (x, y) coordinate
                polygon: List of (x, y) coordinates forming the polygon
            
            Returns:
                True if point is inside polygon, False otherwise
            """
            x, y = point
            n = len(polygon)
            inside = False
            
            j = n - 1
            for i in range(n):
                xi, yi = polygon[i]
                xj, yj = polygon[j]
                
                if ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / (yj - yi) + xi):
                    inside = not inside
                
                j = i
            
            return inside
        
        green_tiles = set()
        red_tiles = self.tiles
        n = len(red_tiles)
        
        # Add green tiles connecting adjacent red tiles
        for i in range(n):
            x1, y1 = red_tiles[i]
            x2, y2 = red_tiles[(i + 1) % n]  # Wraparound to first tile
            
            # Generate line of green tiles between red tiles
            if x1 == x2:  # Vertical line
                min_y, max_y = min(y1, y2), max(y1, y2)
                for y in range(min_y + 1, max_y):
                    green_tiles.add((x1, y))
            elif y1 == y2:  # Horizontal line
                min_x, max_x = min(x1, x2), max(x1, x2)
                for x in range(min_x + 1, max_x):
                    green_tiles.add((x, y1))
        
        # Find tiles inside the loop using point-in-polygon test (ray casting)
        # First, find the bounding box
        min_x = min(x for x, y in red_tiles)
        max_x = max(x for x, y in red_tiles)
        min_y = min(y for x, y in red_tiles)
        max_y = max(y for x, y in red_tiles)
        
        # Build the complete polygon (red tiles + green connecting tiles)
        polygon = []
        for i in range(n):
            x1, y1 = red_tiles[i]
            x2, y2 = red_tiles[(i + 1) % n]
            polygon.append((x1, y1))
            
            # Add intermediate green tiles
            if x1 == x2:  # Vertical
                min_y_seg, max_y_seg = min(y1, y2), max(y1, y2)
                step = 1 if y2 > y1 else -1
                for y in range(y1 + step, y2, step):
                    polygon.append((x1, y))
            elif y1 == y2:  # Horizontal
                min_x_seg, max_x_seg = min(x1, x2), max(x1, x2)
                step = 1 if x2 > x1 else -1
                for x in range(x1 + step, x2, step):
                    polygon.append((x, y1))
        
        # Check each point in bounding box
        all_boundary = set(polygon) | set(red_tiles)
        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                if (x, y) not in all_boundary:
                    # Point-in-polygon test using ray casting
                    if is_inside_polygon((x, y), polygon):
                        green_tiles.add((x, y))
        
        # Cache the result
        self._green_tiles_cache = green_tiles
        return green_tiles
    
    def _get_polygon(self):
        """Get the polygon formed by red tiles and connecting green tiles.
        
        Returns cached polygon if available.
        
        Returns:
            List of (x, y) coordinates forming the complete polygon
        """
        if self._polygon_cache is not None:
            return self._polygon_cache
        
        red_tiles = self.tiles
        n = len(red_tiles)
        polygon = []
        
        for i in range(n):
            x1, y1 = red_tiles[i]
            x2, y2 = red_tiles[(i + 1) % n]
            polygon.append((x1, y1))
            
            # Add intermediate green tiles
            if x1 == x2:  # Vertical
                step = 1 if y2 > y1 else -1
                for y in range(y1 + step, y2, step):
                    polygon.append((x1, y))
            elif y1 == y2:  # Horizontal
                step = 1 if x2 > x1 else -1
                for x in range(x1 + step, x2, step):
                    polygon.append((x, y1))
        
        self._polygon_cache = polygon
        return polygon
    
    def _decompose_into_rectangles(self):
        """Decompose the green region into a set of non-overlapping rectangles.
        
        Uses horizontal scanline algorithm for rectilinear polygons.
        
        Returns:
            List of rectangles as (min_x, min_y, max_x, max_y) tuples
        """
        if self._green_rectangles is not None:
            return self._green_rectangles
        
        red_tiles = self.tiles
        n = len(red_tiles)
        
        # Collect all unique y-coordinates (horizontal scanlines)
        y_coords = sorted(set(y for x, y in red_tiles))
        
        rectangles = []
        
        # For each horizontal strip between consecutive y-coordinates
        for i in range(len(y_coords) - 1):
            y_bottom = y_coords[i]
            y_top = y_coords[i + 1]
            y_mid = (y_bottom + y_top) / 2  # Sample point in the middle of strip
            
            # Find all x-intervals that are inside the polygon at this y-level
            # Use ray casting to find x-ranges
            x_intervals = []
            
            # Collect all x-coordinates where polygon edges cross this y-level
            x_crossings = []
            for j in range(n):
                x1, y1 = red_tiles[j]
                x2, y2 = red_tiles[(j + 1) % n]
                
                # Check if this edge crosses the scanline y=y_mid
                if min(y1, y2) < y_mid < max(y1, y2):
                    # Vertical edge or slanted - find x at y_mid
                    if y1 != y2:
                        x_cross = x1 + (x2 - x1) * (y_mid - y1) / (y2 - y1)
                        x_crossings.append(x_cross)
                elif y1 == y2 == y_mid:
                    # Horizontal edge exactly on scanline - special case
                    # Add both endpoints
                    x_crossings.extend([x1, x2])
            
            # Sort crossings and pair them up (inside between odd/even pairs)
            x_crossings.sort()
            
            # Remove duplicates and pair up
            if len(x_crossings) >= 2:
                # Simple pairing: alternate between inside and outside
                for k in range(0, len(x_crossings) - 1, 2):
                    x_left = x_crossings[k]
                    x_right = x_crossings[k + 1]
                    if x_left < x_right:
                        x_intervals.append((x_left, x_right))
            
            # Create rectangles for each x-interval in this horizontal strip
            for x_left, x_right in x_intervals:
                rectangles.append((x_left, y_bottom, x_right, y_top))
        
        self._green_rectangles = rectangles
        return rectangles
    
    def is_tile_green(self, x, y):
        """Check if a specific tile is green.
        
        A tile is green if it's:
        1. On a line connecting two adjacent red tiles, OR
        2. Inside the loop formed by red tiles
        
        Uses rectangle decomposition for O(R) lookup where R = number of rectangles.
        
        Args:
            x, y: Coordinates to check
        
        Returns:
            True if tile is green, False otherwise
        """
        # Check cache first
        if (x, y) in self._is_green_cache:
            return self._is_green_cache[(x, y)]
        
        # Get rectangle decomposition
        rectangles = self._decompose_into_rectangles()
        
        # Check if point is inside any rectangle
        # Note: rectangles use inclusive bounds for green region
        for min_x, min_y, max_x, max_y in rectangles:
            if min_x <= x <= max_x and min_y <= y <= max_y:
                self._is_green_cache[(x, y)] = True
                return True
        
        # Not in any rectangle
        self._is_green_cache[(x, y)] = False
        return False
    
    def _segments_intersect(self, p1, p2, p3, p4):
        """Check if line segment p1-p2 properly intersects with line segment p3-p4.
        
        Returns True only for proper intersections (crossing through),
        not for touching at endpoints or collinear overlaps.
        
        Args:
            p1, p2: Endpoints of first segment (x, y)
            p3, p4: Endpoints of second segment (x, y)
        
        Returns:
            True if segments properly intersect (cross through each other)
        """
        x1, y1 = p1
        x2, y2 = p2
        x3, y3 = p3
        x4, y4 = p4
        
        def sign(val):
            """Return sign of value: -1, 0, or 1."""
            if val > 0:
                return 1
            elif val < 0:
                return -1
            return 0
        
        def cross_product(o, a, b):
            """Cross product of vectors OA and OB."""
            return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
        
        # Calculate cross products
        cp1 = cross_product(p1, p2, p3)
        cp2 = cross_product(p1, p2, p4)
        cp3 = cross_product(p3, p4, p1)
        cp4 = cross_product(p3, p4, p2)
        
        # Proper intersection: segments cross (signs differ and non-zero)
        if sign(cp1) * sign(cp2) < 0 and sign(cp3) * sign(cp4) < 0:
            return True
        
        return False
    
    def is_rectangle_valid(self, corner1, corner2):
        """Check if all tiles in a rectangle are red or green.
        
        Strategy: Check the other two corners with is_tile_green() (fast with
        rectangle decomposition), then verify rectangle edges don't cross
        polygon boundary.
        
        Args:
            corner1: First corner (x, y) - guaranteed to be a red tile
            corner2: Second corner (x, y) - guaranteed to be a red tile
        
        Returns:
            True if all tiles in rectangle are red or green, False otherwise
        """
        x1, y1 = corner1
        x2, y2 = corner2
        
        rect_min_x, rect_max_x = min(x1, x2), max(x1, x2)
        rect_min_y, rect_max_y = min(y1, y2), max(y1, y2)
        
        # corner1 and corner2 are red tiles, but we need to check the OTHER two corners
        other_corners = []
        for corner in [(rect_min_x, rect_min_y), (rect_max_x, rect_min_y),
                      (rect_max_x, rect_max_y), (rect_min_x, rect_max_y)]:
            if corner != corner1 and corner != corner2:
                other_corners.append(corner)
        
        # Check if the other two corners are red or green
        for corner in other_corners:
            if corner not in self.tile_set and not self.is_tile_green(corner[0], corner[1]):
                return False
        
        # Second check: rectangle edges shouldn't cross polygon boundary
        rect_edges = [
            ((rect_min_x, rect_min_y), (rect_max_x, rect_min_y)),  # Top
            ((rect_max_x, rect_min_y), (rect_max_x, rect_max_y)),  # Right
            ((rect_max_x, rect_max_y), (rect_min_x, rect_max_y)),  # Bottom
            ((rect_min_x, rect_max_y), (rect_min_x, rect_min_y)),  # Left
        ]
        
        # Check against each polygon edge (red tile connections)
        n = len(self.tiles)
        for i in range(n):
            poly_p1 = self.tiles[i]
            poly_p2 = self.tiles[(i + 1) % n]
            
            # Quick bounding box check: skip polygon edges that can't possibly intersect
            poly_min_x = min(poly_p1[0], poly_p2[0])
            poly_max_x = max(poly_p1[0], poly_p2[0])
            poly_min_y = min(poly_p1[1], poly_p2[1])
            poly_max_y = max(poly_p1[1], poly_p2[1])
            
            # If polygon edge bounding box doesn't overlap rectangle bounding box, skip
            if poly_max_x < rect_min_x or poly_min_x > rect_max_x or \
               poly_max_y < rect_min_y or poly_min_y > rect_max_y:
                continue
            
            # Determine if polygon edge is horizontal or vertical
            poly_is_horizontal = (poly_p1[1] == poly_p2[1])
            poly_is_vertical = (poly_p1[0] == poly_p2[0])
            
            # Check if this polygon edge intersects any rectangle edge
            for rect_p1, rect_p2 in rect_edges:
                # Skip parallel segments (they can't properly intersect)
                rect_is_horizontal = (rect_p1[1] == rect_p2[1])
                rect_is_vertical = (rect_p1[0] == rect_p2[0])
                
                if (poly_is_horizontal and rect_is_horizontal) or \
                   (poly_is_vertical and rect_is_vertical):
                    continue  # Parallel segments, skip
                
                if self._segments_intersect(poly_p1, poly_p2, rect_p1, rect_p2):
                    # Intersection found - rectangle crosses boundary
                    return False
        
        return True


def calculate_rectangle_area(corner1, corner2):
    """Calculate rectangle area given two opposite corners.
    
    Coordinates are inclusive, so a rectangle from (0,0) to (0,0) has area 1.
    
    Args:
        corner1: First corner (x, y)
        corner2: Second corner (x, y)
    
    Returns:
        Area of the rectangle (inclusive of boundaries)
    
    Examples:
        >>> calculate_rectangle_area((0, 0), (2, 3))
        12  # 3 units wide × 4 units tall
        >>> calculate_rectangle_area((5, 5), (5, 5))
        1   # Single tile
    """
    x1, y1 = corner1
    x2, y2 = corner2
    
    width = abs(x2 - x1) + 1
    height = abs(y2 - y1) + 1
    
    return width * height


def find_largest_rectangle(tiles_obj, debug=False, green_only=False):
    """Find the largest rectangle formed by any two tiles as opposite corners.
    
    Optimization: Sort tiles and use pruning to skip pairs that can't beat max_area.
    
    Args:
        tiles_obj: Tiles object containing tile locations
        debug: If True, print debug information
        green_only: If True, only consider rectangles with all red/green tiles
    
    Returns:
        Tuple of (max_area, best_corners) where best_corners is (corner1, corner2)
    """
    tiles = tiles_obj.tiles
    max_area = 0
    best_corners = None
    n = len(tiles)
    checked_count = 0
    validated_count = 0
    
    # Sort tiles by x-coordinate (then y as tiebreaker) for better pruning
    sorted_tiles = sorted(tiles, key=lambda t: (t[0], t[1]))
    
    # For green_only mode, initialize with a reasonable lower bound
    # Check a small sample of rectangles to get a starting max_area
    if green_only and n > 50:
        sample_size = min(20, n)
        for i in range(0, sample_size, 2):
            for j in range(i + 1, min(i + 10, n)):
                area = calculate_rectangle_area(sorted_tiles[i], sorted_tiles[j])
                if area > max_area and tiles_obj.is_rectangle_valid(sorted_tiles[i], sorted_tiles[j]):
                    max_area = area
                    best_corners = (sorted_tiles[i], sorted_tiles[j])
    
    # Precompute max y-distance for pruning
    # For each tile, we need to know max y-distance to any tile with x >= current x
    max_y_from_here = []
    for i in range(n):
        # Max y-distance from tile i to any tile j >= i
        if i < n - 1:
            max_dy = max(abs(sorted_tiles[i][1] - sorted_tiles[j][1]) for j in range(i + 1, n))
        else:
            max_dy = 0
        max_y_from_here.append(max_dy)
    
    for i in range(n):
        # Pruning: Skip this tile if max possible area with remaining tiles can't beat current max
        max_x_from_here = sorted_tiles[-1][0] - sorted_tiles[i][0] if i < n - 1 else 0
        max_possible_area = (max_x_from_here + 1) * (max_y_from_here[i] + 1)
        if max_possible_area <= max_area:
            continue
        
        for j in range(i + 1, n):
            x1, y1 = sorted_tiles[i]
            x2, y2 = sorted_tiles[j]
            
            # Calculate area
            area = calculate_rectangle_area(sorted_tiles[i], sorted_tiles[j])
            
            # Early skip: if this area can't beat current max, don't validate
            if area <= max_area:
                continue
            
            checked_count += 1
            
            # If green_only mode, validate the rectangle
            if green_only:
                validated_count += 1
                if tiles_obj.is_rectangle_valid(sorted_tiles[i], sorted_tiles[j]):
                    max_area = area
                    best_corners = (sorted_tiles[i], sorted_tiles[j])
            else:
                max_area = area
                best_corners = (sorted_tiles[i], sorted_tiles[j])
    
    if debug:
        print(f"Stats: checked {checked_count} rectangles, validated {validated_count}")
    
    return max_area, best_corners


if __name__ == "__main__":
    # Args
    parser = argparse.ArgumentParser(description="Advent of Code Day 9")
    parser.add_argument("input", help="input file")
    parser.add_argument("-d", "--debug", action="store_true", help="enable debug output")
    args = parser.parse_args()

    # Parse input (shared by both parts)
    red_tiles = []
    # Pattern: x,y where x and y are integers (can be negative)
    coord_pattern = re.compile(r'^(-?\d+),(-?\d+)$')
    with open(args.input, "r") as f:
        for line_num, line in enumerate(f.readlines(), 1):
            line = line.strip()
            if line:
                match = coord_pattern.match(line)
                assert match, f"Line {line_num}: Invalid coordinate format (expected 'x,y'): {line}"
                x, y = int(match.group(1)), int(match.group(2))
                red_tiles.append((x, y))

    # Create Tiles object
    tiles = Tiles(red_tiles)
    
    if args.debug:
        print("Initial environment:")
        print(tiles)
        print()

    # Part 1
    # Problem: Find the largest rectangle area where two red tiles are opposite corners
    # Opposite corners means (x1,y1) and (x2,y2) form a rectangle
    # Coordinates are inclusive, so area = (abs(x2-x1)+1) * (abs(y2-y1)+1)
    #
    # Example:
    #   Tiles at (0,0) and (2,3) form a 3×4 rectangle with area 12
    #   Tiles at (5,5) and (5,5) form a 1×1 rectangle with area 1
    
    result1, best_corners = find_largest_rectangle(tiles, debug=args.debug)
    
    if args.debug and best_corners:
        print("Final solution:")
        print(f"Max area: {result1} with corners {best_corners[0]} and {best_corners[1]}")
        print(tiles.show_rectangle(best_corners[0], best_corners[1]))
        print()
    
    print(f"Part 1: {result1}")

    # Part 2
    # Problem: Rectangle can only include red or green tiles
    # Red tiles form a closed loop connected by green tiles
    # All tiles inside the loop are also green
    
    if args.debug:
        print("Red and Green tiles:")
        print(tiles.show_with_green())
        print()
    
    result2, best_corners2 = find_largest_rectangle(tiles, debug=args.debug, green_only=True)
    
    if args.debug and best_corners2:
        print("Part 2 Final solution:")
        print(f"Max area: {result2} with corners {best_corners2[0]} and {best_corners2[1]}")
        print(tiles.show_rectangle(best_corners2[0], best_corners2[1]))
        print()
    
    print(f"Part 2: {result2}")
