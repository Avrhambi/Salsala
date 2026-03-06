# General Code Implementation Rules

------------------------------------------------------------------------

## 1. Fundamental Principles

### Readability Over All

Code is read more often than it is written.\
If a human cannot understand a line of code in 5 seconds, it needs to be
simplified or renamed.

### KISS (Keep It Simple, Stupid)

Avoid "clever" code or over-engineering.\
Choose the simplest path to solve the problem.

### YAGNI (You Ain't Gonna Need It)

Do not write code for future use cases.\
Only implement what is required for the current task.

### DRY (Don't Repeat Yourself)

Logic should have a **Single Source of Truth**.\
If you find yourself copying and pasting, abstract it into a reusable
function or constant.

### Boy Scout Rule

Always leave the code slightly cleaner than you found it.

------------------------------------------------------------------------

## 2. Meaningful Naming

### Intent-Revealing Names

Names must tell you: - Why it exists - What it does - How it is used

**Bad:**

``` javascript
var d; // days elapsed
```

**Good:**

``` javascript
var daysElapsed;
```

### Pronounceable & Searchable

Avoid abbreviations.

**Bad:**

``` javascript
calculateTx
```

**Good:**

``` javascript
calculateTransaction
```

### Function Names

Use verbs or verb--noun pairs: - `fetchUser` - `isValidEmail`

### Boolean Names

Use prefixes like: - `is` - `has` - `should`

Example:

``` javascript
isUserLoggedIn
```

### Constants

Replace magic numbers with named constants.

**Bad:**

``` javascript
if (seconds > 86400)
```

**Good:**

``` javascript
const SECONDS_IN_A_DAY = 86400;
if (seconds > SECONDS_IN_A_DAY)
```

------------------------------------------------------------------------

## 3. Function Design

### Small & Atomic

A function should do **one thing only**.\
If it performs multiple tasks, split it.

### Length

A function should ideally fit on one screen without scrolling (typically
\< 25 lines).

### Minimize Arguments

Aim for 0--2 arguments.\
If you need 3 or more, consider passing a single data object.

### No Side Effects

A function should not secretly modify global state unless that is its
explicit purpose.

### Command--Query Separation

A function should either: - Do something (change state), **or** - Answer
something (return data)

But not both.

------------------------------------------------------------------------

## 4. Structure & Organization

### Separation of Concerns

Divide code into distinct sections (e.g., Data, Logic, Presentation).\
Changing the UI should not require changing business logic.

### Encapsulation

Hide internal complexity.\
Only expose what is strictly necessary.

### Vertical Density

Keep related code physically close together.\
Declare variables near their first usage.

### Flow of Execution

Code should read like a top-down narrative: - High-level logic at the
top - Low-level details at the bottom

------------------------------------------------------------------------

## 5. Defensive Programming & Quality

### Error Handling

Never let errors fail silently.\
Use explicit `try/catch` blocks and log meaningful error messages.

### Boundary Conditions

Explicitly handle edge cases: - Empty lists - Null values - Maximum
limits

Handle them at the beginning of functions.

### Write Testable Code

If it's hard to write a test, the code is likely too complex.

### Fail Fast

Validate inputs at the start of a process.\
If something is wrong, stop immediately.

------------------------------------------------------------------------

## 6. Performance vs. Clarity

### Avoid Premature Optimization

Focus on clean, maintainable code first.\
Optimize only if performance data proves a bottleneck.

### Balance

If an efficient algorithm is hard to read: - Wrap it in a well-named
function - Document why the complexity exists

------------------------------------------------------------------------

## 7. Comments & Documentation

### Explain "Why," Not "What"

Code should explain what is happening.\
Comments should explain *why* decisions were made.

### Self-Documenting Code

If you need a comment to explain a block of code, refactor it into a
well-named function.

### No Dead Code

Never leave commented-out code in the file.\
That's what Version Control (Git) is for.

------------------------------------------------------------------------

## 8. Development Workflow

### Consistent Formatting

Follow the project's style guide without exception.

### Frequent Refactoring

Continuously improve the structure of existing code.

### Atomic Commits

Use version control to save small, logical changes with clear commit
messages.
