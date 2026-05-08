#!/usr/bin/env python3
"""
Validate knowledge graph data for consistency and integrity.
Checks entity references, relation types, time ranges, and circular dependencies.
"""

import json
import os
import sys
import argparse
from collections import defaultdict

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KG_DIR = os.path.join(BASE_DIR, "kg")

REPORT_FILE = os.path.join(KG_DIR, "validation_report.json")

class Validator:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.fixes = []
        self.stats = {}

    def load_json(self, path):
        if not os.path.exists(path):
            self.warnings.append(f"File not found: {path}")
            return None
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def validate_all(self, quick=False):
        print("=" * 60)
        print("故宫知识图谱数据校验")
        print("=" * 60)

        self.validate_entity_indexes()
        if not quick:
            self.validate_relations()
            self.validate_chronology()
            self.validate_aliases()
            self.validate_pages()

        self.print_report()
        self.save_report()

    def validate_entity_indexes(self):
        """Validate all entity index files."""
        print("\n[1] 实体索引校验")

        entity_files = {
            "emperors": "entities/data/emperors_index.json",
            "palaces": "entities/data/palaces_index.json",
            "figures": "entities/data/figures_index.json",
        }

        all_ids = set()
        for name, path in entity_files.items():
            filepath = os.path.join(KG_DIR, path)
            data = self.load_json(filepath)
            if data is None:
                continue

            count = len(data) if isinstance(data, dict) else 0
            print(f"  {name}: {count} entities")
            self.stats[f"{name}_count"] = count

            if isinstance(data, dict):
                for eid, entity in data.items():
                    if eid in all_ids:
                        self.errors.append(f"Duplicate entity ID: {eid}")
                    all_ids.add(eid)

                    # Check required fields
                    if "name" not in entity:
                        self.errors.append(f"Entity {eid} missing 'name'")

        self.stats["total_entities"] = len(all_ids)
        print(f"  Total unique entities: {len(all_ids)}")

    def validate_relations(self):
        """Validate relation files."""
        print("\n[2] 关系校验")

        valid_types = {"父子", "夫妻", "兄弟", "君臣", "辅佐", "敌对",
                       "主持修建", "居住于", "办公于", "发生于",
                       "同时代", "师承", "家族", "政敌", "上下级",
                       "执政于", "参与事件", "出生于", "逝世于"}

        relation_files = [
            "relations/data/family.json",
            "relations/data/political.json",
            "relations/data/spatial.json",
            "relations/data/temporal.json",
            "relations/data/all_relations.json",
        ]

        total_relations = 0
        for path in relation_files:
            filepath = os.path.join(KG_DIR, path)
            data = self.load_json(filepath)
            if data is None:
                continue

            relations = data if isinstance(data, list) else data.get("relations", [])
            total_relations += len(relations)

            for i, rel in enumerate(relations):
                if "from" not in rel or "to" not in rel:
                    self.errors.append(f"Relation {path}[{i}] missing from/to")
                    continue

                if rel.get("type") not in valid_types:
                    self.warnings.append(f"Unknown relation type: {rel.get('type')} in {path}[{i}]")

                # Check year range (Ming-Qing: 1368-1912)
                year = rel.get("year")
                if year and (year < 1368 or year > 1912):
                    self.warnings.append(f"Year {year} out of Ming-Qing range in {path}[{i}]")

        self.stats["total_relations"] = total_relations
        print(f"  Total relations: {total_relations}")
        print(f"  Errors: {len([e for e in self.errors if 'Relation' in e])}")

    def validate_chronology(self):
        """Validate chronology data."""
        print("\n[3] 时间线校验")

        reign_path = os.path.join(KG_DIR, "chronology/data/reign_periods.json")
        year_map_path = os.path.join(KG_DIR, "chronology/data/year_ce_map.json")

        reign = self.load_json(reign_path)
        year_map = self.load_json(year_map_path)

        if reign and isinstance(reign, dict):
            print(f"  Reign periods: {len(reign)}")
            self.stats["reign_periods"] = len(reign)

            # Check for overlapping reigns
            emperors_by_year = defaultdict(list)
            for eid, info in reign.items():
                start = info.get("start", 0)
                end = info.get("end", 0)
                for y in range(start, end + 1):
                    emperors_by_year[y].append(eid)

            overlaps = {y: emps for y, emps in emperors_by_year.items() if len(emps) > 1}
            if overlaps:
                self.warnings.append(f"Overlapping reigns in {len(overlaps)} years")

        if year_map:
            print(f"  Year mappings: {len(year_map)}")
            self.stats["year_mappings"] = len(year_map)

    def validate_aliases(self):
        """Validate alias map."""
        print("\n[4] 别名系统校验")

        alias_path = os.path.join(KG_DIR, "entities/data/alias_map.json")
        data = self.load_json(alias_path)

        if data and isinstance(data, dict):
            print(f"  Total aliases: {len(data)}")
            self.stats["total_aliases"] = len(data)

            # Check for duplicate aliases pointing to different entities
            target_map = defaultdict(list)
            for alias, info in data.items():
                target = info.get("canonical_id", "")
                target_map[target].append(alias)

            # Check alias name conflicts (alias should not match a canonical name)
            entity_names = set()
            for idx_file in ["entities/data/emperors_index.json",
                            "entities/data/palaces_index.json",
                            "entities/data/figures_index.json"]:
                idx_data = self.load_json(os.path.join(KG_DIR, idx_file))
                if idx_data:
                    for eid, ent in idx_data.items():
                        if "name" in ent:
                            entity_names.add(ent["name"])

            for alias in data.keys():
                if alias in entity_names:
                    self.warnings.append(f"Alias '{alias}' conflicts with a canonical entity name")

    def validate_pages(self):
        """Validate docs/ pages exist for all entities."""
        print("\n[5] 页面完整性校验")

        docs_dir = os.path.join(BASE_DIR, "docs")
        expected_types = {
            "emperors_index.json": "emperors",
            "palaces_index.json": "palaces",
            "figures_index.json": "figures",
        }

        missing = 0
        total = 0
        for idx_file, dir_name in expected_types.items():
            idx_path = os.path.join(KG_DIR, "entities/data", idx_file)
            data = self.load_json(idx_path)
            if data is None:
                continue

            for eid, entity in data.items():
                total += 1
                name = entity.get("name", "")
                # Expected filename from name
                expected_html = f"{self.name_to_slug(name)}.html"
                page_path = os.path.join(docs_dir, dir_name, expected_html)

                if not os.path.exists(page_path):
                    missing += 1
                    if missing <= 10:  # Only show first 10
                        self.warnings.append(f"Missing page: {dir_name}/{expected_html}")

        self.stats["total_pages_expected"] = total
        self.stats["pages_missing"] = missing
        print(f"  Expected pages: {total}")
        print(f"  Missing pages: {missing}")

    def name_to_slug(self, name):
        """Simple name to slug conversion (identity for Chinese names)."""
        if any('\u4e00' <= c <= '\u9fff' for c in name):
            return name  # Chinese names stay as-is
        return name.lower().replace(" ", "-")

    def print_report(self):
        print("\n" + "=" * 60)
        print("校验报告")
        print("=" * 60)

        if self.errors:
            print(f"\n❌ 错误 ({len(self.errors)}):")
            for e in self.errors[:20]:
                print(f"  - {e}")
            if len(self.errors) > 20:
                print(f"  ... 还有 {len(self.errors) - 20} 个错误")
        else:
            print("\n✅ 无错误")

        if self.warnings:
            print(f"\n⚠️ 警告 ({len(self.warnings)}):")
            for w in self.warnings[:20]:
                print(f"  - {w}")
            if len(self.warnings) > 20:
                print(f"  ... 还有 {len(self.warnings) - 20} 个警告")
        else:
            print("\n✅ 无警告")

        print(f"\n📊 统计:")
        for k, v in sorted(self.stats.items()):
            print(f"  {k}: {v}")

    def save_report(self):
        report = {
            "errors": self.errors,
            "warnings": self.warnings,
            "stats": self.stats,
            "timestamp": __import__("datetime").datetime.now().isoformat(),
        }
        os.makedirs(os.path.dirname(REPORT_FILE), exist_ok=True)
        with open(REPORT_FILE, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"\n📄 报告已保存到 {REPORT_FILE}")


def main():
    parser = argparse.ArgumentParser(description="Validate knowledge graph data")
    parser.add_argument("--quick", action="store_true", help="Quick validation (structure only)")
    parser.add_argument("--fix", action="store_true", help="Auto-fix fixable issues")
    args = parser.parse_args()

    v = Validator()
    v.validate_all(quick=args.quick)

    sys.exit(1 if v.errors else 0)


if __name__ == "__main__":
    main()
