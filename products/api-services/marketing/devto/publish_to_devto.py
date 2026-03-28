"""
Dev.to Article Publisher
Publishes prepared RapidAPI marketing articles to Dev.to as drafts.
Uses Dev.to API v1.

Usage:
  python publish_to_devto.py                    # Publish all unpublished articles as drafts
  python publish_to_devto.py --article 01       # Publish specific article
  python publish_to_devto.py --publish           # Publish as public (not draft)
  python publish_to_devto.py --list              # List existing articles on Dev.to
"""

import json
import sys
import argparse
from pathlib import Path
import requests

SCRIPT_DIR = Path(__file__).parent
MARKETING_DIR = SCRIPT_DIR.parent
CONFIG_PATH = MARKETING_DIR / "dev-to-config.json"
ARTICLES_DIR = MARKETING_DIR / "dev-to-articles"
PUBLISHED_LOG = SCRIPT_DIR / "published_articles.json"


def load_config() -> dict:
    """Load Dev.to API configuration."""
    if not CONFIG_PATH.exists():
        print(f"ERROR: Config not found at {CONFIG_PATH}")
        sys.exit(1)
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def load_published_log() -> dict:
    """Load log of previously published articles."""
    if PUBLISHED_LOG.exists():
        with open(PUBLISHED_LOG, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_published_log(log: dict) -> None:
    """Save published articles log."""
    with open(PUBLISHED_LOG, "w", encoding="utf-8") as f:
        json.dump(log, f, indent=2, ensure_ascii=False)


def parse_article_frontmatter(content: str) -> tuple[dict, str]:
    """Parse frontmatter and body from a Dev.to article markdown file."""
    lines = content.strip().split("\n")

    # Find frontmatter boundaries
    if not lines[0].startswith("---"):
        # No frontmatter — extract title from first heading
        title = lines[0].lstrip("# ").strip()
        body = "\n".join(lines[1:]).strip()
        return {"title": title, "tags": [], "published": False}, body

    end_idx = -1
    for i in range(1, len(lines)):
        if lines[i].startswith("---"):
            end_idx = i
            break

    if end_idx == -1:
        return {"title": "Untitled", "tags": [], "published": False}, content

    frontmatter = {}
    for line in lines[1:end_idx]:
        if ":" in line:
            key, _, value = line.partition(":")
            key = key.strip()
            value = value.strip()
            if key == "tags":
                frontmatter["tags"] = [t.strip() for t in value.split(",") if t.strip()]
            elif key == "published":
                frontmatter["published"] = value.lower() == "true"
            else:
                frontmatter[key] = value

    body = "\n".join(lines[end_idx + 1:]).strip()
    return frontmatter, body


def list_devto_articles(api_key: str) -> None:
    """List existing articles on Dev.to."""
    headers = {"api-key": api_key, "Content-Type": "application/json"}
    resp = requests.get(
        "https://dev.to/api/articles/me/all",
        headers=headers,
        params={"per_page": 50},
        timeout=30,
    )
    resp.raise_for_status()
    articles = resp.json()

    print(f"\n=== Dev.to Articles ({len(articles)} total) ===\n")
    for a in articles:
        status = "PUBLIC" if a.get("published") else "DRAFT"
        views = a.get("page_views_count", 0)
        reactions = a.get("positive_reactions_count", 0)
        print(f"  [{status}] {a['title']}")
        print(f"    URL: {a.get('url', 'N/A')}")
        print(f"    Views: {views} | Reactions: {reactions}")
        print()


def publish_article(api_key: str, filepath: Path, as_public: bool = False) -> dict | None:
    """Publish a single article to Dev.to."""
    content = filepath.read_text(encoding="utf-8")
    frontmatter, body = parse_article_frontmatter(content)

    title = frontmatter.get("title", filepath.stem)
    tags = frontmatter.get("tags", [])

    # Dev.to allows max 4 tags
    tags = tags[:4]

    headers = {"api-key": api_key, "Content-Type": "application/json"}
    payload = {
        "article": {
            "title": title,
            "body_markdown": body,
            "published": as_public,
            "tags": tags,
        }
    }

    print(f"  Publishing: {title}")
    print(f"    Tags: {', '.join(tags)}")
    print(f"    Status: {'PUBLIC' if as_public else 'DRAFT'}")

    resp = requests.post(
        "https://dev.to/api/articles",
        headers=headers,
        json=payload,
        timeout=30,
    )

    if resp.status_code in (200, 201):
        data = resp.json()
        print(f"    SUCCESS: {data.get('url', 'N/A')}")
        return data
    else:
        print(f"    FAILED: {resp.status_code} - {resp.text[:200]}")
        return None


def main():
    parser = argparse.ArgumentParser(description="Publish articles to Dev.to")
    parser.add_argument("--article", type=str, help="Publish specific article by prefix (e.g., '01')")
    parser.add_argument("--publish", action="store_true", help="Publish as public (default: draft)")
    parser.add_argument("--list", action="store_true", help="List existing Dev.to articles")
    parser.add_argument("--force", action="store_true", help="Republish even if already published")
    args = parser.parse_args()

    config = load_config()
    api_key = config["api_key"]

    if args.list:
        list_devto_articles(api_key)
        return

    published_log = load_published_log()

    # Find articles to publish
    article_files = sorted(ARTICLES_DIR.glob("*.md"))
    if not article_files:
        print(f"No articles found in {ARTICLES_DIR}")
        return

    if args.article:
        article_files = [f for f in article_files if f.name.startswith(args.article)]
        if not article_files:
            print(f"No article found with prefix '{args.article}'")
            return

    print(f"\n=== Dev.to Publisher ===")
    print(f"Articles dir: {ARTICLES_DIR}")
    print(f"Found {len(article_files)} article(s)\n")

    published_count = 0
    skipped_count = 0

    for filepath in article_files:
        filename = filepath.name

        if filename in published_log and not args.force:
            print(f"  SKIP (already published): {filename}")
            skipped_count += 1
            continue

        result = publish_article(api_key, filepath, as_public=args.publish)
        if result:
            published_log[filename] = {
                "devto_id": result.get("id"),
                "url": result.get("url"),
                "published": result.get("published", False),
                "published_at": result.get("published_at"),
            }
            published_count += 1

    save_published_log(published_log)

    print(f"\n=== Summary ===")
    print(f"  Published: {published_count}")
    print(f"  Skipped: {skipped_count}")
    print(f"  Total articles on file: {len(article_files)}")


if __name__ == "__main__":
    main()
