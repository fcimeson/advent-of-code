# Advent of Code Solver Prompt

## Purpose
This prompt guides AI agents to solve Advent of Code problems following a consistent structure and workflow.

## How to Use
1. User provides either:
   - **Advent of Code problem URL** (e.g., `https://adventofcode.com/2025/day/5`)
   - **Copy/pasted problem text** from the webpage
2. Agent fetches/analyzes the problem
3. Agent creates the solution following the structure below

---

## Workflow

### Step 1: Get and Analyze Problem

**If URL provided:**
- Fetch the problem page from the URL using webfetch tool
- Extract content from HTML

**If problem text provided:**
- Use the provided text directly

**Then extract:**
- Problem description
- Sample input and expected output for Part 1
- Constraints and edge cases
- Part 1 requirements only (solve Part 1 first)
- Note: Part 2 will be added later (builds on Part 1)

### Step 2: Create Directory Structure
Create a new directory: `day{NN}/` where NN is zero-padded (e.g., `day01`, `day15`)

Required files:
- `main.py` - Main executable script
- `input01.txt` - Sample input from the problem
- `AGENT_SETUP.md` - Documentation of AI agent used

Optional files (as needed):
- `input02.txt` - Full puzzle input (or additional test cases)
- Additional helper files only if problem is very complex

### Step 3: Implement Solution

#### main.py Requirements
```python
#!/usr/bin/env python3
"""Advent of Code - Day {N} ({Problem Title})

Brief description of what the problem asks.

Usage:
  python3 main.py input01.txt
  python3 main.py input02.txt -d
"""
import argparse

if __name__ == "__main__":
    # Args
    parser = argparse.ArgumentParser(description="Advent of Code Day {N}")
    parser.add_argument("input", help="input file")
    parser.add_argument("-d", "--debug", action="store_true", help="enable debug output")
    args = parser.parse_args()

    # Parse input (shared by both parts)
    data = []
    with open(args.input, "r") as f:
        for line in f.readlines():
            line = line.strip()
            # Parse line as needed
            data.append(line)

    # Part 1
    result1 = 0
    # ... solve part 1 ...
    print(f"Part 1: {result1}")

    # Part 2
    result2 = 0
    # ... solve part 2 (can reuse Part 1 variables/functions) ...
    print(f"Part 2: {result2}")
```

**Key Requirements:**
- Use `argparse` with `input` positional argument and optional `-d/--debug` flag
- Read and parse input once (shared by both parts)
- Solve Part 1 and print: `Part 1: {answer}`
- Solve Part 2 and print: `Part 2: {answer}`
- Part 2 can build on Part 1 (reuse variables, intermediate results)
- All code in single `main.py` file (no imports from other files unless complex)
- Make executable: `chmod +x main.py`
- Add shebang: `#!/usr/bin/env python3`

#### Code Style
- Keep all code in single `main.py` file under `if __name__ == "__main__":`
- Use helper functions as needed (but keep them in same file)
- Follow functional programming principles where practical
- Use descriptive variable names
- Comment tricky algorithms or non-obvious logic
- Organize: imports → argparse → input parsing → Part 1 → Part 2

### Step 4: Validate Solution
1. **Test with sample input first:**
   ```bash
   python3 main.py input01.txt
   ```
2. Verify Part 1 output matches expected answer
3. If incorrect, debug and fix
4. Once Part 1 sample passes, test with full input
5. **When Part 2 unlocks:** Update `main.py` to add Part 2 solution
6. Test Part 2 with sample input, then full input

### Step 5: Document Setup
Create `AGENT_SETUP.md`:
```markdown
Setup
- Opencode version: `v{version}`
- Provider: {AI Provider}
- Model: `{Model Name}`
- Agent: {Agent Type}
```

---

## Best Practices

### Problem Solving
- Read the problem carefully (edge cases, constraints)
- Start with Part 1 only (Part 2 unlocks after Part 1 is solved)
- Test with sample input first (critical!)
- Part 2 always builds on Part 1 - design with reusability in mind
- Keep shared data/functions that both parts can use

### Code Organization
- All code in single `main.py` file under `if __name__ == "__main__":`
- Define helper functions above the main block if needed
- Parse input once, use for both parts
- Part 1 code first, then Part 2
- Part 2 can reuse Part 1's variables and helper functions

### Common Patterns
```python
# Parsing numbers
numbers = [int(x) for x in line.strip().split()]

# Parsing grid
grid = [list(line.strip()) for line in lines]

# Reading groups separated by blank lines
groups = '\n'.join(lines).strip().split('\n\n')

# Default dict for counting
from collections import defaultdict
counts = defaultdict(int)
```

### Output
- Print both parts: `Part 1: {answer}` and `Part 2: {answer}`
- Use exact format: `print(f"Part 1: {result}")`
- Add debug output only when `-d/--debug` flag is used
- Keep debug output minimal and helpful

---

## Example Invocations

**User provides URL:**
```
Solve this Advent of Code problem: https://adventofcode.com/2025/day/5
```

**User provides problem text:**
```
Solve this Advent of Code problem:

--- Day 5: Print Queue ---
[full problem text pasted here...]
```

**Agent response (same for both):**
1. Analyze problem requirements (Part 1 only initially)
2. Extract sample input and expected output
3. Create `day05/` directory
4. Implement `main.py` with Part 1 solution (Part 2 placeholder)
5. Create `input01.txt` with sample input
6. Test: `python3 day05/main.py day05/input01.txt`
7. Verify Part 1 output matches expected answer
8. Create `AGENT_SETUP.md`
9. Report results to user
10. When Part 2 unlocks: Update `main.py` to add Part 2 solution

---

## Validation Checklist

Before completing, verify:
- [ ] Directory created: `day{NN}/`
- [ ] `main.py` exists and is executable
- [ ] Uses `argparse` with `input` argument and `-d/--debug` flag
- [ ] `input01.txt` contains sample input
- [ ] Part 1 tested with sample input
- [ ] Part 1 output matches expected answer
- [ ] Part 2 placeholder included (or solved if Part 2 available)
- [ ] Both parts print in format: `Part 1: {answer}` and `Part 2: {answer}`
- [ ] `AGENT_SETUP.md` created
- [ ] All code in single `main.py` file

---

## Notes

- **Initial solve**: Implement Part 1 only, add placeholder for Part 2
- **Part 2 update**: When unlocked, update same `main.py` to solve Part 2
- **Code organization**: Everything in one file, Part 2 builds on Part 1
- **Output format**: Always print `Part 1: {answer}` and `Part 2: {answer}`
- **Performance**: Correctness first, optimize only if needed
- **Debug flag**: Use `-d` flag for debug output during development
