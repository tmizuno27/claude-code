# Project Scaffolder Prompt

## Objective
Generate a complete project structure for a new business automation project, including directory layout, CLAUDE.md, config templates, and starter scripts.

## Required Context / Inputs
- Project type (blog, SaaS, digital product, API)
- Tech stack
- Monetization model

## Prompt

```
Scaffold a complete project for a new [PROJECT TYPE] business.

**Project Details:**
- Name: [PROJECT NAME]
- Type: [blog site / SaaS app / API service / digital product line / e-commerce]
- Tech stack: [Python + WordPress / Next.js + Supabase / Cloudflare Workers / etc.]
- Monetization: [affiliate / ads / subscriptions / one-time sales / API usage]

**Generate:**

1. **Directory Structure**:
   ```
   [project-name]/
   ├── CLAUDE.md
   ├── config/
   │   ├── secrets.json.example
   │   ├── site-config.json
   │   └── affiliate-links.json
   ├── scripts/
   │   ├── content/
   │   ├── publishing/
   │   └── analytics/
   ├── templates/
   ├── inputs/
   ├── outputs/
   ├── logs/
   ├── .gitignore
   └── requirements.txt (or package.json)
   ```

2. **CLAUDE.md** — comprehensive project instructions including:
   - Project overview and goals
   - Directory structure explanation
   - Key commands and scripts
   - Business rules and constraints
   - API credentials location

3. **Config Templates**:
   - secrets.json.example (with placeholder values)
   - .gitignore (exclude secrets, logs, node_modules, __pycache__)

4. **Starter Scripts**:
   - A "hello world" script that validates the setup works
   - Config loader utility
   - Logging setup utility

5. **README.md** with setup instructions

**Output:**
- Create all files in [DESTINATION PATH]
- Print a "Getting Started" checklist to console

Project name: [NAME]
Destination: [PATH]
```

## Expected Output
- Complete project directory with all files
- Console checklist for first-time setup

## Tips
- CLAUDE.md is the most important file — invest time in making it comprehensive
- The secrets.json.example should have realistic placeholder values so you know what format is expected
- Start with this scaffold, then evolve it as your project grows
