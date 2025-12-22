#!/usr/bin/env python3
"""Advent of Code - Day 10 (Factory)

Unified integer linear programming solution for button-press optimization.

Both parts solve the SAME integer linear programming problem:
    minimize sum(x) subject to Ax ≡ b (mod m), x ∈ ℤ≥0
    
where:
    - A[i][j] = 1 if button j affects constraint i
    - x[j] = number of times button j is pressed (non-negative integer)
    - b[i] = target value for constraint i
    - m = modulus (2 for Part 1, ∞ for Part 2)

The ONLY difference is the modulo:
    - Part 1: Ax ≡ b (mod 2), x ∈ ℤ≥0 - toggles (odd/even presses)
    - Part 2: Ax = b, x ∈ ℤ≥0 - increments (exact counts)

Key insight for Part 1: 
  - Buttons can be pressed any number of times (x ∈ ℤ≥0)
  - Due to mod 2: pressing 2k times ≡ 0 (OFF), pressing 2k+1 times ≡ 1 (ON)
  - The objective "minimize sum(x)" ensures the solver naturally prefers 0 or 1 presses
  - No need to explicitly constrain x ≤ 1!

Implementation:
    Part 1: scipy.optimize.milp with slack variables (Ax - 2k = b)
    Part 2: scipy.optimize.milp (standard integer LP)

This is the mathematically elegant formulation - both are integer LP!

Usage:
  python3 main.py input01.txt
  python3 main.py input02.txt -d
"""
import argparse
import re


class LightMachine:
    """Machine with buttons that affect lights/counters.
    
    Solves integer linear programming problems:
    - Part 1: minimize sum(x) subject to Ax ≡ b (mod 2), x ∈ ℤ≥0
    - Part 2: minimize sum(x) subject to Ax = b, x ∈ ℤ≥0
    """
    
    def __init__(self, target_pattern, button_wirings, joltage_targets=None):
        """Initialize the machine.
        
        Args:
            target_pattern: String of '.' and '#' characters (target light state)
            button_wirings: List of button definitions, each is a list of indices
            joltage_targets: Optional list of target joltage values
        """
        self.lights = [1 if c == '#' else 0 for c in target_pattern]
        self.buttons = button_wirings
        self.joltages = joltage_targets
    
    def _solve_ilp(self, A, b, c, lower_bounds=None):
        """Solve integer linear programming problem: minimize c·x subject to Ax = b, x ∈ ℤ.
        
        Args:
            A: Constraint matrix (numpy array)
            b: Target values (numpy array)
            c: Objective coefficients (numpy array)
            lower_bounds: Optional list of lower bounds for each variable (default: all 0)
        
        Returns:
            Solution vector, or None if no solution found
        """
        try:
            from scipy.optimize import milp, LinearConstraint, Bounds
            import numpy as np
            
            n_vars = len(c)
            
            # Bounds: default all variables ≥ 0
            if lower_bounds is None:
                lb_list = [0] * n_vars
            else:
                lb_list = lower_bounds
            ub_list = [float('inf')] * n_vars
            variable_bounds = Bounds(lb=lb_list, ub=ub_list)  # type: ignore
            
            # All variables are integers
            integrality = np.ones(n_vars, dtype=int)
            constraints = LinearConstraint(A, b, b)
            
            result = milp(c=c, constraints=constraints, bounds=variable_bounds,
                         integrality=integrality)
            
            if result.success:
                return result.x
            
            return None
                
        except ImportError:
            return None
    
    def _verify_solution(self, solution, targets, modulo=None):
        """Verify that a solution satisfies the target constraints.
        
        Args:
            solution: List of button press counts (or extended with slack variables)
            targets: List of target values for each constraint
            modulo: If specified, compute values mod this number (for mod 2, use 2)
        
        Returns:
            True if solution is valid (integers + constraints satisfied), False otherwise
        """
        # Verify all solution values are integers
        n_buttons = len(self.buttons)
        for i, x in enumerate(solution[:n_buttons]):
            if abs(x - round(x)) >= 1e-6:
                return False
        
        # Verify constraints are satisfied
        n_constraints = len(targets)
        for constraint_idx in range(n_constraints):
            value = 0
            for button_idx in range(n_buttons):
                if constraint_idx in self.buttons[button_idx]:
                    value += solution[button_idx]
            
            if modulo is not None:
                value %= modulo
            
            if value != targets[constraint_idx]:
                return False
        
        return True

    def find_minimum_presses_for_lights(self):
        """Find minimum button presses to configure lights (Part 1).
        
        Solves: minimize sum(x) subject to Ax ≡ b (mod 2), x ∈ ℤ≥0
        
        Reformulates as: minimize sum(x) subject to Ax - 2k = b, x,k ∈ ℤ, x ≥ 0
        
        Returns:
            Minimum number of presses needed
        
        Raises:
            AssertionError: If no solution found or solution is invalid
        """
        if all(light == 0 for light in self.lights):
            return 0
        
        import numpy as np
        
        n_lights = len(self.lights)
        n_buttons = len(self.buttons)
        
        # Build constraint matrix A where A[i][j] = 1 if button j affects light i
        A = np.zeros((n_lights, n_buttons), dtype=float)
        for light_idx in range(n_lights):
            for button_idx in range(n_buttons):
                if light_idx in self.buttons[button_idx]:
                    A[light_idx][button_idx] = 1.0
        
        # Add slack variables: Ax - 2k = b
        # Extended variables: [x (buttons), k (slack)]
        A_extended = np.hstack([A, -2 * np.eye(n_lights)])
        b = np.array(self.lights, dtype=float)
        c = np.array([1.0] * n_buttons + [0.0] * n_lights)  # Only count button presses
        
        # Bounds: buttons ≥ 0, slack variables unbounded
        lower_bounds = [0] * n_buttons + [float('-inf')] * n_lights
        
        # Solve
        solution = self._solve_ilp(A_extended, b, c, lower_bounds=lower_bounds)
        assert solution is not None, f"No solution found for lights: {self.lights}"
        
        # Verify and extract button presses
        solution_list = [int(round(x)) for x in solution]
        assert self._verify_solution(solution_list, self.lights, modulo=2), \
            f"Solution verification failed for lights: {self.lights}"
        
        return sum(solution_list[:n_buttons])
    
    def find_minimum_presses_for_joltage(self):
        """Find minimum button presses to configure joltage (Part 2).
        
        Solves: minimize sum(x) subject to Ax = b, x ∈ ℤ≥0
        
        Returns:
            Minimum number of presses needed
        
        Raises:
            AssertionError: If no solution found or solution is invalid
        """
        assert self.joltages is not None, "No joltage targets specified"
        
        if all(j == 0 for j in self.joltages):
            return 0
        
        import numpy as np
        
        n_counters = len(self.joltages)
        n_buttons = len(self.buttons)
        
        # Build constraint matrix A where A[i][j] = 1 if button j affects counter i
        A = np.zeros((n_counters, n_buttons), dtype=float)
        for counter_idx in range(n_counters):
            for button_idx in range(n_buttons):
                if counter_idx in self.buttons[button_idx]:
                    A[counter_idx][button_idx] = 1.0
        
        b = np.array(self.joltages, dtype=float)
        c = np.array([1.0] * n_buttons)
        
        # Solve
        solution = self._solve_ilp(A, b, c)
        assert solution is not None, f"No solution found for joltages: {self.joltages}"
        
        # Verify and return
        solution_list = [int(round(x)) for x in solution]
        assert self._verify_solution(solution_list, self.joltages, modulo=None), \
            f"Solution verification failed for joltages: {self.joltages}"
        
        return sum(solution_list)
    

