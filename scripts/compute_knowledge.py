#!/usr/bin/env python3
"""
Compute Knowledge metric (K-value) for the Gugong Knowledge Graph.
Tracks knowledge growth over time.

K = log2(1 + bytes) * (1 + links_density) * type_weight * quality_norm

Inspired by shiji-kb's knowledge metric system.
"""

import json
import math
import os
import sys
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KG_DIR = os.path.join(BASE_DIR, "kg")
DOCS_DIR = os.path.join(BASE_DIR, "docs")

# Type weights (more specific/rare types = higher weight)
TYPE_WEIGHTS = {
    "emperor": 1.5,    # Core entities
    "palace": 1.3,     # Spatial core
    "figure": 1.0,     # Standard entities
    "event": 1.2,      # Dynamic entities
    "artifact": 0.8,   # Supplementary
    "title": 0.6,      # Supporting
}


def compute_entity_k(entity_data, entity_type):
    """Compute K-value for a single entity."""
    # Bytes: size of entity data
    entity_bytes = len(json.dumps(entity_data, ensure_ascii=False))

    # Links density: number of relations per byte
    num_relations = len(entity_data.get("related_events", [])) + \
                    len(entity_data.get("related_emperors", [])) + \
                    len(entity_data.get("related_figures", [])) + \
                    len(entity_data.get("related_palaces", []))
    links_density = num_relations / max(entity_bytes, 1) * 1000  # per 1000 bytes

    # Type weight
    type_weight = TYPE_WEIGHTS.get(entity_type, 1.0)

    # Quality norm: based on field completeness
    required_fields = {"name", "description"}
    optional_fields = {"aliases", "time_range", "source", "coordinates", "related_events",
                       "related_emperors", "related_figures", "related_palaces"}

    present_required = sum(1 for f in required_fields if entity_data.get(f))
    present_optional = sum(1 for f in optional_fields if entity_data.get(f))

    quality_norm = 0.5 + 0.3 * (present_required / max(len(required_fields), 1)) + \
                   0.2 * (present_optional / max(len(optional_fields), 1))

    # K formula
    k_value = math.log2(1 + entity_bytes) * (1 + links_density) * type_weight * quality_norm
    return round(k_value, 2)


def compute_page_k(filepath):
    """Compute K-value for a docs/ page based on content length and links."""
    if not os.path.exists(filepath):
        return 0

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    page_bytes = len(content.encode("utf-8"))

    # Count wikilinks/anchors
    link_count = content.count("href=")
    links_density = link_count / max(page_bytes, 1) * 1000

    k_value = math.log2(1 + page_bytes) * (1 + links_density)
    return round(k_value, 2)


def scan_all_entities():
    """Scan all entity indexes and compute K-values."""
    entity_files = {
        "emperor": "entities/data/emperors_index.json",
        "palace": "entities/data/palaces_index.json",
        "figure": "entities/data/figures_index.json",
    }

    total_k = 0
    entity_ks = {}
    type_breakdown = {}

    for etype, path in entity_files.items():
        filepath = os.path.join(KG_DIR, path)
        if not os.path.exists(filepath):
            continue

        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        type_k = 0
        for eid, entity in data.items():
            k = compute_entity_k(entity, etype)
            entity_ks[eid] = {"name": entity.get("name", ""), "type": etype, "k": k}
            type_k += k

        type_breakdown[etype] = {
            "count": len(data),
            "total_k": round(type_k, 2),
            "avg_k": round(type_k / max(len(data), 1), 2),
        }
        total_k += type_k

    return {
        "entities": entity_ks,
        "total_k": round(total_k, 2),
        "type_breakdown": type_breakdown,
    }


def scan_all_pages():
    """Scan all docs/ pages and compute K-values."""
    dirs = ["palaces", "emperors", "figures", "events"]
    total_k = 0
    page_ks = {}

    for dir_name in dirs:
        dir_path = os.path.join(DOCS_DIR, dir_name)
        if not os.path.exists(dir_path):
            continue

        for fname in os.listdir(dir_path):
            if not fname.endswith(".html"):
                continue
            filepath = os.path.join(dir_path, fname)
            k = compute_page_k(filepath)
            page_ks[fname] = k
            total_k += k

    return {
        "pages": page_ks,
        "total_k": round(total_k, 2),
        "count": len(page_ks),
        "avg_k": round(total_k / max(len(page_ks), 1), 2),
    }


def main():
    print("=" * 60)
    print("故宫知识图谱 — 知识度量 (K-Value)")
    print("=" * 60)

    # Entity K-values
    print("\n[1] 实体知识度量")
    entity_result = scan_all_entities()
    print(f"  总 K 值: {entity_result['total_k']}")
    for etype, info in entity_result["type_breakdown"].items():
        print(f"  {etype}: {info['count']} 个, K={info['total_k']}, 平均 K={info['avg_k']}")

    # Page K-values
    print("\n[2] 页面知识度量")
    page_result = scan_all_pages()
    print(f"  总 K 值: {page_result['total_k']}")
    print(f"  页面数: {page_result['count']}")
    print(f"  平均 K/页: {page_result['avg_k']}")

    # Combined
    combined_k = entity_result["total_k"] + page_result["total_k"]
    print(f"\n[3] 综合知识度量")
    print(f"  总 K 值: {round(combined_k, 2)}")

    # Top entities by K
    print(f"\n[4] Top 10 高价值实体:")
    sorted_entities = sorted(entity_result["entities"].items(),
                            key=lambda x: x[1]["k"], reverse=True)
    for i, (eid, info) in enumerate(sorted_entities[:10]):
        print(f"  {i+1}. {info['name']} ({eid}) K={info['k']}")

    # Save report
    report = {
        "timestamp": datetime.now().isoformat(),
        "entity_k": entity_result["total_k"],
        "page_k": page_result["total_k"],
        "combined_k": round(combined_k, 2),
        "entity_types": entity_result["type_breakdown"],
        "pages": {
            "count": page_result["count"],
            "total_k": page_result["total_k"],
            "avg_k": page_result["avg_k"],
        },
        "top_entities": [{"id": eid, **info} for eid, info in sorted_entities[:10]],
    }

    report_path = os.path.join(KG_DIR, "knowledge_report.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"\n📄 报告已保存到 {report_path}")


if __name__ == "__main__":
    main()
