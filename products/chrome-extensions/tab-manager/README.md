# Tab Manager & Session Saver

Chrome extension for smart tab management with session save/restore, duplicate detection, and drag-and-drop reordering.

## Features

- **Tab Overview**: View all open tabs with favicons, titles, and URLs
- **Session Save/Restore**: Save named tab sessions and restore them later
- **Search & Filter**: Instantly find tabs by title or URL
- **Duplicate Detection**: Highlights and bulk-closes duplicate tabs
- **Drag & Drop**: Reorder tabs within the popup
- **Dark Mode**: Toggle between light and dark themes
- **Keyboard Shortcut**: Ctrl+Shift+T to open popup
- **Freemium Model**: Free (3 sessions) / Pro (unlimited + export/import)

## Installation (Development)

1. Open `chrome://extensions/`
2. Enable "Developer mode"
3. Click "Load unpacked"
4. Select this directory

## Permissions

- `tabs` - Read tab information
- `storage` - Store sessions locally

No host permissions required. No data leaves your device.

## File Structure

```
tab-manager/
├── manifest.json
├── background.js
├── popup.html
├── popup.css
├── popup.js
├── icons/
├── store-assets/
│   ├── description.txt
│   └── privacy-policy.html
└── README.md
```

## Build for Store

1. Add icon PNGs (16, 32, 48, 128px) to `icons/`
2. Zip all files except `store-assets/` and `README.md`
3. Upload to Chrome Web Store Developer Dashboard
