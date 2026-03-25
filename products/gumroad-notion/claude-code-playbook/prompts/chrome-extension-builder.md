# Chrome Extension Builder Prompt

## Objective
Build a complete Chrome extension from concept to submission-ready package, including manifest, popup UI, content scripts, and Chrome Web Store listing.

## Required Context / Inputs
- Extension concept
- Target functionality
- Monetization (free, freemium, paid)

## Prompt

```
Build a complete Chrome extension.

**Extension Details:**
- Name: [EXTENSION NAME]
- Purpose: [WHAT DOES IT DO]
- Target users: [WHO USES THIS]
- Permissions needed: [tabs, storage, activeTab, etc.]
- Monetization: [free / freemium / paid one-time]

**Generate:**

1. **manifest.json** (Manifest V3):
   - Proper permissions (minimum required)
   - Icons (placeholder paths)
   - Background service worker
   - Content scripts (if needed)
   - Popup (if needed)

2. **Popup UI** (if applicable):
   - popup.html + popup.css + popup.js
   - Clean, modern design
   - Responsive to popup size constraints (max 800x600)

3. **Core Functionality**:
   - Background service worker (background.js)
   - Content script (content.js) if needed
   - Options page (options.html) if configurable
   - Storage management for user preferences

4. **Freemium Gate** (if applicable):
   - Free tier: basic features
   - Pro tier: advanced features behind a license key check
   - License validation endpoint or local check

5. **Chrome Web Store Listing**:
   - Title (under 45 characters)
   - Short description (under 132 characters)
   - Full description (detailed, keyword-rich)
   - Category recommendation
   - Screenshot descriptions (what to capture)

6. **Package**:
   - ZIP file ready for Chrome Web Store upload
   - Exclude development files

**Output:**
- Save to products/chrome-extensions/[extension-slug]/
- Include all source files
- Include store-listing.md with CWS metadata

Extension concept: [YOUR IDEA]
```

## Expected Output
- Complete extension in `products/chrome-extensions/[extension-slug]/`
- Store listing metadata

## Tips
- Manifest V3 is required for new extensions. Do not use Manifest V2.
- Request minimum permissions — excessive permissions trigger longer review times
- Test with `chrome://extensions` developer mode before submitting
- Include privacy policy URL if you collect any data
