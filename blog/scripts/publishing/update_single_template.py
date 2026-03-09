#!/usr/bin/env python3
"""Update single post template with TCD-style CSS + JS.

Replaces all inline CSS blocks and updates JS in the single template.
Preserves sidebar HTML and block refs.
"""

import re
import requests
from base64 import b64encode
from pathlib import Path

URL = 'https://nambei-oyaji.com/wp-json/wp/v2'
CREDS = b64encode('t.mizuno27@gmail.com:agNg 2624 4lL4 QoT9 EOOZ OEZr'.encode()).decode()
HEADERS = {'Authorization': f'Basic {CREDS}', 'Content-Type': 'application/json'}
TEMPLATE_SLUG = 'twentytwentyfive//single'

JS_FILE = Path(__file__).parent.parent.parent / 'design' / 'single-article.js'

# =========================================================================
# TCD-Style CSS for single posts - replaces all inline CSS blocks
# =========================================================================
TCD_CSS = """
/* === TCD-Style Single Post Design === */

/* --- Reset: clean slate for single posts --- */
body.single main.wp-block-group { margin-top: 0 !important; }
body.single .entry-content > p:has(> span:only-child:empty) {
  display: none !important; margin: 0 !important; padding: 0 !important;
}
body.single .entry-content > p:has(> span[id]:only-child) {
  display: none !important; margin: 0 !important; padding: 0 !important;
}

/* --- Page Background --- */
body.single { background: #f5f5f5 !important; }

/* --- Title: TCD clean style (not gradient) --- */
body.single .wp-block-post-title {
  font-size: 28px !important;
  font-weight: 700 !important;
  line-height: 1.45 !important;
  color: #333 !important;
  letter-spacing: 0 !important;
  text-align: left !important;
  max-width: none !important;
  margin: 0 0 16px !important;
  padding: 0 !important;
  background: none !important;
  -webkit-background-clip: unset !important;
  -webkit-text-fill-color: #333 !important;
  background-clip: unset !important;
  border: none !important;
  font-feature-settings: normal !important;
}

/* --- Meta (date, author, category) --- */
body.single .wp-block-group.has-accent-4-color {
  margin-bottom: 16px !important;
  font-size: 13px !important;
  color: #999 !important;
}
body.single .wp-block-group.has-accent-4-color p {
  color: #999 !important;
  font-size: 13px !important;
}
body.single .wp-block-group.has-accent-4-color a {
  color: #999 !important;
  text-decoration: none !important;
}
body.single .wp-block-group.has-accent-4-color a:hover {
  color: #333 !important;
}
body.single .wp-block-post-terms a {
  color: #666 !important;
  text-decoration: none !important;
  background: #f0f0f0 !important;
  padding: 2px 10px !important;
  border-radius: 3px !important;
  font-size: 12px !important;
  font-weight: 400 !important;
}

/* --- Featured Image --- */
body.single .wp-block-post-featured-image {
  margin-bottom: 28px !important;
}
body.single .wp-block-post-featured-image img {
  width: 100% !important;
  height: auto !important;
  border-radius: 0 !important;
  display: block !important;
}

/* --- Content Typography --- */
body.single .entry-content,
body.single .wp-block-post-content {
  font-size: 16px !important;
  line-height: 2.2 !important;
  color: #333 !important;
  letter-spacing: 0 !important;
  max-width: none !important;
  width: 100% !important;
  padding: 0 !important;
}
body.single .entry-content p {
  margin-bottom: 1.8em !important;
  font-size: 16px !important;
  line-height: 2.2 !important;
}

/* --- H2: TCD-style with background and bottom border --- */
body.single .entry-content h2 {
  font-size: 22px !important;
  font-weight: 700 !important;
  line-height: 1.5 !important;
  color: #333 !important;
  background: #fafafa !important;
  padding: 20px 24px !important;
  margin: 56px 0 28px !important;
  border: none !important;
  border-bottom: 3px solid #333 !important;
  border-radius: 0 !important;
  max-width: none !important;
}

/* --- H3: TCD-style with left border --- */
body.single .entry-content h3 {
  font-size: 19px !important;
  font-weight: 700 !important;
  line-height: 1.5 !important;
  color: #333 !important;
  padding: 14px 0 14px 20px !important;
  margin: 40px 0 20px !important;
  border: none !important;
  border-left: 4px solid #333 !important;
  background: none !important;
  max-width: none !important;
}

/* --- H4 --- */
body.single .entry-content h4 {
  font-size: 17px !important;
  font-weight: 700 !important;
  color: #333 !important;
  margin: 32px 0 16px !important;
  padding: 0 !important;
  border: none !important;
  max-width: none !important;
}

/* --- Bold: subtle yellow highlight --- */
body.single .entry-content strong {
  font-weight: 700 !important;
  background: linear-gradient(transparent 60%, #fff9c4 60%) !important;
  padding: 0 2px !important;
}

/* --- Links --- */
body.single .entry-content a:not(.tcd-share-btn):not(.tcd-related-card):not(.tcd-meta-cat):not(.wp-block-button__link) {
  color: #0066CC !important;
  text-decoration: none !important;
  border-bottom: 1px solid rgba(0,102,204,0.3) !important;
  background: none !important;
  background-image: none !important;
  transition: color 0.2s ease, border-color 0.2s ease !important;
}
body.single .entry-content a:not(.tcd-share-btn):not(.tcd-related-card):not(.tcd-meta-cat):not(.wp-block-button__link):hover {
  color: #004C99 !important;
  border-bottom-color: #004C99 !important;
  background-image: none !important;
}

/* --- CTA: single link → button --- */
body.single .entry-content p > a:only-child:not(.tcd-share-btn):not(.wp-block-button__link) {
  display: inline-block !important;
  background: #333 !important;
  background-image: none !important;
  color: #fff !important;
  padding: 14px 32px !important;
  border-radius: 4px !important;
  font-size: 15px !important;
  font-weight: 600 !important;
  text-decoration: none !important;
  border: none !important;
  transition: background 0.3s ease !important;
  margin: 12px 0 !important;
}
body.single .entry-content p > a:only-child:not(.tcd-share-btn):not(.wp-block-button__link):hover {
  background: #555 !important;
  color: #fff !important;
}

/* --- Lists: clean dots --- */
body.single .entry-content ul {
  list-style: disc !important;
  padding-left: 24px !important;
  margin-bottom: 1.5em !important;
}
body.single .entry-content ul li {
  margin-bottom: 8px !important;
  line-height: 2 !important;
}
body.single .entry-content ul li::before {
  content: none !important;
  display: none !important;
}

/* --- Ordered lists --- */
body.single .entry-content ol {
  list-style: decimal !important;
  padding-left: 28px !important;
  margin-bottom: 1.5em !important;
  counter-reset: none !important;
}
body.single .entry-content ol li {
  margin-bottom: 8px !important;
  line-height: 2 !important;
  counter-increment: none !important;
}
body.single .entry-content ol li::before {
  content: none !important;
  display: none !important;
}

/* --- Tables: clean TCD style --- */
body.single .entry-content table,
body.single .wp-block-table table {
  width: 100% !important;
  max-width: none !important;
  border-collapse: collapse !important;
  font-size: 14px !important;
  margin: 32px 0 !important;
}
body.single .wp-block-table {
  max-width: none !important;
  margin: 32px 0 !important;
  padding: 0 !important;
  overflow: visible !important;
}
body.single .entry-content table th,
body.single .wp-block-table table th {
  background: #333 !important;
  color: #fff !important;
  font-weight: 600 !important;
  padding: 12px 16px !important;
  text-align: left !important;
  font-size: 13px !important;
  border: none !important;
}
body.single .entry-content table td,
body.single .wp-block-table table td {
  padding: 12px 16px !important;
  border-bottom: 1px solid #eee !important;
  border-left: none !important;
  border-right: none !important;
}
body.single .entry-content table tr:nth-child(even) td,
body.single .wp-block-table table tr:nth-child(even) td {
  background: #fafafa !important;
}

/* --- Images --- */
body.single .entry-content img {
  max-width: 100% !important;
  height: auto !important;
  border-radius: 0 !important;
  margin: 12px 0 !important;
}
body.single .wp-block-image {
  margin: 28px 0 !important;
  max-width: none !important;
}
body.single .wp-block-image figcaption {
  font-size: 13px !important;
  color: #999 !important;
  text-align: center !important;
  margin-top: 8px !important;
}

/* --- Blockquote --- */
body.single .entry-content blockquote {
  border-left: 4px solid #ddd !important;
  padding: 20px 24px !important;
  margin: 28px 0 !important;
  background: #fafafa !important;
  border-radius: 0 !important;
  font-style: normal !important;
}
body.single .entry-content blockquote p {
  color: #666 !important;
  font-size: 15px !important;
  line-height: 2 !important;
  margin-bottom: 0 !important;
}

/* --- Breadcrumbs (injected by JS) --- */
.tcd-breadcrumb {
  font-size: 12px !important;
  color: #999 !important;
  padding: 12px 0 !important;
  margin-bottom: 8px !important;
  grid-column: 1 / 2 !important;
}
.tcd-breadcrumb a {
  color: #666 !important;
  text-decoration: none !important;
  border-bottom: none !important;
  background: none !important;
}
.tcd-breadcrumb a:hover {
  color: #333 !important;
  text-decoration: underline !important;
}
.tcd-bc-sep { margin: 0 6px; color: #ccc; }
.tcd-bc-current { color: #999; }

/* --- TOC (in-content) --- */
.tcd-toc {
  background: #fafafa !important;
  border: 1px solid #eee !important;
  border-radius: 4px !important;
  padding: 24px 28px !important;
  margin: 28px 0 32px !important;
  max-width: none !important;
}
.tcd-toc-title {
  display: flex !important;
  align-items: center !important;
  justify-content: space-between !important;
  font-size: 16px !important;
  font-weight: 700 !important;
  color: #333 !important;
  cursor: pointer !important;
  padding-bottom: 12px !important;
  border-bottom: 1px solid #eee !important;
  margin-bottom: 16px !important;
}
.tcd-toc-toggle {
  background: none !important;
  border: none !important;
  font-size: 12px !important;
  color: #999 !important;
  cursor: pointer !important;
  padding: 4px 8px !important;
}
.tcd-toc--closed .tcd-toc-list { display: none !important; }
.tcd-toc--closed .tcd-toc-title {
  border-bottom: none !important;
  margin-bottom: 0 !important;
  padding-bottom: 0 !important;
}
.tcd-toc-list {
  list-style: none !important;
  padding: 0 !important;
  margin: 0 !important;
  counter-reset: toc-counter !important;
}
.tcd-toc-h2 {
  counter-increment: toc-counter !important;
  padding: 5px 0 !important;
}
.tcd-toc-h2 > a {
  font-size: 14px !important;
  font-weight: 600 !important;
  color: #333 !important;
  text-decoration: none !important;
  line-height: 1.7 !important;
  border-bottom: none !important;
  background: none !important;
}
.tcd-toc-h2 > a::before {
  content: counter(toc-counter) ". " !important;
  color: #999 !important;
}
.tcd-toc-h2 > a:hover { color: #0066CC !important; }
.tcd-toc-sub {
  list-style: none !important;
  padding: 0 0 0 20px !important;
  margin: 0 !important;
}
.tcd-toc-h3 { padding: 3px 0 !important; }
.tcd-toc-h3 a {
  font-size: 13px !important;
  font-weight: 400 !important;
  color: #666 !important;
  text-decoration: none !important;
  line-height: 1.7 !important;
  border-bottom: none !important;
  background: none !important;
}
.tcd-toc-h3 a:hover { color: #0066CC !important; }

/* --- SNS Share Buttons --- */
.tcd-share {
  padding: 20px 0 !important;
  border-top: 1px solid #eee !important;
  border-bottom: 1px solid #eee !important;
  margin: 28px 0 !important;
  display: flex !important;
  align-items: center !important;
  gap: 14px !important;
  max-width: none !important;
}
.tcd-share-label {
  font-size: 13px !important;
  font-weight: 600 !important;
  color: #999 !important;
  white-space: nowrap !important;
}
.tcd-share-buttons {
  display: flex !important;
  gap: 8px !important;
  flex-wrap: wrap !important;
}
.tcd-share-btn {
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  padding: 8px 18px !important;
  border-radius: 4px !important;
  font-size: 13px !important;
  font-weight: 600 !important;
  text-decoration: none !important;
  cursor: pointer !important;
  transition: all 0.2s ease !important;
  border: 1px solid #ddd !important;
  background: #fff !important;
  color: #666 !important;
}
.tcd-share-btn:hover { background: #f5f5f5 !important; }
.tcd-share-x { border-color: #333 !important; color: #333 !important; }
.tcd-share-x:hover { background: #333 !important; color: #fff !important; }
.tcd-share-fb { border-color: #1877F2 !important; color: #1877F2 !important; }
.tcd-share-fb:hover { background: #1877F2 !important; color: #fff !important; }
.tcd-share-hatena { border-color: #00A4DE !important; color: #00A4DE !important; }
.tcd-share-hatena:hover { background: #00A4DE !important; color: #fff !important; }

/* --- Author Info --- */
.tcd-author {
  margin: 40px 0 !important;
  padding: 28px !important;
  background: #fafafa !important;
  border: 1px solid #eee !important;
  border-radius: 4px !important;
  max-width: none !important;
}
.tcd-author-inner {
  display: flex !important;
  gap: 20px !important;
  align-items: flex-start !important;
}
.tcd-author-avatar {
  flex-shrink: 0 !important;
  width: 72px !important;
  height: 72px !important;
  border-radius: 50% !important;
  overflow: hidden !important;
}
.tcd-author-avatar-fallback {
  width: 100% !important;
  height: 100% !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  background: #e8e8e8 !important;
  font-size: 28px !important;
}
.tcd-author-label {
  font-size: 11px !important;
  font-weight: 600 !important;
  color: #999 !important;
  letter-spacing: .04em !important;
  margin-bottom: 2px !important;
}
.tcd-author-name {
  font-size: 18px !important;
  font-weight: 700 !important;
  color: #333 !important;
  margin-bottom: 8px !important;
}
.tcd-author-desc {
  font-size: 14px !important;
  color: #666 !important;
  line-height: 1.8 !important;
  margin: 0 !important;
}

/* --- Sidebar TOC (injected by JS) --- */
.tcd-sidebar-toc {
  background: #fff !important;
  border: 1px solid #eee !important;
  border-radius: 4px !important;
  padding: 16px !important;
}
.tcd-sidebar-toc-list {
  list-style: none !important;
  padding: 0 !important;
  margin: 0 !important;
  counter-reset: stoc !important;
}
.tcd-stoc-h2 {
  counter-increment: stoc !important;
  padding: 4px 0 !important;
}
.tcd-stoc-h2 > a {
  font-size: 13px !important;
  font-weight: 600 !important;
  color: #333 !important;
  text-decoration: none !important;
  line-height: 1.6 !important;
  display: block !important;
  border-left: 3px solid transparent !important;
  padding-left: 10px !important;
  border-bottom: none !important;
  background: none !important;
  transition: all 0.2s ease !important;
}
.tcd-stoc-h2 > a::before {
  content: counter(stoc) ". " !important;
  color: #999 !important;
}
.tcd-stoc-h2 > a:hover { color: #0066CC !important; }
.tcd-stoc-h2 > a.tcd-stoc-active {
  color: #0066CC !important;
  border-left-color: #0066CC !important;
}
.tcd-stoc-sub {
  list-style: none !important;
  padding: 0 0 0 14px !important;
  margin: 0 !important;
}
.tcd-stoc-h3 { padding: 2px 0 !important; }
.tcd-stoc-h3 a {
  font-size: 12px !important;
  font-weight: 400 !important;
  color: #999 !important;
  text-decoration: none !important;
  line-height: 1.6 !important;
  display: block !important;
  padding-left: 10px !important;
  border-left: 2px solid transparent !important;
  border-bottom: none !important;
  background: none !important;
  transition: all 0.2s ease !important;
}
.tcd-stoc-h3 a:hover { color: #0066CC !important; }
.tcd-stoc-h3 a.tcd-stoc-active {
  color: #0066CC !important;
  border-left-color: #0066CC !important;
}

/* --- Floating Back to Top --- */
.tcd-totop {
  position: fixed !important;
  bottom: 30px !important;
  right: 30px !important;
  width: 44px !important;
  height: 44px !important;
  border-radius: 50% !important;
  background: rgba(51,51,51,0.85) !important;
  color: #fff !important;
  border: none !important;
  cursor: pointer !important;
  font-size: 18px !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  z-index: 99 !important;
  transition: all 0.3s ease !important;
  box-shadow: 0 2px 8px rgba(0,0,0,0.15) !important;
}
.tcd-totop:hover {
  background: rgba(51,51,51,1) !important;
  transform: scale(1.1) !important;
}

/* Mobile TOC Button (hidden on desktop) */
.tcd-mtoc-btn { display: none !important; }
.tcd-mtoc-overlay { display: none !important; }

/* --- Comments styling --- */
body.single .wp-block-comments {
  max-width: none !important;
  margin: 32px 0 !important;
  padding: 28px !important;
  background: #fff !important;
  border: 1px solid #eee !important;
  border-radius: 4px !important;
}
body.single .wp-block-comments h2 {
  font-size: 20px !important;
  background: none !important;
  border: none !important;
  border-bottom: 2px solid #333 !important;
  padding: 0 0 12px !important;
  margin: 0 0 20px !important;
}

/* --- Post Navigation --- */
body.single nav[aria-label] {
  margin: 20px 0 !important;
  padding: 16px 0 !important;
}
body.single .wp-block-post-navigation-link a {
  color: #333 !important;
  text-decoration: none !important;
  font-size: 14px !important;
  border-bottom: none !important;
  background: none !important;
}
body.single .wp-block-post-navigation-link a:hover {
  color: #0066CC !important;
}

/* --- Related Posts (template query block) --- */
body.single .wp-block-query .wp-block-post-title a {
  color: #333 !important;
  text-decoration: none !important;
  font-size: 15px !important;
  font-weight: 600 !important;
  border-bottom: none !important;
  background: none !important;
}
body.single .wp-block-query .wp-block-post-title a:hover {
  color: #0066CC !important;
}
body.single .wp-block-query .wp-block-post-date {
  font-size: 13px !important;
  color: #999 !important;
}

/* --- Visual Components --- */
.nao-tip {
  max-width: none !important;
  margin: 32px 0 !important;
  padding: 24px 28px !important;
  background: #f0f7ff !important;
  border-radius: 4px !important;
  border-left: 4px solid #0066CC !important;
  position: relative !important;
}
.nao-tip-title {
  font-size: 15px !important;
  font-weight: 700 !important;
  color: #0066CC !important;
  margin-bottom: 8px !important;
}
.nao-warn {
  max-width: none !important;
  margin: 32px 0 !important;
  padding: 24px 28px !important;
  background: #fff8e1 !important;
  border-radius: 4px !important;
  border-left: 4px solid #f9a825 !important;
  position: relative !important;
}
"""

