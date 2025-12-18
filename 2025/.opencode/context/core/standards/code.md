<!-- Context: standards/code | Priority: critical | Version: 2.0 | Updated: 2025-01-21 -->
# Code Standards

## Quick Reference

**Core Philosophy**: Modular, Functional, Maintainable
**Golden Rule**: If you can't easily test it, refactor it

**Critical Patterns** (use these):
- ✅ Pure functions (same input = same output, no side effects)
- ✅ Immutability (create new data, don't modify)
- ✅ Composition (build complex from simple)
- ✅ Small functions (< 50 lines)
- ✅ Explicit dependencies (dependency injection)

**Anti-Patterns** (avoid these):
- ❌ Mutation, side effects, deep nesting
- ❌ God modules, global state, large functions

---

## Core Philosophy

**Modular**: Everything is a component - small, focused, reusable
**Functional**: Pure functions, immutability, composition over inheritance
**Maintainable**: Self-documenting, testable, predictable

## Principles

### Modular Design
- Single responsibility per module
- Clear interfaces (explicit inputs/outputs)
- Independent and composable
- < 100 lines per component (ideally < 50)

### Functional Approach
- **Pure functions**: Same input = same output, no side effects
- **Immutability**: Create new data, don't modify existing
- **Composition**: Build complex from simple functions
- **Declarative**: Describe what, not how

### Component Structure
```
component/
├── index.js      # Public interface
├── core.js       # Core logic (pure functions)
├── utils.js      # Helpers
└── tests/        # Tests
```

## Patterns

### Pure Functions
```javascript
// ✅ Pure
const add = (a, b) => a + b;
const formatUser = (user) => ({ ...user, fullName: `${user.firstName} ${user.lastName}` });

// ❌ Impure (side effects)
let total = 0;
const addToTotal = (value) => { total += value; return total; };
```

### Immutability
```javascript
// ✅ Immutable
const addItem = (items, item) => [...items, item];
const updateUser = (user, changes) => ({ ...user, ...changes });

// ❌ Mutable
const addItem = (items, item) => { items.push(item); return items; };
```

### Composition
```javascript
// ✅ Compose small functions
const processUser = pipe(validateUser, enrichUserData, saveUser);
const isValidEmail = (email) => validateEmail(normalizeEmail(email));

// ❌ Deep inheritance
class ExtendedUserManagerWithValidation extends UserManager { }
```

### Declarative
```javascript
// ✅ Declarative
const activeUsers = users.filter(u => u.isActive).map(u => u.name);

// ❌ Imperative
const names = [];
for (let i = 0; i < users.length; i++) {
  if (users[i].isActive) names.push(users[i].name);
}
```

## Naming

- **Files**: lowercase-with-dashes.js
- **Functions**: verbPhrases (getUser, validateEmail)
- **Predicates**: isValid, hasPermission, canAccess
- **Variables**: descriptive (userCount not uc), const by default
- **Constants**: UPPER_SNAKE_CASE

## Scripting Standards (Bash & Python)

### Bash

Use bash for **small, straightforward glue** only.

✅ DO:
- Keep scripts **minimal** and readable
- Prefer simple pipelines and direct commands over abstraction
- Inline one-off values rather than introducing extra variables

❌ DON'T:
- Add lots of boilerplate “strict mode” / heavy error-handling scaffolding by default
- Build mini frameworks (helpers, complex flag parsing, deep function hierarchies)

Rule of thumb: if a bash script starts needing non-trivial parsing, branching, state, retries, or grows beyond a small utility, **switch to Python**.

### Python

Use Python for anything **non-trivial**. The extra structure (functions, validation, error handling) is expected and encouraged.

✅ DO:
- Always provide a CLI interface via `argparse`
- Structure scripts with `main()` and small testable functions
- Prefer Python over bash when the task has multiple steps, complex conditions, or non-trivial input/output

`argparse` template:

```python
import argparse

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Describe what this script does")
    parser.add_argument("--input", required=True, help="Path to input")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    # ... implement logic ...

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## Error Handling

```javascript
// ✅ Explicit error handling
function parseJSON(text) {
  try {
    return { success: true, data: JSON.parse(text) };
  } catch (error) {
    return { success: false, error: error.message };
  }
}

// ✅ Validate at boundaries
function createUser(userData) {
  const validation = validateUserData(userData);
  if (!validation.isValid) {
    return { success: false, errors: validation.errors };
  }
  return { success: true, user: saveUser(userData) };
}
```

## Dependency Injection

```javascript
// ✅ Dependencies explicit
function createUserService(database, logger) {
  return {
    createUser: (userData) => {
      logger.info('Creating user');
      return database.insert('users', userData);
    }
  };
}

// ❌ Hidden dependencies
import db from './database.js';
function createUser(userData) { return db.insert('users', userData); }
```

## Anti-Patterns

❌ **Mutation**: Modifying data in place
❌ **Side effects**: console.log, API calls in pure functions
❌ **Deep nesting**: Use early returns instead
❌ **God modules**: Split into focused modules
❌ **Global state**: Pass dependencies explicitly
❌ **Large functions**: Keep < 50 lines

## Best Practices

✅ Pure functions whenever possible
✅ Immutable data structures
✅ Small, focused functions (< 50 lines)
✅ Compose small functions into larger ones
✅ Explicit dependencies (dependency injection)
✅ Validate at boundaries
✅ Self-documenting code
✅ Test in isolation

**Golden Rule**: If you can't easily test it, refactor it.
