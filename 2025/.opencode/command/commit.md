---
description: Create professional commits with detailed, context-aware messages
---

# Commit Command

You are an AI agent that helps create professional git commits with detailed, context-aware commit messages. Follow these instructions exactly. Always create the commit without asking for confirmation unless there is a big issue or error.

## Instructions for Agent

When the user runs this command, execute the following workflow:

1. **Check command mode**:
   - If user provides $ARGUMENTS (additional context or specific message), use it to inform the commit message

2. **Analyze git status**:
   - Run `git status --porcelain` to check for changes
   - Run `git status` for detailed view of changed files
   - If no files are staged, run `git add .` to stage all modified files
   - If files are already staged, proceed with only those files
   
3. **Analyze the changes in detail**:
   - Run `git diff --cached` to see what will be committed
   - Identify the files that changed and the nature of changes
   - Understand WHAT functionality changed (not just which files)
   - Determine the primary change type (feat, fix, docs, refactor, etc.)
   - Identify specific components, features, or systems affected
   
4. **Generate detailed commit message**:
   - Follow format: `<type>: Brief description of what was changed`
   - First line should be 50-72 characters or less
   - Use imperative mood: "Add feature" not "Added feature"
   - Capitalize first letter after colon
   - Do NOT end first line with a period
   - Add extended description with bullet points for significant changes:
     - Focus on WHAT functionality changed and WHY
     - Not just which files changed, but what those changes accomplish
     - Group related changes together
     - Be specific about components/features affected

   **Body formatting rules (avoid extra blank lines):**
   - Use exactly **one** blank line between subject and body
   - Use a tight bullet list: one bullet per line, **no** blank lines between bullets

5. **Execute the commit**:
   - Use **two message paragraphs** (subject + body):
     - `git commit -m "<subject>" -m "<body>"`
   - Ensure `<body>` contains the full bullet list in a single string (do **not** pass one `-m` per bullet, as that can introduce extra blank lines)
   - Display the commit hash and confirm success
   - Provide brief summary of what was committed

## Commit Message Guidelines

### Format Structure
```
<type>: Brief description of what was changed

- Bullet point for significant changes
- Another bullet point for important details
- Focus on functionality, not just file names
```

**Formatting notes:**
- Exactly **one** blank line between subject and body
- No blank lines between bullet items

### Rules

- **Be concise**: First line should be 50-72 characters or less
- **Use imperative mood**: "Add feature" not "Added feature"
- **Capitalize first letter**: After the colon, start with capital letter
- **No period**: Don't end the first line with a period
- **Focus on WHY and WHAT**: Not just what files changed, but what functionality changed
- **Use bullet points**: For multiple changes in extended description
- **Atomic commits**: Each commit should contain related changes that serve a single purpose

### Common Change Types

Map git changes to meaningful descriptions:

- **New files**: "Add [component/feature]"
- **Modified files**: "Update [functionality]", "Fix [issue]", "Enhance [feature]"
- **Deleted files**: "Remove [deprecated/unused component]"
- **Refactoring**: "Refactor [component] for better [performance/readability/maintainability]"
- **Bug fixes**: "Fix [specific issue/bug]"
- **Documentation**: "Update documentation for [component]"
- **Tests**: "Add/Update tests for [functionality]"

### Conventional Commit Types

Use conventional commit format `<type>: <description>`:
  - `feat`: A new feature
  - `fix`: A bug fix
  - `docs`: Documentation changes
  - `style`: Code style changes (formatting, etc.)
  - `refactor`: Code changes that neither fix bugs nor add features
  - `perf`: Performance improvements
  - `test`: Adding or fixing tests
  - `chore`: Changes to the build process, tools, etc.

## Reference: Good Commit Examples

### Detailed Commits with Extended Descriptions

**Excellent examples:**
```
feat: Add max heading error helper functionality

- Enhanced local controller safety features
- Updated supervisor implementation 
- Improved error handling for heading calculations
```

```
fix: Resolve memory leak in trajectory groomer

- Release allocated memory in destructor
- Add null pointer checks
- Update unit tests for memory management
```

```
feat: Implement new obstacle avoidance algorithm

- Add wall follower trajectory generation
- Integrate with existing path planning system
- Update configuration parameters
```

```
refactor: Simplify authentication module for better maintainability

- Extract validation logic into separate helper functions
- Simplify error handling in login flow
- Add comprehensive unit tests for edge cases
```

```
docs: Update API documentation with new endpoints

- Add examples for authentication endpoints
- Document rate limiting behavior
- Include error response formats
```

### Simple Commits (Single Line)

Use for smaller, focused changes:
- feat: add user authentication system
- fix: resolve memory leak in rendering process
- docs: update API documentation with new endpoints
- refactor: simplify error handling logic in parser
- style: resolve linter warnings in component files
- chore: improve developer tooling setup process
- test: add unit tests for authentication flow

## Agent Behavior Notes

- **Type selection**: Always use appropriate conventional commit type (feat, fix, docs, refactor, etc.)
- **Detailed analysis**: Go beyond file names - understand what functionality is being changed
- **Extended descriptions**: Use bullet points to provide context for significant changes
- **Error handling**: If validation fails, give user option to proceed or fix issues first  
- **Auto-staging**: If no files are staged, automatically stage all changes with `git add .`
- **File priority**: If files are already staged, only commit those specific files
- **Always create the commit**: You don't need to ask for confirmation unless there is a big issue or error. Do NOT push to remote.
- **Message quality**: Ensure commit messages are clear, detailed, and follow the format guidelines above
- **Success feedback**: After successful commit, show commit hash and brief summary
- **Context awareness**: If user provides additional context or arguments, incorporate that into the commit message
- **Focus on value**: Emphasize what changed and why, not just which files were modified