# Mobile CSS
TCD_MOBILE_CSS = """
@media (max-width: 1079px) {
  .nao-tcd-sidebar { display: none !important; }
  body.single .wp-site-blocks {
    display: block !important;
    padding: 0 16px !important;
  }

  body.single .wp-block-post-title {
    font-size: 22px !important;
    line-height: 1.45 !important;
  }

  body.single .entry-content h2 {
    font-size: 19px !important;
    padding: 16px 18px !important;
    margin: 40px 0 20px !important;
  }
  body.single .entry-content h3 {
    font-size: 17px !important;
    padding: 12px 0 12px 16px !important;
    margin: 32px 0 16px !important;
  }

  body.single .entry-content,
  body.single .entry-content p {
    font-size: 15px !important;
    line-height: 2 !important;
  }

  .tcd-share {
    flex-direction: column !important;
    gap: 10px !important;
  }
  .tcd-share-btn {
    padding: 8px 14px !important;
    font-size: 12px !important;
  }

  .tcd-author {
    padding: 20px !important;
  }
  .tcd-author-inner {
    flex-direction: column !important;
    align-items: center !important;
    text-align: center !important;
    gap: 12px !important;
  }
  .tcd-author-avatar {
    width: 56px !important;
    height: 56px !important;
  }
  .tcd-author-desc {
    text-align: left !important;
    font-size: 13px !important;
  }

  .tcd-toc {
    padding: 16px 18px !important;
  }
  .tcd-toc-title { font-size: 14px !important; }
  .tcd-toc-h2 > a { font-size: 13px !important; }
  .tcd-toc-h3 a { font-size: 12px !important; }

  .tcd-totop {
    bottom: 70px !important;
    right: 16px !important;
    width: 38px !important;
    height: 38px !important;
    font-size: 16px !important;
  }

  /* Mobile TOC floating button */
  .tcd-mtoc-btn {
    display: flex !important;
    position: fixed !important;
    bottom: 20px !important;
    left: 50% !important;
    transform: translateX(-50%) !important;
    z-index: 98 !important;
    background: rgba(51,51,51,0.9) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 20px !important;
    padding: 10px 22px !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    cursor: pointer !important;
    box-shadow: 0 4px 16px rgba(0,0,0,0.2) !important;
    align-items: center !important;
    gap: 6px !important;
  }

  .tcd-mtoc-overlay {
    position: fixed !important;
    top: 0 !important; left: 0 !important; right: 0 !important; bottom: 0 !important;
    z-index: 9999 !important;
    background: rgba(0,0,0,0.5) !important;
    align-items: flex-end !important;
    justify-content: center !important;
  }
  .tcd-mtoc-inner {
    background: #fff !important;
    border-radius: 16px 16px 0 0 !important;
    width: 100% !important;
    max-height: 70vh !important;
    overflow-y: auto !important;
    padding: 20px !important;
  }
  .tcd-mtoc-header {
    display: flex !important;
    justify-content: space-between !important;
    align-items: center !important;
    font-size: 16px !important;
    font-weight: 700 !important;
    color: #333 !important;
    padding-bottom: 12px !important;
    border-bottom: 1px solid #eee !important;
    margin-bottom: 12px !important;
  }
  .tcd-mtoc-close {
    background: none !important;
    border: none !important;
    font-size: 20px !important;
    color: #999 !important;
    cursor: pointer !important;
  }
  .tcd-mtoc-list {
    list-style: none !important;
    padding: 0 !important;
    margin: 0 !important;
  }
  .tcd-mtoc-h2 { padding: 8px 0 !important; }
  .tcd-mtoc-h2 a {
    font-size: 15px !important;
    font-weight: 600 !important;
    color: #333 !important;
    text-decoration: none !important;
    display: block !important;
    border-bottom: none !important;
    background: none !important;
  }
  .tcd-mtoc-h3 { padding: 5px 0 5px 16px !important; }
  .tcd-mtoc-h3 a {
    font-size: 14px !important;
    font-weight: 400 !important;
    color: #666 !important;
    text-decoration: none !important;
    display: block !important;
    border-bottom: none !important;
    background: none !important;
  }

  body.single .nao-m-bottom { display: none !important; }
}
"""

