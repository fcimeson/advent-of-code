# Parser Updates Summary

All parsers have been updated to use regular expressions with assertions for input validation.

## Changes by Day

### Day 1 (Secret Entrance)
- **Already had**: Regex pattern `r'^([LRlr])(\d+)$'` for rotation commands
- **Status**: ✓ No changes needed

### Day 2 (Gift Shop)
- **Already had**: Regex pattern `r'^(\d+)-(\d+)$'` for ranges
- **Status**: ✓ No changes needed

### Day 3 (Lobby)
- **Added**: Regex pattern `r'^\d+$'` to validate battery bank lines contain only digits
- **Added**: Assertion with line number for invalid formats
- **Added**: Import of `re` module

### Day 4 (Printing Department)
- **Added**: Regex pattern `r'^[@.]+$'` to validate grid contains only '@' and '.' characters
- **Added**: Assertion with line number for invalid characters
- **Added**: Import of `re` module

### Day 5 (Cafeteria)
- **Added**: Regex pattern `r'^(\d+)-(\d+)$'` for range validation
- **Added**: Regex pattern `r'^\d+$'` for ingredient ID validation
- **Added**: Assertion checking for exactly 2 sections in input
- **Added**: Assertions with line numbers for both ranges and IDs
- **Added**: Import of `re` module

### Day 6 (Trash Compactor)
- **Added**: Regex pattern `r'^[\d+* ]*$'` to validate worksheet contains only valid characters
- **Added**: Assertion with line number for invalid formats
- **Added**: Import of `re` module

### Day 7 (Laboratories)
- **Added**: Regex pattern `r'^[S^. ]*$'` to validate grid characters
- **Added**: Assertion to prevent multiple 'S' markers
- **Added**: Assertion to ensure 'S' marker exists
- **Added**: Assertions with line numbers for invalid characters
- **Added**: Import of `re` module

### Day 8 (Playground)
- **Added**: Regex pattern `r'^(-?\d+),(-?\d+),(-?\d+)$'` for 3D coordinate validation
- **Added**: Support for negative coordinates
- **Added**: Assertion with line number for invalid coordinate format
- **Added**: Import of `re` module

### Day 9 (Movie Theater)
- **Added**: Regex pattern `r'^(-?\d+),(-?\d+)$'` for 2D coordinate validation
- **Added**: Support for negative coordinates
- **Added**: Assertion with line number for invalid coordinate format
- **Added**: Import of `re` module

### Day 10 (Factory)
- **Enhanced**: Added assertions in `parse_machine()` function
- **Added**: Validation for lights pattern `[...]` existence
- **Added**: Validation for button indices format
- **Added**: Assertion that at least one button exists
- **Enhanced**: Error handling in main parsing loop with line numbers
- **Status**: Already had regex, improved assertions

### Day 11 (Reactor)
- **Added**: Regex pattern `r'^([a-zA-Z0-9]+):\s+(.+)$'` for device graph lines
- **Added**: Validation that output device names are alphanumeric
- **Added**: Assertion with line number for invalid formats
- **Added**: Import of `re` module

### Day 12 (Christmas Tree Farm)
- **Added**: Regex pattern `r'^(\d+)x(\d+):\s+([\d\s]+)$'` for region definitions
- **Added**: Regex pattern `r'^(\d+):$'` for shape index lines
- **Added**: Regex pattern `r'^[#.]+$'` in `parse_shape()` to validate shape characters
- **Added**: Validation that presents are space-separated numbers
- **Added**: Multiple assertions with clear error messages
- **Added**: Import of `re` module

## Benefits

1. **Input Validation**: All inputs are now validated against expected formats
2. **Clear Error Messages**: Assertions provide specific line numbers and expected formats
3. **Early Failure**: Invalid inputs are caught immediately during parsing
4. **Type Safety**: Regex patterns ensure data types match expectations before conversion
5. **Maintainability**: Patterns are clearly defined and easy to modify
6. **Debugging**: Line numbers in error messages make troubleshooting easier

## Testing

All parsers have been tested with:
- Valid input files (input01.txt for each day)
- Invalid inputs to verify assertions trigger correctly
- Edge cases like negative coordinates and special characters

All tests pass successfully.

## Example Patterns Reference

### Simple Line Patterns
```python
# Digits only
bank_pattern = re.compile(r'^\d+$')

# Direction + number (L/R followed by digits)
line_pattern = re.compile(r'^([LRlr])(\d+)$')

# Range format (num-num)
range_pattern = re.compile(r'^(\d+)-(\d+)$')

# Device graph (name: output1 output2 ...)
line_pattern = re.compile(r'^([a-zA-Z0-9]+):\s+(.+)$')
```

### Coordinate Patterns
```python
# 2D coordinates (supports negative)
coord_pattern = re.compile(r'^(-?\d+),(-?\d+)$')

# 3D coordinates (supports negative)
coord_pattern = re.compile(r'^(-?\d+),(-?\d+),(-?\d+)$')
```

### Grid Patterns
```python
# Grid with specific characters
grid_pattern = re.compile(r'^[@.]+$')

# Grid with multiple valid characters
line_pattern = re.compile(r'^[S^. ]*$')

# Shape pattern
shape_pattern = re.compile(r'^[#.]+$')
```

### Complex Patterns
```python
# Region definition (WxH: num1 num2 ...)
region_pattern = re.compile(r'^(\d+)x(\d+):\s+([\d\s]+)$')

# Shape index (N:)
shape_idx_pattern = re.compile(r'^(\d+):$')

# Machine lights and buttons
lights_match = re.search(r'\[([.#]+)\]', line)
button_match = re.finditer(r'\(([0-9,]+)\)', line)
```

### Usage Pattern
```python
with open(args.input, "r") as f:
    for line_num, line in enumerate(f.readlines(), 1):
        line = line.strip()
        if line:
            match = pattern.match(line)
            assert match, f"Line {line_num}: Invalid format: {line}"
            # Extract groups and process
            value = match.group(1)
```

## Error Message Format

All assertions follow this format for consistency:
```python
assert condition, f"Line {line_num}: {error_description}: {actual_value}"
```

Example error messages:
- `Line 5: Invalid bank format (expected digits only): 12ab34`
- `Line 3: Invalid coordinate format (expected 'x,y,z'): 1,2`
- `Line 7: Invalid grid format (expected only '@' or '.' characters): @#@`
