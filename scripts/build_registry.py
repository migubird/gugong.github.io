#!/usr/bin/env python3
"""
Build pages.json registry from docs/ directory.
Generates both the flat pages.json (for inline JS) and alias index for search.
"""

import json
import os
import re
from pathlib import Path

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS_DIR = os.path.join(BASE_DIR, "docs")
OUTPUT_FILE = os.path.join(DOCS_DIR, "pages.json")

# Type mapping from directory name
TYPE_MAP = {
    "palaces": "palace",
    "emperors": "emperor",
    "figures": "figure",
    "events": "event",
}

# Load existing alias map
def load_alias_map():
    alias_file = os.path.join(BASE_DIR, "kg", "entities", "data", "alias_map.json")
    if os.path.exists(alias_file):
        with open(alias_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def scan_docs():
    """Scan docs/ directory and build page registry."""
    pages = {}

    for dir_name, type_name in TYPE_MAP.items():
        dir_path = os.path.join(DOCS_DIR, dir_name)
        if not os.path.exists(dir_path):
            continue

        for fname in os.listdir(dir_path):
            if not fname.endswith(".html"):
                continue

            # Extract entity name from filename
            name = fname.replace(".html", "")
            # Convert kebab-case to Chinese by looking at HTML title
            filepath = os.path.join(dir_path, fname)
            title = extract_title(filepath)
            if not title:
                title = name.replace("-", " ").title()

            url = f"docs/{dir_name}/{fname}"

            # Register by canonical name
            pages[title] = {
                "url": url,
                "type": type_name,
                "name": title,
            }

    return pages


def extract_title(filepath):
    """Extract Chinese title from HTML file."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read(2000)
        # Look for <h1>...</h1>
        match = re.search(r"<h1[^>]*>(.*?)</h1>", content, re.DOTALL)
        if match:
            return match.group(1).strip()
        # Look for <title>...</title>
        match = re.search(r"<title>(.*?)</title>", content, re.DOTALL)
        if match:
            title = match.group(1).strip()
            # Remove " - 故宫知识图谱" suffix
            title = re.sub(r"\s*-\s*故宫知识图谱.*", "", title)
            return title
    except Exception:
        pass
    return None


def merge_aliases(pages, alias_map):
    """Add alias entries pointing to the same page."""
    alias_entries = {}
    for alias_name, info in alias_map.items():
        canonical_id = info.get("canonical_id", "")
        entity_type = info.get("type", "")

        # Find the matching page
        for page_name, page_info in pages.items():
            if canonical_id in page_info.get("url", ""):
                alias_entries[alias_name] = {
                    "url": page_info["url"],
                    "type": entity_type or page_info["type"],
                    "alias_of": page_name,
                }
                break

    # Merge aliases into pages
    pages.update(alias_entries)
    return pages


def main():
    print("Scanning docs/ directory...")
    pages = scan_docs()
    print(f"Found {len(pages)} canonical pages")

    # Merge aliases
    alias_map = load_alias_map()
    if alias_map:
        pages = merge_aliases(pages, alias_map)
        print(f"Added {len(alias_map)} alias entries")

    print(f"Total entries: {len(pages)}")

    # Write pages.json
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(pages, f, ensure_ascii=False, indent=2)

    print(f"Written to {OUTPUT_FILE}")

    # Print type breakdown
    type_counts = {}
    for p in pages.values():
        t = p.get("type", "unknown")
        type_counts[t] = type_counts.get(t, 0) + 1
    for t, c in sorted(type_counts.items()):
        print(f"  {t}: {c}")


if __name__ == "__main__":
    main()
