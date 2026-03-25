# Code Review Automation Prompt

## Objective
Perform a comprehensive code review on a file, directory, or entire project — checking for bugs, security issues, performance problems, and code quality.

## Required Context / Inputs
- Path to the code to review
- Language/framework context
- What the code does (brief description)

## Prompt

```
Perform a thorough code review on [PATH_TO_CODE].

**Review Scope:**
- Files/directory: [PATH]
- Language: [Python / JavaScript / TypeScript / etc.]
- Framework: [Next.js / Flask / WordPress / etc.]
- Purpose: [Brief description of what this code does]

**Review Checklist:**

1. **Security** (CRITICAL):
   - Hardcoded secrets or API keys
   - SQL injection vulnerabilities
   - XSS vulnerabilities
   - Missing input validation
   - Insecure authentication/authorization
   - Exposed error messages with sensitive data

2. **Bugs & Logic Errors** (HIGH):
   - Off-by-one errors
   - Null/undefined handling
   - Race conditions
   - Unhandled exceptions
   - Incorrect API usage
   - Edge cases not covered

3. **Performance** (MEDIUM):
   - N+1 query patterns
   - Missing pagination on large datasets
   - Unnecessary re-renders (React/frontend)
   - Missing caching opportunities
   - Synchronous operations that should be async
   - Large file reads without streaming

4. **Code Quality** (MEDIUM):
   - Functions over 50 lines
   - Files over 800 lines
   - Deep nesting (>4 levels)
   - Unclear variable/function names
   - Duplicated code
   - Missing error handling
   - Hardcoded values that should be config

5. **Architecture** (LOW):
   - Separation of concerns
   - Dependency management
   - Testability
   - Scalability concerns

**Output Format:**
For each finding:
- Severity: CRITICAL / HIGH / MEDIUM / LOW
- File: path/to/file.py
- Line: approximate line number
- Issue: concise description
- Fix: recommended solution with code example

**Summary:**
- Total findings by severity
- Top 3 most important fixes
- Overall code health score (1-10)

Save report to: outputs/code-review-[date].md
```

## Expected Output
- `outputs/code-review-[date].md` — detailed review report
- Console summary with severity counts and top priorities

## Example Usage

```
Review Scope:
- Files/directory: scripts/publishing/
- Language: Python
- Framework: WordPress REST API integration
- Purpose: Scripts that publish articles and manage content on WordPress sites
```

## Tips
- Run before every major deployment or commit
- Focus on CRITICAL and HIGH issues first
- For large codebases, review one directory at a time
- Use this as a pre-commit check by integrating into your workflow