# Desktop 2-column layout CSS
TCD_LAYOUT_CSS = """
/* === TCD 2-Column Layout (1080px+) === */
@media (max-width: 1079px) {
  .nao-tcd-sidebar { display: none !important; }
}

@media (min-width: 1080px) {
  body.single { background: #f5f5f5 !important; }

  body.single .wp-site-blocks {
    max-width: 1100px !important;
    margin: 0 auto !important;
    display: grid !important;
    grid-template-columns: 1fr 280px !important;
    gap: 40px !important;
    padding: 0 30px !important;
    align-items: start !important;
  }

  body.single .wp-site-blocks > header,
  body.single .wp-site-blocks > footer,
  body.single .wp-site-blocks > .wp-block-template-part {
    grid-column: 1 / -1 !important;
  }

  body.single main.wp-block-group {
    grid-column: 1 / 2 !important;
    background: #fff !important;
    border-radius: 4px !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06) !important;
    padding: 40px !important;
    min-width: 0 !important;
  }

  .nao-tcd-sidebar {
    grid-column: 2 / 3 !important;
    grid-row: 2 / 99 !important;
    position: sticky !important;
    top: 64px !important;
    max-height: calc(100vh - 80px) !important;
    overflow-y: auto !important;
    display: block !important;
  }

  body.single .wp-block-comments {
    background: #fff !important;
    border-radius: 4px !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06) !important;
    padding: 40px !important;
  }
}

/* --- Sidebar Widgets --- */
.nao-tcd-sidebar-inner {
  display: flex;
  flex-direction: column;
  gap: 20px;
}
.nao-tcd-widget {
  background: #fff;
  border: 1px solid #eee;
  border-radius: 4px;
  padding: 16px;
}
.nao-tcd-widget-title {
  font-size: 14px !important;
  font-weight: 700 !important;
  color: #333 !important;
  padding-bottom: 10px !important;
  border-bottom: 2px solid #333 !important;
  margin-bottom: 12px !important;
  background: none !important;
  border-left: none !important;
  border-top: none !important;
  border-right: none !important;
}
.nao-tcd-search {
  display: flex;
  gap: 6px;
}
.nao-tcd-search-input {
  flex: 1;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  outline: none;
}
.nao-tcd-search-input:focus { border-color: #999; }
.nao-tcd-search-btn {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background: #fff;
  cursor: pointer;
  color: #666;
}
.nao-tcd-search-btn:hover { background: #f5f5f5; }

.nao-tcd-post-list {
  list-style: none !important;
  padding: 0 !important;
  margin: 0 !important;
}
.nao-tcd-post-list li { border-bottom: 1px solid #f0f0f0; }
.nao-tcd-post-list li:last-child { border-bottom: none; }
.nao-tcd-post-list a {
  display: block;
  padding: 10px 0;
  text-decoration: none !important;
  border-bottom: none !important;
  background: none !important;
}
.nao-tcd-post-list a:hover .nao-tcd-post-title { color: #0066CC; }
.nao-tcd-post-cat {
  display: inline-block;
  font-size: 10px;
  font-weight: 600;
  color: #999;
  background: #f5f5f5;
  padding: 1px 6px;
  border-radius: 2px;
  margin-bottom: 2px;
}
.nao-tcd-post-title {
  display: block;
  font-size: 13px;
  color: #333;
  line-height: 1.5;
  transition: color 0.2s ease;
}

.nao-tcd-cat-list {
  list-style: none !important;
  padding: 0 !important;
  margin: 0 !important;
}
.nao-tcd-cat-list li { border-bottom: 1px solid #f0f0f0; }
.nao-tcd-cat-list li:last-child { border-bottom: none; }
.nao-tcd-cat-list a {
  display: flex;
  justify-content: space-between;
  padding: 8px 0;
  text-decoration: none !important;
  border-bottom: none !important;
  background: none !important;
}
.nao-tcd-cat-name { font-size: 14px; color: #333; }
.nao-tcd-cat-count { font-size: 13px; color: #999; }
.nao-tcd-cat-list a:hover .nao-tcd-cat-name { color: #0066CC; }

.nao-tcd-about p {
  font-size: 13px;
  color: #666;
  line-height: 1.7;
  margin: 0 0 8px;
}
.nao-tcd-about-link {
  font-size: 13px;
  color: #0066CC !important;
  text-decoration: none !important;
  border-bottom: none !important;
  background: none !important;
}
.nao-tcd-about-link:hover { text-decoration: underline !important; }
"""


