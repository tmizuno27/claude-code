#!/usr/bin/env python3
"""
Notion Blog Management - Sync Script
CSV + Markdown -> Notion Database sync with WordPress status

Usage:
  python run_notion_init.py              # Full sync (articles + WP status)
  python run_notion_init.py --init       # Create new Notion database
  python run_notion_init.py --status     # WordPress status update only

Note: Due to Japanese path issues with Google Drive, run via:
  python C:/Users/tmizu/run_notion_init.py [options]
"""
# This is a reference copy. The executable version is at:
# C:/Users/tmizu/run_notion_init.py
