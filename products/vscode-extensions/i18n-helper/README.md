# M27 i18n Helper

> Complete i18n workflow in VS Code. Autocomplete keys, detect missing translations, and manage locale files effortlessly.

## Why This Extension?

Managing translation files manually is slow and error-prone. i18n Helper provides **IntelliSense for translation keys**, highlights missing translations as diagnostics, and lets you manage keys across all locales from one place.

## Features

- **IntelliSense Autocomplete** -- Suggestions for `t()`, `$t()`, `i18n.t()` patterns
- **Hover Preview** -- See translation values across all locales by hovering
- **Missing Translation Detection** -- Inline diagnostics for keys missing in any locale
- **Key Management** -- Add, rename, and delete keys across all locale files at once
- **Sort Keys** -- Alphabetically sort keys in all locale files
- **TreeView Browser** -- Visual browser for all locales and their keys
- **Multi-Framework** -- Works with React (react-i18next), Vue (vue-i18n), Angular, and plain JSON

## Installation

1. Open VS Code
2. Go to Extensions (`Ctrl+Shift+X`)
3. Search for **"M27 i18n Helper"**
4. Click **Install**

Or from the command line:
```
ext install miccho27.m27-i18n-helper
```

## Usage

1. Open a project with i18n JSON files (e.g., `locales/en.json`, `locales/ja.json`)
2. Start typing `t('` in any JS/TS file -- autocomplete suggestions appear
3. Hover over any translation key to see all locale values
4. Open the **"i18n Helper"** panel to browse and manage keys

## Configuration

| Setting | Default | Description |
|---------|---------|-------------|
| `i18nHelper.localesPath` | `locales` | Path to locale files directory |
| `i18nHelper.defaultLocale` | `en` | Primary locale for reference |

## Alternatives Comparison

| Feature | i18n Helper | i18n Ally | i18next (ext) |
|---------|:----------:|:---------:|:------------:|
| Autocomplete keys | Yes | Yes | Limited |
| Missing detection | Yes | Yes | No |
| Manage keys | Yes | Yes | No |
| Lightweight | Yes | No | Yes |
| Free | Yes | Yes | Yes |

## License

MIT
