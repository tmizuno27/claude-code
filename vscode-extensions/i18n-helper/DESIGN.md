# i18n Helper - Design Specification

## Overview
Manage internationalization files: autocomplete keys, detect missing translations, bulk operations.

## Features

### 1. Key Autocomplete
- IntelliSense for `t('key')`, `$t('key')`, `i18n.t('key')` patterns
- Show translation value in hover/detail

### 2. Missing Translation Detection
- Compare all locale JSON files
- Diagnostics for keys missing in any locale
- Quick fix: add missing key with placeholder

### 3. Key Management
- Add key to all locales at once
- Rename key across all locales
- Delete key from all locales

### 4. Sort & Format
- Sort keys alphabetically (nested support)
- Consistent JSON formatting

### 5. TreeView
- Browse all locales and their keys
- Visual indicator for missing translations
- Click to navigate to key in file

## Configuration
```json
{
  "i18nHelper.localesPath": "src/locales",
  "i18nHelper.defaultLocale": "en",
  "i18nHelper.functionPatterns": ["t", "$t", "i18n.t"]
}
```
