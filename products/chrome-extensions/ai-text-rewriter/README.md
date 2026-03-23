# AI Text Rewriter

A Chrome extension that lets you select any text on a webpage and rewrite it using AI. Choose from five styles: Casual, Professional, Shorter, Longer, or Fix Grammar.

## Features

- **Select and Rewrite**: Highlight text on any page, right-click or use the popup to rewrite
- **5 Modes**: Casual, Professional, Shorter, Longer, Fix Grammar
- **BYOK**: Uses your own OpenAI API key -- no subscription, no middleman
- **Context Menu**: Right-click selected text for instant rewriting
- **Privacy**: API key stored locally; no data collected by the developer

## How It Works

1. Enter your OpenAI API key in extension settings (stored locally in browser)
2. Select any text on a webpage
3. Right-click and choose a rewriting style, or open the popup
4. Rewritten text appears instantly

## Installation

Install from the [Chrome Web Store](https://chrome.google.com/webstore).

## Privacy

Your API key is stored locally. Selected text is sent to OpenAI API for processing only. No data is collected or stored by the extension developer.

## Tech Stack

- Manifest V3
- OpenAI API (user-provided key)
- Chrome Storage API, Context Menus API
