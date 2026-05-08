#!/usr/bin/env python3
"""
Extract entities and relations from historical text corpus.
Uses pattern matching and rule-based extraction for Chinese historical texts.

Usage:
    python3 scripts/extract_entities.py corpus/明史-宫殿志.md
    python3 scripts/extract_entities.py --all  # Process all corpus files
"""

import json
import os
import re
import sys
import argparse

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KG_DIR = os.path.join(BASE_DIR, "kg")
CORPUS_DIR = os.path.join(BASE_DIR, "corpus")


class EntityExtractor:
    def __init__(self):
        self.entities = []
        self.relations = []
        self.existing_entities = self._load_existing_entities()

    def _load_existing_entities(self):
        """Load existing entity IDs to avoid duplicates."""
        existing = {}
        for idx_file in ["entities/data/emperors_index.json",
                        "entities/data/palaces_index.json",
                        "entities/data/figures_index.json"]:
            path = os.path.join(KG_DIR, idx_file)
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                for eid, ent in data.items():
                    existing[ent.get("name", "")] = eid
                    for alias in ent.get("aliases", []):
                        existing[alias] = eid
        return existing

    def extract_from_text(self, text, source=""):
        """Extract entities and relations from text."""
        self._extract_emperors(text, source)
        self._extract_palaces(text, source)
        self._extract_events(text, source)
        self._extract_relations(text, source)
        return self.entities, self.relations

    def _extract_emperors(self, text, source):
        """Extract emperor mentions."""
        # Pattern: 皇帝/帝 + 庙号/谥号
        patterns = [
            r'([\u4e00-\u9fff]{1,2})帝',
            r'([\u4e00-\u9fff]+)皇帝',
            r'([\u4e00-\u9fff]+?)(?:元年|二年|三年|四年|五年|六年|七年|八年|九年|十年)',
        ]
        for pattern in patterns:
            for match in re.finditer(pattern, text):
                name = match.group(1)
                if name not in self.existing_entities:
                    self.entities.append({
                        "type": "emperor",
                        "name": name,
                        "source": source,
                        "context": match.group(0),
                    })

    def _extract_palaces(self, text, source):
        """Extract palace/building mentions."""
        palace_suffixes = ['殿', '宫', '门', '阁', '亭', '楼', '坊', '园', '苑', '堂', '斋', '馆', '所', '处', '库', '房']
        for suffix in palace_suffixes:
            pattern = rf'([\u4e00-\u9fff]{{1,5}}{suffix})'
            for match in re.finditer(pattern, text):
                name = match.group(1)
                # Filter out common non-palace words
                if name not in ('圣旨', '天下', '国家', '天下'):
                    if name not in self.existing_entities:
                        self.entities.append({
                            "type": "palace",
                            "name": name,
                            "source": source,
                            "context": match.group(0),
                        })

    def _extract_events(self, text, source):
        """Extract event mentions."""
        event_patterns = [
            r'([\u4e00-\u9fff]{2,10}之[变乱役祸难争战局约盟])',
            r'(?:始|建|造|修|建)于([\u4e00-\u9fff]+?)(?:年|间)',
        ]
        for pattern in event_patterns:
            for match in re.finditer(pattern, text):
                name = match.group(1)
                self.entities.append({
                    "type": "event",
                    "name": name,
                    "source": source,
                    "context": match.group(0),
                })

    def _extract_relations(self, text, source):
        """Extract relationship patterns from text."""
        # A 居住于 B
        for match in re.finditer(r'([\u4e00-\u9fff]{2,8})居住于([\u4e00-\u9fff]{2,8})', text):
            self.relations.append({
                "from": match.group(1),
                "to": match.group(2),
                "type": "居住于",
                "source": source,
            })

        # A 主持修建 B
        for match in re.finditer(r'([\u4e00-\u9fff]{2,8})主持修建([\u4e00-\u9fff]{2,8})', text):
            self.relations.append({
                "from": match.group(1),
                "to": match.group(2),
                "type": "主持修建",
                "source": source,
            })

        # B 建于 A年间
        for match in re.finditer(r'([\u4e00-\u9fff]{2,8})建于([\u4e00-\u9fff]+?)(?:年|年间)', text):
            self.relations.append({
                "from": match.group(2),
                "to": match.group(1),
                "type": "发生于",
                "source": source,
            })


def process_file(filepath):
    """Process a single corpus file."""
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return [], []

    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()

    source = os.path.basename(filepath)
    extractor = EntityExtractor()
    entities, relations = extractor.extract_from_text(text, source)
    return entities, relations


def process_all():
    """Process all files in corpus/."""
    all_entities = []
    all_relations = []

    if not os.path.exists(CORPUS_DIR):
        print(f"Corpus directory not found: {CORPUS_DIR}")
        return all_entities, all_relations

    for fname in os.listdir(CORPUS_DIR):
        filepath = os.path.join(CORPUS_DIR, fname)
        if os.path.isfile(filepath):
            entities, relations = process_file(filepath)
            all_entities.extend(entities)
            all_relations.extend(relations)

    return all_entities, all_relations


def save_results(entities, relations, output_dir=None):
    """Save extracted entities and relations."""
    if output_dir is None:
        output_dir = os.path.join(KG_DIR, "extracted")

    os.makedirs(output_dir, exist_ok=True)

    # Save entities
    entity_path = os.path.join(output_dir, "extracted_entities.json")
    with open(entity_path, "w", encoding="utf-8") as f:
        json.dump(entities, f, ensure_ascii=False, indent=2)

    # Save relations
    relation_path = os.path.join(output_dir, "extracted_relations.json")
    with open(relation_path, "w", encoding="utf-8") as f:
        json.dump(relations, f, ensure_ascii=False, indent=2)

    print(f"\nSaved {len(entities)} entities to {entity_path}")
    print(f"Saved {len(relations)} relations to {relation_path}")


def main():
    parser = argparse.ArgumentParser(description="Extract entities from historical text")
    parser.add_argument("file", nargs="?", help="Corpus file to process")
    parser.add_argument("--all", action="store_true", help="Process all corpus files")
    args = parser.parse_args()

    if args.all:
        print("Processing all corpus files...")
        entities, relations = process_all()
    elif args.file:
        print(f"Processing {args.file}...")
        entities, relations = process_file(args.file)
    else:
        print("No input specified. Use --all or provide a file path.")
        sys.exit(1)

    # Print summary
    print(f"\nExtracted {len(entities)} entities:")
    type_counts = {}
    for e in entities:
        t = e.get("type", "unknown")
        type_counts[t] = type_counts.get(t, 0) + 1
    for t, c in sorted(type_counts.items()):
        print(f"  {t}: {c}")

    print(f"\nExtracted {len(relations)} relations")

    # Save results
    save_results(entities, relations)


if __name__ == "__main__":
    main()
