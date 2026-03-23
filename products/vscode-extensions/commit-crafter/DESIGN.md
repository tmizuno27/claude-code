# Commit Crafter - Design Specification

## Overview
Generate structured, conventional commit messages with templates and smart analysis of staged changes.

## Features

### 1. Conventional Commit Templates
- QuickPick with types: feat, fix, docs, style, refactor, perf, test, build, ci, chore
- Optional scope selection (auto-detected from changed file paths)
- Breaking change flag

### 2. Smart Message Generation
- Analyze `git diff --staged` to suggest commit message
- Detect file types changed and suggest appropriate type
- Count files changed, insertions, deletions for summary

### 3. SCM Integration
- Fill VS Code's built-in SCM input box with generated message
- Keyboard shortcut to trigger from SCM view

### 4. Custom Templates
- User-defined templates in settings
- Project-level `.commitcrafterrc` support
- Template variables: `{type}`, `{scope}`, `{description}`, `{body}`, `{footer}`

### 5. Validation
- Max length warnings (50 char subject, 72 char body)
- Conventional commit format enforcement
- Emoji prefix option (gitmoji style)

## Configuration
```json
{
  "commitCrafter.template": "{type}({scope}): {description}",
  "commitCrafter.enableEmoji": false,
  "commitCrafter.scopes": ["api", "ui", "core", "docs"],
  "commitCrafter.maxSubjectLength": 50
}
```

## Commands
| Command | Description |
|---------|-------------|
| `commitCrafter.generate` | Analyze diff and generate message |
| `commitCrafter.selectTemplate` | Pick from saved templates |