def minify_css(raw):
    css = re.sub(r'/\*.*?\*/', '', raw, flags=re.DOTALL)
    css = re.sub(r'\s+', ' ', css)
    for ch in '{}:;,':
        css = re.sub(rf'\s*\{re.escape(ch)}\s*', ch, css)
    return css.strip()


def minify_js(raw):
    js = re.sub(r'/\*.*?\*/', '', raw, flags=re.DOTALL)
    js = re.sub(r'(?<!:)//[^\n]*', '', js)
    js = re.sub(r'\s+', ' ', js)
    return js.strip()


def main():
    print('=== Update Single Template: TCD Style ===\n')

    # 1. Get current template
    print('[1/3] Getting template...')
    url = f'{URL}/templates/{TEMPLATE_SLUG}'
    r = requests.get(url, headers=HEADERS, params={'context': 'edit'}, timeout=15)
    if r.status_code != 200:
        print(f'  FAIL: {r.status_code}')
        return
    raw = r.json().get('content', {}).get('raw', '')
    print(f'  Template length: {len(raw)}')

    # 2. Remove all existing inline CSS and JS blocks
    print('\n[2/3] Replacing inline CSS/JS...')

    # Remove ALL <!-- wp:html --> blocks that contain <style> or <script>
    cleaned = re.sub(
        r'<!-- wp:html -->\s*<style>.*?</style>\s*<!-- /wp:html -->\s*',
        '', raw, flags=re.DOTALL
    )
    cleaned = re.sub(
        r'<!-- wp:html -->\s*<script>.*?</script>\s*<!-- /wp:html -->\s*',
        '', cleaned, flags=re.DOTALL
    )
    print(f'  After removing inline blocks: {len(cleaned)}')

    # 3. Build new CSS + JS blocks
    all_css = TCD_CSS + '\n' + TCD_MOBILE_CSS + '\n' + TCD_LAYOUT_CSS
    mini_css = minify_css(all_css)
    print(f'  CSS: {len(mini_css)} chars')

    raw_js = JS_FILE.read_text(encoding='utf-8')
    mini_js = minify_js(raw_js)
    print(f'  JS: {len(mini_js)} chars')

    # Split CSS into chunks to avoid WAF (max ~3000 chars per block)
    css_chunks = []
    rules = re.split(r'(})', mini_css)
    temp = ''
    for i in range(0, len(rules) - 1, 2):
        rule = rules[i] + (rules[i + 1] if i + 1 < len(rules) else '')
        if len(temp) + len(rule) > 2800 and temp:
            css_chunks.append(temp)
            temp = rule
        else:
            temp += rule
    if temp.strip():
        css_chunks.append(temp)

    print(f'  CSS chunks: {len(css_chunks)}')

    # Build the inline blocks
    inline_blocks = ''
    for chunk in css_chunks:
        inline_blocks += f'<!-- wp:html --><style>{chunk}</style><!-- /wp:html -->\n'

    # JS block
    inline_blocks += f'<!-- wp:html --><script>/* TCD-SINGLE */{mini_js}</script><!-- /wp:html -->\n'

    # Insert inline blocks before <main>
    main_marker = '<!-- wp:group {"tagName":"main"'
    main_pos = cleaned.find(main_marker)
    if main_pos >= 0:
        new_content = cleaned[:main_pos] + inline_blocks + cleaned[main_pos:]
    else:
        # Fallback: insert after sidebar
        sidebar_end = cleaned.find('</aside>')
        if sidebar_end > 0:
            insert_pos = cleaned.find('<!-- /wp:html -->', sidebar_end) + len('<!-- /wp:html -->')
            new_content = cleaned[:insert_pos] + '\n' + inline_blocks + cleaned[insert_pos:]
        else:
            new_content = inline_blocks + cleaned

    print(f'  New template length: {len(new_content)}')

    # 4. Update template
    print('\n[3/3] Updating template...')
    r2 = requests.post(url, headers=HEADERS, json={'content': new_content}, timeout=60)
    if r2.status_code == 200:
        print('  Template updated OK!')
    else:
        print(f'  FAIL: {r2.status_code}')
        print(f'  Response: {r2.text[:500]}')

    print('\n=== Done! Check https://nambei-oyaji.com/paraguay-ijuu-hiyou/ ===')


if __name__ == '__main__':
    main()
