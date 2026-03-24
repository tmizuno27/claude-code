# M27 Env File Lens

> The complete .env file manager for VS Code. Browse, compare, detect secrets, and generate .env.example automatically.

## Why This Extension?

Managing `.env` files across environments (dev, staging, production) is error-prone. Env File Lens gives you a **visual overview** of all env files, highlights missing keys, warns about exposed secrets, and generates safe `.env.example` templates.

## Features

- **TreeView Browser** -- See all `.env*` files and their keys in a sidebar panel
- **Compare Env Files** -- Side-by-side comparison showing missing keys between files
- **Secret Detection** -- Warns when keys containing `password`, `token`, `secret`, `key`, `api_key` have values
- **Inline Decorations** -- Color-coded value types (URL, number, boolean, string, hash)
- **Generate .env.example** -- One-click generation with safe placeholders, preserving key names
- **Multi-File Support** -- Works with `.env`, `.env.local`, `.env.development`, `.env.production`, etc.

## Installation

1. Open VS Code
2. Go to Extensions (`Ctrl+Shift+X`)
3. Search for **"M27 Env File Lens"**
4. Click **Install**

Or from the command line:
```
ext install miccho27.m27-env-lens-tool
```

## Usage

1. Open the **"ENV Lens"** panel in the Activity Bar
2. Browse all `.env` files and their keys
3. Run **"ENV Lens: Compare Two .env Files"** to find missing keys
4. Run **"ENV Lens: Generate .env.example"** to create a safe template

## Alternatives Comparison

| Feature | Env File Lens | DotENV (ext) | EnvFile (ext) |
|---------|:------------:|:------------:|:------------:|
| TreeView browser | Yes | No | No |
| Compare env files | Yes | No | No |
| Secret detection | Yes | No | No |
| Generate .env.example | Yes | No | No |
| Syntax highlighting | Yes | Yes | Yes |

## License

MIT
