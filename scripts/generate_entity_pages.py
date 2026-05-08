#!/usr/bin/env python3
"""
Generate wiki pages for all entities in kg/ data.
Creates HTML pages in docs/{type}/ with consistent formatting.

Usage:
    python3 scripts/generate_entity_pages.py              # Generate all
    python3 scripts/generate_entity_pages.py --type palace # Generate specific type
    python3 scripts/generate_entity_pages.py --dry-run     # Preview only
"""

import json
import os
import re
import argparse
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KG_DIR = os.path.join(BASE_DIR, "kg")
DOCS_DIR = os.path.join(BASE_DIR, "docs")

# Load all data
def load_json(path):
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_all_relations():
    """Load all relation files and build a lookup by entity."""
    relations = {}
    rel_dir = os.path.join(KG_DIR, "relations/data")
    if not os.path.exists(rel_dir):
        return relations

    for fname in os.listdir(rel_dir):
        if not fname.endswith(".json"):
            continue
        data = load_json(os.path.join(rel_dir, fname))
        rel_list = data if isinstance(data, list) else data.get("relations", [])
        for rel in rel_list:
            from_id = rel.get("from", "")
            to_id = rel.get("to", "")
            if from_id not in relations:
                relations[from_id] = []
            relations[from_id].append(rel)
            if to_id not in relations:
                relations[to_id] = []
            relations[to_id].append(rel)

    return relations

def load_all_entities():
    """Load all entity indexes."""
    entities = {}
    for idx_file in ["entities/data/emperors_index.json",
                     "entities/data/palaces_index.json",
                     "entities/data/figures_index.json"]:
        data = load_json(os.path.join(KG_DIR, idx_file))
        entities.update(data)
    return entities

def generate_page_html(entity, entity_id, entity_type, relations, all_entities):
    """Generate HTML page for an entity."""
    name = entity.get("name", entity_id)
    aliases = entity.get("aliases", [])
    description = entity.get("description", "暂无详细描述")
    time_range = entity.get("time_range", {})
    source = entity.get("source", "")

    # Get related entities
    related = relations.get(entity_id, [])

    # Group relations by type
    rel_by_type = {}
    for rel in related:
        rtype = rel.get("type", "其他")
        if rtype not in rel_by_type:
            rel_by_type[rtype] = []
        # Find the other entity
        other_id = rel.get("to") if rel.get("from") == entity_id else rel.get("from")
        other_name = other_id
        if other_id in all_entities:
            other_name = all_entities[other_id].get("name", other_id)
        rel_by_type[rtype].append({
            "name": other_name,
            "id": other_id,
            "year": rel.get("year", ""),
            "note": rel.get("note", ""),
        })

    # Build wiki links for aliases
    alias_links = []
    for a in aliases:
        alias_links.append(f'<a href="../search.html?q={a}" class="alias-link">{a}</a>')

    # Build related entity links
    related_html = ""
    for rtype, items in sorted(rel_by_type.items()):
        related_html += f"<h3>{rtype}</h3><ul>"
        for item in items:
            slug = item["name"]
            link = f"../figures/{slug}.html"
            # Try to find correct link
            for etype in ["emperors", "palaces", "figures", "events"]:
                if os.path.exists(os.path.join(DOCS_DIR, etype, f"{slug}.html")):
                    link = f"../{etype}/{slug}.html"
                    break
            year_str = f" ({item['year']})" if item["year"] else ""
            note_str = f" — {item['note']}" if item["note"] else ""
            related_html += f'<li><a href="{link}">{item["name"]}</a>{year_str}{note_str}</li>'
        related_html += "</ul>"

    # Timeline info
    timeline_html = ""
    if time_range:
        start = time_range.get("start", "")
        end = time_range.get("end", "")
        if start and end:
            timeline_html = f"{start} — {end}"
        elif start:
            timeline_html = str(start)

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{name} - 故宫知识图谱</title>
  <link rel="stylesheet" href="../css/wiki.css">
</head>
<body>
<header>
  <div class="nav">
    <a href="../index.html">首页</a> |
    <a href="../palaces/">宫殿</a> |
    <a href="../emperors/">皇帝</a> |
    <a href="../figures/">人物</a> |
    <a href="../events/">事件</a>
  </div>
  <h1>{name}</h1>
</header>
<div class="container">
  <div class="type-badge">{entity_type}</div>
  <div class="desc">{description}</div>

  <div class="meta-grid">
    <div class="meta-label">别名</div>
    <div class="meta-value">{', '.join(aliases) if aliases else '无'}</div>
    <div class="meta-label">时间</div>
    <div class="meta-value">{timeline_html or '不详'}</div>
    <div class="meta-label">来源</div>
    <div class="meta-value">{source or '待补充'}</div>
  </div>

  <h2>关联信息</h2>
  {related_html or '<p>暂无关联信息</p>'}

</div>
<footer>
  <p>故宫知识图谱 &middot; 2026 &middot; CC BY-NC-SA 4.0</p>
</footer>
</body>
</html>"""

    return html


def name_to_slug(name):
    """Convert entity name to filename slug."""
    # Chinese names: use the name directly
    if any('\u4e00' <= c <= '\u9fff' for c in name):
        return name
    # English/pinyin: lowercase and replace spaces with hyphens
    return name.lower().replace(" ", "-")


def main():
    parser = argparse.ArgumentParser(description="Generate entity wiki pages")
    parser.add_argument("--type", choices=["emperor", "palace", "figure"], help="Generate specific type only")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing files")
    args = parser.parse_args()

    print("Loading knowledge graph data...")
    all_entities = load_all_entities()
    relations = load_all_relations()
    print(f"Loaded {len(all_entities)} entities, {sum(len(v) for v in relations.values())} relation entries")

    type_dirs = {
        "emperor": "emperors",
        "palace": "palaces",
        "figure": "figures",
    }

    total = 0
    generated = 0

    for entity_id, entity in all_entities.items():
        etype = entity.get("type", "")

        # Filter by type if specified
        if args.type and etype != args.type:
            continue

        total += 1

        dir_name = type_dirs.get(etype)
        if not dir_name:
            continue

        name = entity.get("name", entity_id)
        slug = name_to_slug(name)
        filename = f"{slug}.html"
        filepath = os.path.join(DOCS_DIR, dir_name, filename)

        if args.dry_run:
            print(f"  Would generate: {dir_name}/{filename}")
            continue

        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        html = generate_page_html(entity, entity_id, etype, relations, all_entities)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)
        generated += 1

    if args.dry_run:
        print(f"\nDry run: would generate {total} pages")
    else:
        print(f"\nGenerated {generated} pages in docs/")

        # Update registry
        print("Updating pages.json...")
        os.system(f"cd {BASE_DIR} && python3 scripts/build_registry.py")


if __name__ == "__main__":
    main()
