# Automation Script Builder Prompt

## Objective
Create a production-ready Python automation script with logging, error handling, health checks, and scheduling support.

## Required Context / Inputs
- Task to automate (what manual process are you replacing?)
- Trigger (schedule, event, manual)
- Required APIs or data sources

## Prompt

```
Build a production-ready automation script.

**Task Description:**
- What to automate: [DESCRIBE THE MANUAL PROCESS]
- Trigger: [daily at X time / every N hours / on event / manual]
- Input: [files, APIs, databases]
- Output: [files, API calls, notifications]

**Requirements:**

1. **Core Logic**:
   - Implement the automation task
   - Handle all edge cases (empty data, API failures, rate limits)
   - Idempotent execution (safe to run multiple times)

2. **Configuration**:
   - Read credentials from config/secrets.json (never hardcode)
   - Support --dry-run flag for testing
   - Support --verbose flag for debugging
   - Use environment variables for overrides

3. **Logging**:
   - Log to both console and file (logs/[script-name].log)
   - Include timestamps, log levels (INFO, WARNING, ERROR)
   - Log start/end times and execution duration
   - Log summary statistics (items processed, successes, failures)

4. **Error Handling**:
   - Try/except around all external calls (API, file I/O)
   - Retry with exponential backoff for transient failures (3 attempts)
   - Continue processing remaining items on individual failures
   - Summary of all errors at the end

5. **Health Check Integration**:
   - Ping Healthchecks.io on success (GET https://hc-ping.com/{CHECK_ID})
   - Ping /fail endpoint on failure
   - Include check ID in config

6. **Scheduling Support**:
   - Include Task Scheduler setup instructions (Windows)
   - Include cron setup instructions (Linux/Mac)
   - Include the PowerShell wrapper script for Task Scheduler

**Output:**
- Save script to scripts/[category]/[script-name].py
- Include a README section at the top of the file with usage instructions
- Generate the scheduling commands

Script name: [NAME]
Category: [content / publishing / analytics / maintenance]
```

## Expected Output
- `scripts/[category]/[script-name].py` — complete script
- Scheduling setup instructions in console output

## Tips
- Every script should work standalone (python script.py) without requiring Claude Code
- The --dry-run flag is essential for testing in production environments
- Health check pings cost nothing and save hours of debugging silent failures
