#!/usr/bin/env python3
"""Generate wiki pages from JSON data for GitHub Pages deployment."""

import json
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load_json(filename):
    path = os.path.join(BASE_DIR, 'data', filename)
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_relations():
    path = os.path.join(BASE_DIR, 'data', 'relations.json')
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)["relations"]

def generate_palace_page(palace_id, palace, rels, persons, events):
    name = palace["name"]
    aliases = "、".join(palace.get("aliases", []))

    dims_text = ""
    if palace.get("dimensions", {}).get("width_m"):
        dims = palace["dimensions"]
        dims_text = "## 建筑尺寸\n\n- 面阔：%s米\n- 进深：%s米\n- 高度：%s米\n" % (
            dims["width_m"], dims["depth_m"], dims["height_m"])

    alias_text = "又名：" + aliases if aliases else ""

    related_persons = [r for r in rels if r["to"] == palace_id and r["type"] in ["居住于", "执政于", "主持修建"]]
    related_events = [r for r in rels if r["to"] == palace_id and r["type"] == "发生于"]

    lines = []
    lines.append("---")
    lines.append('title: "%s"' % name)
    lines.append("layout: default")
    lines.append("---")
    lines.append("")
    lines.append("# " + name)
    lines.append("")
    lines.append(alias_text)
    lines.append("")
    lines.append("- **类别**：%s" % palace["category"])
    lines.append("- **始建**：%s年" % palace["built_year"])
    lines.append("- **朝代**：%s" % palace["dynasty"])
    lines.append("- **历史地位**：%s" % palace.get("significance", ""))
    lines.append("")
    lines.append("## 简介")
    lines.append("")
    lines.append(palace["description"])
    lines.append("")
    lines.append(dims_text)
    lines.append("## 相关人物")
    lines.append("")

    for r in related_persons:
        person = persons.get(r["from"])
        if person:
            line = "- **%s**（%s）%s" % (person['name'], person.get('category', ''), r['type'])
            if r.get("period"):
                line += "（%s）" % r["period"]
            if r.get("note"):
                line += "：%s" % r["note"]
            lines.append(line)

    lines.append("")
    lines.append("## 相关事件")
    lines.append("")
    for r in related_events:
        evt = events.get(r["to"]) or events.get(r["from"])
        if evt:
            lines.append("- **%s**（%s年）：%s" % (
                evt['name'], evt.get('start_year', ''), evt.get('description', '')))

    return "\n".join(lines)

def generate_emperor_page(emperor_id, emperor, rels, figures):
    name = emperor["name"]
    achievements = "、".join(emperor.get("achievements", []))

    lines = []
    lines.append("---")
    lines.append('title: "%s"' % name)
    lines.append("layout: default")
    lines.append("---")
    lines.append("")
    lines.append("# " + name)
    lines.append("")
    lines.append("- **年号**：%s" % emperor["era_name"])
    lines.append("- **朝代**：%s" % emperor["dynasty"])
    lines.append("- **在位**：%s-%s年" % (emperor["reign_start"], emperor["reign_end"]))
    lines.append("- **生卒**：%s-%s年" % (emperor["birth_year"], emperor["death_year"]))
    lines.append("")
    lines.append("## 简介")
    lines.append("")
    lines.append(emperor["description"])
    lines.append("")
    lines.append("## 主要成就")
    lines.append("")
    lines.append(achievements)
    lines.append("")
    lines.append("## 相关人物")
    lines.append("")

    for r in rels:
        if r["from"] == emperor_id and r["type"] == "君臣":
            person = figures.get(r["to"])
            if person:
                note = r.get("note", "")
                lines.append("- **%s**（君臣）%s" % (person['name'], note))
        elif r["to"] == emperor_id and r["type"] == "辅佐":
            person = figures.get(r["from"])
            if person:
                note = r.get("note", "")
                lines.append("- **%s**（辅佐）%s" % (person['name'], note))
        elif r["to"] == emperor_id and r["type"] == "父子":
            if r["from"] in figures:
                lines.append("- **%s**（父子）" % figures[r['from']]['name'])

    return "\n".join(lines)

def generate_index(palaces, emperors, events, figures):
    today = datetime.now().strftime("%Y-%m-%d")
    lines = []
    lines.append("---")
    lines.append('title: "故宫知识图谱"')
    lines.append("---")
    lines.append("")
    lines.append("# 故宫知识图谱")
    lines.append("")
    lines.append("> 用AI将故宫600年历史转化为可交互的空间-人物-事件知识图谱")
    lines.append("")
    lines.append("**数据规模**：%d座宫殿、%d位皇帝、%d位人物、%d个事件" % (
        len(palaces), len(emperors), len(figures), len(events)))
    lines.append("**最后更新**：%s" % today)
    lines.append("")
    lines.append("## 快速入口")
    lines.append("")
    lines.append("- [交互式故宫平面图](app/map/index.html) - 点击宫殿查看关联人物和事件")
    lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## 宫殿")
    lines.append("")
    for pid, palace in palaces.items():
        aliases = "（%s）" % "、".join(palace.get("aliases", [])) if palace.get("aliases") else ""
        lines.append("- %s%s - %s，%s年建" % (
            palace['name'], aliases, palace['category'], palace['built_year']))

    lines.append("")
    lines.append("## 皇帝")
    lines.append("")
    for eid, emp in emperors.items():
        lines.append("- %s（%s） - %s，%s-%s年在位" % (
            emp['name'], emp['era_name'], emp['dynasty'], emp['reign_start'], emp['reign_end']))

    lines.append("")
    lines.append("## 人物")
    lines.append("")
    for fid, fig in figures.items():
        bd = "%s-%s" % (fig.get('birth_year', '?'), fig.get('death_year', '?'))
        lines.append("- %s（%s，%s）" % (fig['name'], fig['category'], bd))

    lines.append("")
    lines.append("## 事件")
    lines.append("")
    for eid, evt in events.items():
        lines.append("- %s（%s年）- %s" % (
            evt['name'], evt.get('start_year', '?'), evt['category']))

    return "\n".join(lines)

def main():
    palaces = load_json('palaces.json')
    emperors = load_json('emperors.json')
    figures = load_json('figures.json')
    events = load_json('events.json')
    rels = load_relations()

    persons = {}
    persons.update(emperors)
    persons.update(figures)

    wiki_dir = os.path.join(BASE_DIR, 'wiki')

    palace_dir = os.path.join(wiki_dir, 'palaces')
    os.makedirs(palace_dir, exist_ok=True)
    for pid, palace in palaces.items():
        content = generate_palace_page(pid, palace, rels, persons, events)
        path = os.path.join(palace_dir, "%s.md" % pid)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("Generated: wiki/palaces/%s.md" % pid)

    emperor_dir = os.path.join(wiki_dir, 'emperors')
    os.makedirs(emperor_dir, exist_ok=True)
    for eid, emp in emperors.items():
        content = generate_emperor_page(eid, emp, rels, figures)
        path = os.path.join(emperor_dir, "%s.md" % eid)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("Generated: wiki/emperors/%s.md" % eid)

    index_content = generate_index(palaces, emperors, events, figures)
    index_path = os.path.join(wiki_dir, 'index.md')
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(index_content)
    print("Generated: wiki/index.md")

    print("\nDone! Generated %d palace pages, %d emperor pages, 1 index page." % (
        len(palaces), len(emperors)))

if __name__ == '__main__':
    main()
