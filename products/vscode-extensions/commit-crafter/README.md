# M27 Commit Crafter

> Generate perfect conventional commit messages with one click. Smart analysis of your staged changes.

## Why This Extension?

Writing consistent commit messages is tedious. Commit Crafter **analyzes your staged changes** and generates structured messages following the [Conventional Commits](https://www.conventionalcommits.org/) specification -- with optional gitmoji support.

## Features

- **Smart Type Detection** -- Automatically suggests `feat`, `fix`, `refactor`, etc. based on staged diffs
- **Auto-Detect Scope** -- Infers scope from changed file paths (e.g., `auth`, `api`, `ui`)
- **Gitmoji Support** -- Optional emoji prefixes for visual commit history
- **Custom Templates** -- Define your own commit message templates
- **SCM Integration** -- Fills the VS Code Source Control input box directly
- **Subject Validation** -- Warns if subject line exceeds configured length

## Installation

1. Open VS Code
2. Go to Extensions (`Ctrl+Shift+X`)
3. Search for **"M27 Commit Crafter"**
4. Click **Install**

Or from the command line:
```
ext install miccho27.m27-commit-crafter
```

## Usage

1. Stage your changes in Git
2. Open Command Palette (`Ctrl+Shift+P`)
3. Run **"Commit Crafter: Generate Message"**
4. Review and adjust the generated message
5. Commit directly from the SCM panel

## Configuration

| Setting | Default | Description |
|---------|---------|-------------|
| `commitCrafter.useGitmoji` | `false` | Enable gitmoji emoji prefix |
| `commitCrafter.maxSubjectLength` | `72` | Max characters for subject line |
| `commitCrafter.customTemplates` | `[]` | Custom message templates |

## Alternatives Comparison

| Feature | Commit Crafter | Git Lens | Conventional Commits (ext) |
|---------|:--------------:|:--------:|:-------------------------:|
| Auto-generate message | Yes | No | No |
| Analyze staged changes | Yes | No | No |
| Gitmoji support | Yes | No | No |
| Custom templates | Yes | N/A | Limited |
| Free | Yes | Freemium | Yes |

## License

MIT
