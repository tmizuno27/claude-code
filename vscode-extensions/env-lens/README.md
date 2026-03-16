# ENV Lens

Browse, compare, and analyze `.env` files in your workspace.

## Features

- **TreeView** showing all `.env*` files with their keys
- **Compare** any two `.env` files side by side (shows missing keys)
- **Inline decorations** showing value types (URL, number, boolean, string, hash)
- **Secret detection**: warns on keys containing password, token, secret, key, etc.
- **Generate `.env.example`**: strips values, keeps keys with safe placeholders

## Usage

1. Open the "ENV Lens" panel in the Activity Bar
2. Browse all `.env` files and their keys
3. Use "ENV Lens: Compare Two .env Files" to find missing keys
4. Use "ENV Lens: Generate .env.example" to create a template

## Install

```
ext install miccho27.env-lens
```

## License

MIT
