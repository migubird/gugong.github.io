#!/usr/bin/env python3
"""Generate wiki pages (HTML + Markdown) from JSON data for GitHub Pages."""

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

HTML_HEADER = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{title}} - 故宫知识图谱</title>
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{ font-family: "PingFang SC", "Microsoft YaHei", sans-serif; background: #0d1117; color: #e6edf3; min-height: 100vh; font-size: 16px; }}
    header {{ background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); padding: 1.5rem 2rem; border-bottom: 2px solid #c9a227; }}
    header a {{ color: #58a6ff; text-decoration: none; }}
    header a:hover {{ text-decoration: underline; }}
    .nav {{ display: flex; align-items: center; gap: 1rem; margin-bottom: 0.5rem; flex-wrap: wrap; }}
    h1 {{ color: #c9a227; font-size: 1.8rem; }}
    .container {{ max-width: 900px; margin: 2rem auto; padding: 0 1.5rem; }}
    .meta {{ display: grid; grid-template-columns: 100px 1fr; gap: 6px 12px; font-size: 15px; margin: 1rem 0; }}
    .meta-label {{ color: #8b949e; }}
    .meta-value {{ color: #e6edf3; }}
    .desc {{ font-size: 17px; line-height: 1.8; color: #ccc; margin: 1rem 0; }}
    h2 {{ color: #c9a227; font-size: 1.3rem; margin: 1.5rem 0 0.8rem; padding-bottom: 6px; border-bottom: 1px solid #30363d; }}
    ul {{ padding-left: 1.5rem; }}
    li {{ margin: 0.5rem 0; line-height: 1.6; font-size: 15px; }}
    strong {{ color: #e6edf3; }}
    .badge {{ display: inline-block; background: #c9a01733; color: #c9a017; padding: 2px 8px; border-radius: 4px; font-size: 13px; margin-right: 6px; }}
    .note {{ color: #8b949e; font-size: 14px; }}
    .event-card {{ background: #161b22; border: 1px solid #30363d; border-radius: 6px; padding: 12px; margin: 8px 0; }}
    .event-card .ename {{ color: #e74c3c; font-weight: bold; font-size: 16px; }}
    .event-card .edesc {{ color: #aaa; line-height: 1.5; }}
    .event-card .eyear {{ color: #8b949e; font-size: 13px; margin-top: 4px; }}
    .link-list a {{ color: #58a6ff; text-decoration: none; }}
    .link-list a:hover {{ text-decoration: underline; }}
    @media (max-width: 600px) {{
      h1 {{ font-size: 1.4rem; }}
      .container {{ padding: 0 1rem; }}
      .meta {{ grid-template-columns: 80px 1fr; font-size: 14px; }}
      .desc {{ font-size: 15px; }}
      li {{ font-size: 14px; }}
    }}
  </style>
</head>
<body>
<header>
  <div class="nav">
    <a href="../../">&#8592; 返回主页</a>
    <span><a href="../">宫殿</a> | <a href="../emperors/">皇帝</a></span>
  </div>
  <h1>{{title}}</h1>
</header>
<div class="container">
{{body}}
</div>
</body>
</html>
"""

def palace_html(title, palace, related_persons, related_events):
    metas = ""
    metas += '<div class="meta">'
    metas += '<span class="meta-label">类别</span><span class="meta-value">%s</span>' % palace["category"]
    metas += '<span class="meta-label">始建</span><span class="meta-value">%s年</span>' % palace["built_year"]
    metas += '<span class="meta-label">朝代</span><span class="meta-value">%s</span>' % palace["dynasty"]
    metas += '<span class="meta-label">地位</span><span class="meta-value">%s</span>' % palace.get("significance", "")
    if palace.get("dimensions", {}).get("width_m"):
        d = palace["dimensions"]
        metas += '<span class="meta-label">尺寸</span><span class="meta-value">%sm x %sm, 高%sm</span>' % (d["width_m"], d["depth_m"], d["height_m"])
    metas += '</div>'

    persons_html = ""
    if related_persons:
        persons_html += '<h2>相关人物</h2><ul>'
        for r in related_persons:
            p = r.get("_person", {})
            line = '<li><span class="badge">%s</span><strong>%s</strong>' % (r['type'], p.get('name', r.get('from', '')))
            if r.get("period"):
                line += ' <span class="note">（%s）</span>' % r["period"]
            if r.get("note"):
                line += ' <span class="note">— %s</span>' % r["note"]
            line += '</li>'
            persons_html += line
        persons_html += '</ul>'

    events_html = ""
    if related_events:
        events_html += '<h2>相关事件</h2>'
        for r in related_events:
            e = r.get("_event", {})
            events_html += '<div class="event-card">'
            events_html += '<div class="ename">%s</div>' % e.get('name', '')
            if e.get('description'):
                events_html += '<div class="edesc">%s</div>' % e['description']
            events_html += '<div class="eyear">%s年</div>' % e.get('start_year', '')
            events_html += '</div>'

    body = '<div class="desc">%s</div>' % palace["description"]
    body += metas
    body += persons_html
    body += events_html

    return HTML_HEADER.replace("{{title}}", title).replace("{{body}}", body)

def emperor_html(title, emperor, related_persons):
    metas = ""
    metas += '<div class="meta">'
    metas += '<span class="meta-label">年号</span><span class="meta-value">%s</span>' % emperor["era_name"]
    metas += '<span class="meta-label">朝代</span><span class="meta-value">%s</span>' % emperor["dynasty"]
    metas += '<span class="meta-label">在位</span><span class="meta-value">%s-%s年</span>' % (emperor["reign_start"], emperor["reign_end"])
    metas += '<span class="meta-label">生卒</span><span class="meta-value">%s-%s年</span>' % (emperor["birth_year"], emperor["death_year"])
    metas += '</div>'

    persons_html = ""
    if related_persons:
        persons_html += '<h2>相关人物</h2><ul>'
        for r in related_persons:
            p = r.get("_person", {})
            line = '<li><span class="badge">%s</span><strong>%s</strong>' % (r['type'], p.get('name', r.get('from', '')))
            if r.get("note"):
                line += ' <span class="note">— %s</span>' % r["note"]
            line += '</li>'
            persons_html += line
        persons_html += '</ul>'

    achievements = "、".join(emperor.get("achievements", []))
    body = '<div class="desc">%s</div>' % emperor["description"]
    body += metas
    body += '<h2>主要成就</h2><p class="desc">%s</p>' % achievements
    body += persons_html

    return HTML_HEADER.replace("{{title}}", title).replace("{{body}}", body)

def index_html(palaces, emperors, events, figures):
    today = datetime.now().strftime("%Y-%m-%d")
    body = '<div class="desc">用AI将故宫600年历史转化为可交互的空间-人物-事件知识图谱</div>'
    body += '<p style="color:#8b949e;margin:1rem 0;"><strong>数据规模</strong>：%d座宫殿、%d位皇帝、%d位人物、%d个事件 | <strong>最后更新</strong>：%s</p>' % (
        len(palaces), len(emperors), len(figures), len(events), today)

    body += '<h2>宫殿</h2><ul class="link-list">'
    for pid, palace in palaces.items():
        aliases = "（%s）" % "、".join(palace.get("aliases", [])) if palace.get("aliases") else ""
        body += '<li><a href="palaces/%s.html">%s</a>%s — %s，%s年建</li>' % (
            pid, palace['name'], aliases, palace['category'], palace['built_year'])
    body += '</ul>'

    body += '<h2>皇帝</h2><ul class="link-list">'
    for eid, emp in emperors.items():
        body += '<li><a href="emperors/%s.html">%s</a>（%s）— %s，%s-%s年在位</li>' % (
            eid, emp['name'], emp['era_name'], emp['dynasty'], emp['reign_start'], emp['reign_end'])
    body += '</ul>'

    body += '<h2>人物</h2><ul class="link-list">'
    for fid, fig in figures.items():
        bd = "%s-%s" % (fig.get('birth_year', '?'), fig.get('death_year', '?'))
        body += '<li><strong>%s</strong>（%s，%s）</li>' % (fig['name'], fig['category'], bd)
    body += '</ul>'

    body += '<h2>事件</h2><ul class="link-list">'
    for eid, evt in events.items():
        body += '<li><strong>%s</strong>（%s年）— %s</li>' % (evt['name'], evt.get('start_year', '?'), evt['category'])
    body += '</ul>'

    html = HTML_HEADER.replace("{{title}}", "故宫知识图谱 Wiki").replace("{{body}}", body)
    # Fix header nav for index
    html = html.replace('<span><a href="../">宫殿</a> | <a href="../emperors/">皇帝</a></span>',
                        '<span><a href="../app/map/">平面图</a></span>')
    return html

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
    os.makedirs(os.path.join(wiki_dir, 'palaces'), exist_ok=True)
    os.makedirs(os.path.join(wiki_dir, 'emperors'), exist_ok=True)

    # Generate palace pages
    for pid, palace in palaces.items():
        rel_p = [r for r in rels if r["to"] == pid and r["type"] in ["居住于", "执政于", "主持修建"]]
        rel_e = [r for r in rels if r["to"] == pid and r["type"] == "发生于"]
        # Enrich with full data
        for r in rel_p:
            r["_person"] = persons.get(r["from"], {})
        for r in rel_e:
            r["_event"] = events.get(r.get("event_id", ""), {})

        # Markdown
        content = ""
        content += "# %s\n\n" % palace["name"]
        if palace.get("aliases"):
            content += "又名：%s\n\n" % "、".join(palace["aliases"])
        content += "- **类别**：%s\n" % palace["category"]
        content += "- **始建**：%s年\n" % palace["built_year"]
        content += "- **朝代**：%s\n" % palace["dynasty"]
        content += "- **地位**：%s\n\n" % palace.get("significance", "")
        content += "## 简介\n\n%s\n\n" % palace["description"]
        if rel_p:
            content += "## 相关人物\n\n"
            for r in rel_p:
                p = persons.get(r["from"], {})
                content += "- **%s**（%s）%s" % (p.get('name', r['from']), p.get('category', ''), r['type'])
                if r.get("period"):
                    content += "（%s）" % r["period"]
                if r.get("note"):
                    content += "：%s" % r["note"]
                content += "\n"
            content += "\n"
        if rel_e:
            content += "## 相关事件\n\n"
            for r in rel_e:
                evt = events.get(r.get("event_id", ""), {})
                content += "- **%s**（%s年）：%s\n" % (evt.get('name',''), evt.get('start_year',''), evt.get('description',''))
            content += "\n"

        md_path = os.path.join(wiki_dir, 'palaces', "%s.md" % pid)
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(content)

        # HTML
        html_path = os.path.join(wiki_dir, 'palaces', "%s.html" % pid)
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(palace_html(palace["name"], palace, rel_p, rel_e))

        print("Generated: wiki/palaces/%s" % pid)

    # Generate emperor pages
    for eid, emp in emperors.items():
        rel_p = []
        for r in rels:
            if r["from"] == eid and r["type"] == "君臣":
                r2 = dict(r)
                r2["_person"] = figures.get(r["to"], {})
                rel_p.append(r2)
            elif r["to"] == eid and r["type"] == "辅佐":
                r2 = dict(r)
                r2["_person"] = figures.get(r["from"], {})
                rel_p.append(r2)

        # Markdown
        content = ""
        content += "# %s\n\n" % emp["name"]
        content += "- **年号**：%s\n" % emp["era_name"]
        content += "- **朝代**：%s\n" % emp["dynasty"]
        content += "- **在位**：%s-%s年\n" % (emp["reign_start"], emp["reign_end"])
        content += "- **生卒**：%s-%s年\n\n" % (emp["birth_year"], emp["death_year"])
        content += "## 简介\n\n%s\n\n" % emp["description"]
        content += "## 主要成就\n\n%s\n\n" % "、".join(emp.get("achievements", []))
        if rel_p:
            content += "## 相关人物\n\n"
            for r in rel_p:
                p = figures.get(r.get("to", r.get("from")), {})
                content += "- **%s**（%s）" % (p.get('name', ''), r['type'])
                if r.get("note"):
                    content += " — %s" % r["note"]
                content += "\n"
            content += "\n"

        md_path = os.path.join(wiki_dir, 'emperors', "%s.md" % eid)
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(content)

        html_path = os.path.join(wiki_dir, 'emperors', "%s.html" % eid)
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(emperor_html(emp["name"], emp, rel_p))

        print("Generated: wiki/emperors/%s" % eid)

    # Generate index
    md_index = ""
    md_index += "# 故宫知识图谱\n\n"
    md_index += "> 用AI将故宫600年历史转化为可交互的空间-人物-事件知识图谱\n\n"
    md_index += "**数据规模**：%d座宫殿、%d位皇帝、%d位人物、%d个事件\n" % (len(palaces), len(emperors), len(figures), len(events))
    md_index += "**最后更新**：%s\n\n" % datetime.now().strftime("%Y-%m-%d")
    md_index += "## 快速入口\n\n"
    md_index += "- [交互式故宫平面图](app/map/index.html)\n\n---\n\n"
    md_index += "## 宫殿\n\n"
    for pid, palace in palaces.items():
        aliases = "（%s）" % "、".join(palace.get("aliases", [])) if palace.get("aliases") else ""
        md_index += "- [%s](wiki/palaces/%s.html)%s — %s，%s年建\n" % (palace['name'], pid, aliases, palace['category'], palace['built_year'])
    md_index += "\n## 皇帝\n\n"
    for eid, emp in emperors.items():
        md_index += "- [%s](wiki/emperors/%s.html)（%s）— %s，%s-%s年在位\n" % (emp['name'], eid, emp['era_name'], emp['dynasty'], emp['reign_start'], emp['reign_end'])
    md_index += "\n## 人物\n\n"
    for fid, fig in figures.items():
        md_index += "- %s（%s，%s-%s）\n" % (fig['name'], fig['category'], fig.get('birth_year','?'), fig.get('death_year','?'))
    md_index += "\n## 事件\n\n"
    for eid, evt in events.items():
        md_index += "- %s（%s年）— %s\n" % (evt['name'], evt.get('start_year','?'), evt['category'])

    md_path = os.path.join(wiki_dir, 'index.md')
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(md_index)

    html_path = os.path.join(wiki_dir, 'index.html')
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(index_html(palaces, emperors, events, figures))

    print("Generated: wiki/index.html")
    print("\nDone! %d palaces, %d emperors, index." % (len(palaces), len(emperors)))

if __name__ == '__main__':
    main()