def parse_machine_description(line):
    """Parse a machine description line.
    
    Format: [.#.#] (1,3) (0,2,4) ... {3,5,4,7}
    - [...] contains target light pattern
    - (...) contains comma-separated light indices for each button
    - {...} contains joltage requirements (optional)
    
    Args:
        line: Machine description string
    
    Returns:
        Tuple of (target_pattern, button_wirings, joltage_requirements)
    """
    # Extract indicator lights pattern
    lights_match = re.search(r'\[([.#]+)\]', line)
    assert lights_match, f"Invalid machine format: missing lights pattern '[...]' in: {line}"
    lights = lights_match.group(1)
    
    # Extract button wirings
    buttons = []
    for match in re.finditer(r'\(([0-9,]+)\)', line):
        indices_str = match.group(1)
        # Validate that it's comma-separated digits
        assert re.match(r'^\d+(,\d+)*$', indices_str), f"Invalid button format in: {line}"
        indices = list(map(int, indices_str.split(',')))
        buttons.append(indices)
    
    assert len(buttons) > 0, f"Invalid machine format: no buttons found in: {line}"
    
    # Extract joltage requirements (optional for Part 2)
    joltage = None
    joltage_match = re.search(r'\{([0-9,]+)\}', line)
    if joltage_match:
        joltage_str = joltage_match.group(1)
        joltage = list(map(int, joltage_str.split(',')))
    
    return lights, buttons, joltage


if __name__ == "__main__":
    # Args
    parser = argparse.ArgumentParser(description="Advent of Code Day 10")
    parser.add_argument("input", help="input file")
    parser.add_argument("-d", "--debug", action="store_true", help="enable debug output")
    args = parser.parse_args()

    # Parse input (shared by both parts)
    machines = []
    with open(args.input, "r") as f:
        for line_num, line in enumerate(f.readlines(), 1):
            line = line.strip()
            if line:
                try:
                    target_pattern, button_wirings, joltage = parse_machine_description(line)
                    machine = LightMachine(target_pattern, button_wirings, joltage)
                    machines.append(machine)
                except AssertionError as e:
                    raise AssertionError(f"Line {line_num}: {e}") from e

    # Part 1: Minimize button presses with Ax ≡ b (mod 2)
    result1 = 0
    for i, machine in enumerate(machines):
        min_presses = machine.find_minimum_presses_for_lights()
        result1 += min_presses
        if args.debug:
            print(f"Machine {i+1}: {min_presses} presses (target: {machine.lights})")
    
    print(f"Part 1: {result1}")

    # Part 2: Minimize button presses with Ax = b
    result2 = 0
    for i, machine in enumerate(machines):
        if machine.joltages:
            min_presses = machine.find_minimum_presses_for_joltage()
            result2 += min_presses
            if args.debug:
                print(f"Machine {i+1} (joltage): {min_presses} presses (target: {machine.joltages})")
    
    print(f"Part 2: {result2}")
