#!/usr/bin/env python3
"""Generate complete Wiki pages (HTML) from JSON data for GitHub Pages.

Creates:
  docs/index.html        - Main wiki index with search
  docs/pages.json        - Registry for wikilink resolution
  docs/palaces/*.html    - 72 palace detail pages
  docs/emperors/*.html   - 26 emperor detail pages
  docs/figures/*.html    - 221 figure detail pages
  docs/events/*.html     - 82 event detail pages
  docs/css/wiki.css      - Syntax highlighting styles
"""

import json
import os
import re
from datetime import datetime
from collections import OrderedDict

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS_DIR = os.path.join(BASE_DIR, 'docs')

# ── CSS ──────────────────────────────────────────────────────────────────────

WIKI_CSS = """\
/* 故宫知识图谱 Wiki - Dark Chinese Imperial Theme */

:root {
  --bg-primary: #0d1117;
  --bg-secondary: #161b22;
  --bg-tertiary: #1c2333;
  --border: #30363d;
  --text-primary: #e6edf3;
  --text-secondary: #8b949e;
  --text-muted: #6e7681;
  --gold: #c9a227;
  --gold-dim: #c9a01733;
  --blue: #58a6ff;
  --link: #58a6ff;

  /* Entity type colors */
  --entity-person: #3498db;    /* 人名 */
  --entity-palace: #27ae60;    /* 建筑 */
  --entity-event: #c0392b;     /* 事件 */
  --entity-figure: #e67e22;    /* 人物/figures */
  --entity-time: #f39c12;      /* 时间 */
  --entity-title: #9b59b6;     /* 官职 */
}

* { margin: 0; padding: 0; box-sizing: border-box; }

body {
  font-family: "PingFang SC", "Microsoft YaHei", "Noto Sans SC", sans-serif;
  background: var(--bg-primary);
  color: var(--text-primary);
  min-height: 100vh;
  font-size: 16px;
  line-height: 1.6;
}

/* ── Header ─────────────────────────────────────────────────────── */

header {
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
  padding: 1.25rem 2rem;
  border-bottom: 2px solid var(--gold);
}

.header-top {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 0.5rem;
  flex-wrap: wrap;
}

.header-top a {
  color: var(--blue);
  text-decoration: none;
  font-size: 0.95rem;
}

.header-top a:hover { text-decoration: underline; }

header h1 {
  color: var(--gold);
  font-size: 1.8rem;
  font-weight: 700;
}

header h1 .entity-badge {
  font-size: 0.75rem;
  vertical-align: middle;
  padding: 2px 8px;
  border-radius: 4px;
  margin-left: 8px;
  font-weight: 400;
}

/* ── Container ──────────────────────────────────────────────────── */

.container {
  max-width: 960px;
  margin: 2rem auto;
  padding: 0 1.5rem;
}

/* ── Meta table ─────────────────────────────────────────────────── */

.meta {
  display: grid;
  grid-template-columns: 110px 1fr;
  gap: 8px 14px;
  font-size: 15px;
  margin: 1.25rem 0;
  background: var(--bg-secondary);
  padding: 14px 18px;
  border-radius: 8px;
  border: 1px solid var(--border);
}

.meta-label {
  color: var(--text-secondary);
  font-weight: 500;
}

.meta-value {
  color: var(--text-primary);
}

/* ── Description ────────────────────────────────────────────────── */

.desc {
  font-size: 17px;
  line-height: 1.85;
  color: #ccc;
  margin: 1.25rem 0;
}

/* ── Section headings ───────────────────────────────────────────── */

h2 {
  color: var(--gold);
  font-size: 1.3rem;
  margin: 1.75rem 0 0.75rem;
  padding-bottom: 6px;
  border-bottom: 1px solid var(--border);
}

h3 {
  color: var(--gold);
  font-size: 1.1rem;
  margin: 1.25rem 0 0.5rem;
}

/* ── Lists ──────────────────────────────────────────────────────── */

ul { padding-left: 1.5rem; }
li { margin: 0.4rem 0; line-height: 1.6; font-size: 15px; }
li a { color: var(--blue); text-decoration: none; }
li a:hover { text-decoration: underline; }

/* ── Badges ─────────────────────────────────────────────────────── */

.badge {
  display: inline-block;
  background: var(--gold-dim);
  color: var(--gold);
  padding: 2px 10px;
  border-radius: 4px;
  font-size: 13px;
  margin-right: 6px;
  white-space: nowrap;
}

.note {
  color: var(--text-secondary);
  font-size: 14px;
}

/* ── Event cards ────────────────────────────────────────────────── */

.event-card {
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 14px 16px;
  margin: 10px 0;
}

.event-card .ename {
  color: #e74c3c;
  font-weight: bold;
  font-size: 16px;
}

.event-card .edesc {
  color: #aaa;
  line-height: 1.5;
  margin-top: 4px;
}

.event-card .eyear {
  color: var(--text-secondary);
  font-size: 13px;
  margin-top: 4px;
}

.event-card .eoutcome {
  color: var(--gold);
  font-size: 14px;
  margin-top: 4px;
}

/* ── Entity mentions (syntax highlighting) ──────────────────────── */

.entity-person {
  color: var(--entity-person);
  font-weight: 500;
}

.entity-palace {
  color: var(--entity-palace);
  font-weight: 500;
}

.entity-event {
  color: var(--entity-event);
  font-weight: 500;
}

.entity-figure {
  color: var(--entity-figure);
  font-weight: 500;
}

.entity-time {
  color: var(--entity-time);
  font-weight: 500;
}

.entity-title {
  color: var(--entity-title);
  font-weight: 500;
}

/* ── Achievements list ──────────────────────────────────────────── */

.achievements {
  list-style: none;
  padding: 0;
}

.achievements li {
  padding: 4px 0;
  padding-left: 20px;
  position: relative;
}

.achievements li::before {
  content: "◆";
  color: var(--gold);
  position: absolute;
  left: 0;
  font-size: 12px;
}

/* ── Navigation ─────────────────────────────────────────────────── */

.nav-bottom {
  display: flex;
  justify-content: space-between;
  margin: 2rem 0;
  padding-top: 1rem;
  border-top: 1px solid var(--border);
}

.nav-bottom a {
  color: var(--blue);
  text-decoration: none;
  padding: 8px 16px;
  border: 1px solid var(--border);
  border-radius: 6px;
  font-size: 14px;
  transition: background 0.2s;
}

.nav-bottom a:hover {
  background: var(--bg-secondary);
  text-decoration: none;
}

/* ── Related entity list ────────────────────────────────────────── */

.related-link {
  display: inline-block;
  margin: 4px 6px 4px 0;
  padding: 4px 12px;
  border: 1px solid var(--border);
  border-radius: 4px;
  font-size: 14px;
  color: var(--blue);
  text-decoration: none;
  transition: all 0.2s;
}

.related-link:hover {
  background: var(--bg-tertiary);
  border-color: var(--gold);
  color: var(--gold);
  text-decoration: none;
}

.related-link.type-palace { border-color: #27ae6044; }
.related-link.type-palace:hover { border-color: #27ae60; color: #27ae60; }
.related-link.type-emperor { border-color: #e67e2244; }
.related-link.type-emperor:hover { border-color: #e67e22; color: #e67e22; }
.related-link.type-figure { border-color: #3498db44; }
.related-link.type-figure:hover { border-color: #3498db; color: #3498db; }
.related-link.type-event { border-color: #c0392b44; }
.related-link.type-event:hover { border-color: #c0392b; color: #c0392b; }

/* ── Index page ─────────────────────────────────────────────────── */

.search-box {
  margin: 1.5rem 0;
}

.search-input {
  width: 100%;
  max-width: 500px;
  padding: 12px 16px;
  font-size: 16px;
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: 8px;
  color: var(--text-primary);
  outline: none;
  transition: border-color 0.2s;
}

.search-input:focus {
  border-color: var(--gold);
}

.search-input::placeholder {
  color: var(--text-muted);
}

.search-results {
  margin-top: 1rem;
  max-height: 400px;
  overflow-y: auto;
}

.search-result-item {
  padding: 10px 14px;
  border: 1px solid var(--border);
  border-radius: 6px;
  margin: 6px 0;
  background: var(--bg-secondary);
}

.search-result-item a {
  color: var(--blue);
  text-decoration: none;
  font-weight: 500;
}

.search-result-item a:hover { text-decoration: underline; }

.search-result-item .result-type {
  font-size: 12px;
  color: var(--text-secondary);
  margin-left: 8px;
}

.stats-section {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 12px;
  margin: 1.5rem 0;
}

.stat-card {
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 16px;
  text-align: center;
}

.stat-card .stat-num {
  font-size: 2rem;
  font-weight: 700;
  color: var(--gold);
}

.stat-card .stat-label {
  font-size: 14px;
  color: var(--text-secondary);
  margin-top: 4px;
}

.app-links {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  margin: 1.5rem 0;
}

.app-link {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 10px 18px;
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: 8px;
  color: var(--text-primary);
  text-decoration: none;
  transition: all 0.2s;
}

.app-link:hover {
  border-color: var(--gold);
  color: var(--gold);
}

.category-nav {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  margin: 1.25rem 0;
}

.category-nav a {
  color: var(--gold);
  text-decoration: none;
  font-weight: 500;
  padding: 6px 14px;
  border: 1px solid var(--gold);
  border-radius: 6px;
  transition: all 0.2s;
}

.category-nav a:hover {
  background: var(--gold-dim);
}

.entity-list {
  list-style: none;
  padding: 0;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 6px 12px;
}

.entity-list li {
  padding: 4px 0;
}

.entity-list li a {
  color: var(--text-primary);
  text-decoration: none;
}

.entity-list li a:hover {
  color: var(--gold);
  text-decoration: underline;
}

.entity-list .entity-alias {
  color: var(--text-muted);
  font-size: 13px;
}

/* ── Responsive ─────────────────────────────────────────────────── */

@media (max-width: 600px) {
  header { padding: 1rem; }
  header h1 { font-size: 1.4rem; }
  .container { padding: 0 1rem; }
  .meta { grid-template-columns: 80px 1fr; font-size: 14px; }
  .desc { font-size: 15px; }
  li { font-size: 14px; }
  .stats-section { grid-template-columns: repeat(2, 1fr); }
  .entity-list { grid-template-columns: 1fr; }
}
"""

# ── HTML TEMPLATES ────────────────────────────────────────────────────────────

PAGE_HEADER = """\
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} - 故宫知识图谱 Wiki</title>
  <link rel="stylesheet" href="{rel_prefix}css/wiki.css">
</head>
<body>
<header>
  <div class="header-top">
    <a href="{rel_prefix}index.html">&#8592; 返回 Wiki 首页</a>
    <span>
      <a href="{rel_prefix}palaces/">宫殿</a> |
      <a href="{rel_prefix}emperors/">皇帝</a> |
      <a href="{rel_prefix}figures/">人物</a> |
      <a href="{rel_prefix}events/">事件</a>
    </span>
  </div>
  <h1>{title} <span class="entity-badge badge-{entity_type}">{entity_label}</span></h1>
</header>
<div class="container">
"""

PAGE_FOOTER = """\
</div>
</body>
</html>
"""

INDEX_HEADER = """\
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>故宫知识图谱 Wiki</title>
  <link rel="stylesheet" href="css/wiki.css">
</head>
<body>
<header>
  <div class="header-top">
    <span>
      <a href="../app/map/">平面图</a> |
      <a href="../app/metro/">时空地铁</a> |
      <a href="../app/explorer/">图谱探索</a>
    </span>
  </div>
  <h1>故宫知识图谱 Wiki</h1>
</header>
<div class="container">
"""

# ── GLOBALS ──────────────────────────────────────────────────────────────────
LOOKUP_NAME = {}  # name -> entity_id
LOOKUP_BY_ID = {}  # entity_id -> entity_dict


# ── DATA LOADING ──────────────────────────────────────────────────────────────

def load_json(filename):
    path = os.path.join(BASE_DIR, 'data', filename)
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_alias_map():
    path = os.path.join(BASE_DIR, 'kg', 'entities', 'data', 'alias_map.json')
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_relations():
    path = os.path.join(BASE_DIR, 'data', 'relations.json')
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)["relations"]


# ── ENTITY RESOLUTION ─────────────────────────────────────────────────────────

# Build lookup tables
def build_lookups(palaces, emperors, figures, events, alias_map):
    """Build lookup dicts: id->entity, name->id, type->id."""
    # ID lookups
    by_id = {}
    by_id.update(palaces)
    by_id.update(emperors)
    by_id.update(figures)
    by_id.update(events)

    # name -> canonical id (from data + alias_map)
    name_to_id = {}
    for eid, ent in palaces.items():
        name_to_id[ent['name']] = eid
    for eid, ent in emperors.items():
        name_to_id[ent['name']] = eid
    for fid, ent in figures.items():
        name_to_id[ent['name']] = fid
    for eid, ent in events.items():
        name_to_id[ent['name']] = eid

    # Merge alias_map
    for alias, info in alias_map.items():
        name_to_id[alias] = info['canonical_id']

    # type -> id
    type_to_id = {}
    for eid in palaces:
        type_to_id[eid] = 'palace'
    for eid in emperors:
        type_to_id[eid] = 'emperor'
    for fid in figures:
        type_to_id[fid] = 'figure'
    for eid in events:
        type_to_id[eid] = 'event'

    return by_id, name_to_id, type_to_id


# ── RELATION LOOKUP ───────────────────────────────────────────────────────────

def get_relations_for(entity_id, rels, by_id):
    """Get all relations where entity is from or to."""
    incoming = [r for r in rels if r.get('to') == entity_id]
    outgoing = [r for r in rels if r.get('from') == entity_id]
    return incoming, outgoing


def enrich_relation(rel, by_id):
    """Add _target or _source to relation with full entity data."""
    r = dict(rel)
    if r.get('to') and r['to'] in by_id:
        r['_target'] = by_id[r['to']]
        r['_target_type'] = get_entity_type(r['to'], by_id)
    if r.get('from') and r['from'] in by_id:
        r['_source'] = by_id[r['from']]
        r['_source_type'] = get_entity_type(r['from'], by_id)
    return r


def get_entity_type(entity_id, by_id):
    if entity_id in by_id:
        ent = by_id[entity_id]
        if 'era_name' in ent:
            return 'emperor'
        if 'category' in ent and 'built_year' in ent:
            return 'palace'
        if 'start_year' in ent:
            return 'event'
        return 'figure'
    return None


def get_url(entity_id, entity_type):
    """Get relative URL for an entity."""
    return "{type}s/{id}.html".format(type=entity_type, id=entity_id)


# ── WIKILINK RENDERING ───────────────────────────────────────────────────────

def render_wikilinks(text):
    """Replace [[wikilink]] syntax with clickable HTML links.
    Also highlights entity mentions in text with appropriate CSS classes.
    Uses global LOOKUP_NAME and LOOKUP_BY_ID."""
    global LOOKUP_NAME, LOOKUP_BY_ID
    # First handle explicit [[wikilink]] patterns
    def replace_wikilink(match):
        link_text = match.group(1)
        eid = LOOKUP_NAME.get(link_text)
        if eid and eid in LOOKUP_BY_ID:
            etype = get_entity_type(eid, LOOKUP_BY_ID)
            url = get_url(eid, etype)
            return '<a href="{url}" class="entity-{etype}">{text}</a>'.format(
                url=url, etype=etype, text=link_text)
        return link_text

    text = re.sub(r'\[\[([^\]]+)\]\]', replace_wikilink, text)

    # Also wrap known entity names in spans for color highlighting
    # Sort by length descending to match longer names first
    sorted_names = sorted(LOOKUP_NAME.keys(), key=len, reverse=True)
    for name in sorted_names:
        eid = LOOKUP_NAME[name]
        if isinstance(eid, dict):
            continue
        if eid not in LOOKUP_BY_ID:
            continue
        etype = get_entity_type(eid, LOOKUP_BY_ID)
        replacement = '<span class="entity-{etype}">{name}</span>'.format(etype=etype, name=name)
        # Simple string replace - safe since names don't contain HTML
        if name in text:
            text = text.replace(name, replacement)

    return text


# ── PAGE GENERATORS ──────────────────────────────────────────────────────────

ENTITY_TYPE_LABELS = {
    'palace': '宫殿',
    'emperor': '皇帝',
    'figure': '人物',
    'event': '事件',
}

def render_related_links(relations, by_id, entity_type, exclude_id=None):
    """Render related entity links as pills."""
    links = []
    seen = set()
    for r in relations:
        target_id = r.get('to') or r.get('from')
        if not target_id or target_id == exclude_id or target_id in seen:
            continue
        seen.add(target_id)
        ttype = get_entity_type(target_id, by_id)
        if ttype and target_id in by_id:
            ent = by_id[target_id]
            url = get_url(target_id, ttype)
            links.append(
                '<a href="{url}" class="related-link type-{ttype}">{name}</a>'.format(
                    url=url, ttype=ttype, name=ent.get('name', target_id)))
    return ' '.join(links) if links else '<span class="note">暂无</span>'


def generate_palace_page(pid, palace, rels, all_ids):
    """Generate a palace detail HTML page."""
    global LOOKUP_BY_ID
    by_id = LOOKUP_BY_ID
    incoming, outgoing = get_relations_for(pid, rels, by_id)

    # Meta info
    meta_items = [
        ('类别', palace.get('category', '')),
        ('始建', '%s年' % palace.get('built_year', '')),
        ('朝代', palace.get('dynasty', '')),
        ('地位', palace.get('significance', '')),
    ]
    if palace.get('rebuilt_years'):
        meta_items.append(('重修', ', '.join('%s年' % y for y in palace['rebuilt_years'])))
    if palace.get('dimensions', {}).get('width_m'):
        d = palace['dimensions']
        meta_items.append(('尺寸', '%sm × %sm, 高%sm' % (d['width_m'], d['depth_m'], d['height_m'])))
    if palace.get('aliases'):
        meta_items.append(('别名', ', '.join(palace['aliases'])))

    meta_html = '<div class="meta">'
    for label, value in meta_items:
        meta_html += '<span class="meta-label">%s</span><span class="meta-value">%s</span>' % (label, value)
    meta_html += '</div>'

    # Description with entity highlighting
    desc_html = '<div class="desc">%s</div>' % render_wikilinks(palace.get('description', ''))

    # Related people (incoming relations)
    related_people = []
    for r in incoming:
        rel_type = r.get('type', '')
        if rel_type in ('居住于', '执政于', '主持修建', '居住'):
            r2 = enrich_relation(r, by_id)
            related_people.append(r2)

    related_events = []
    for r in incoming:
        if r.get('type') == '发生于':
            r2 = enrich_relation(r, by_id)
            related_events.append(r2)

    people_html = ''
    if related_people:
        people_html = '<h2>相关人物</h2>'
        for r in related_people:
            src = r.get('_source', {})
            name = src.get('name', r.get('from', ''))
            eid = r.get('from', '')
            url = ''
            if eid in by_id:
                etype = get_entity_type(eid, by_id)
                url = get_url(eid, etype)
            line = '<span class="badge">%s</span>' % r.get('type', '')
            if url:
                line += '<a href="%s" class="entity-%s">%s</a>' % (url, get_entity_type(eid, by_id), name)
            else:
                line += '<strong>%s</strong>' % name
            if r.get('period'):
                line += ' <span class="note">（%s）</span>' % r['period']
            if r.get('note'):
                line += ' <span class="note">— %s</span>' % r['note']
            people_html += '<li>%s</li>' % line
        people_html = '<h2>相关人物</h2><ul>' + people_html + '</ul>'

    events_html = ''
    if related_events:
        events_html = '<h2>相关事件</h2>'
        for r in related_events:
            evt = r.get('_target', r.get('_source', {}))
            # For "发生于" relation, the target is the palace, source is the event
            if r.get('from') and r['from'] in by_id and get_entity_type(r['from'], by_id) == 'event':
                evt = by_id[r['from']]
                eid = r['from']
            elif r.get('to') and r['to'] in by_id and get_entity_type(r['to'], by_id) == 'event':
                evt = by_id[r['to']]
                eid = r['to']
            else:
                continue
            url = get_url(eid, 'event')
            events_html += '<div class="event-card">'
            events_html += '<a href="%s" class="ename">%s</a>' % (url, evt.get('name', ''))
            if evt.get('description'):
                events_html += '<div class="edesc">%s</div>' % render_wikilinks(evt['description'])
            events_html += '<div class="eyear">%s–%s年</div>' % (
                evt.get('start_year', '?'), evt.get('end_year', evt.get('start_year', '?')))
            if evt.get('outcome'):
                events_html += '<div class="eoutcome">结果：%s</div>' % evt['outcome']
            events_html += '</div>'

    # Navigation
    sorted_ids = sorted(all_ids['palaces'])
    idx = sorted_ids.index(pid) if pid in sorted_ids else 0
    nav_html = '<div class="nav-bottom">'
    if idx > 0:
        prev_id = sorted_ids[idx - 1]
        nav_html += '<a href="%s.html">&#8592; %s</a>' % (prev_id, by_id[prev_id]['name'])
    else:
        nav_html += '<span></span>'
    nav_html += '<a href="index.html">&#9650; 宫殿列表</a>'
    if idx < len(sorted_ids) - 1:
        next_id = sorted_ids[idx + 1]
        nav_html += '<a href="%s.html">%s &#8594;</a>' % (next_id, by_id[next_id]['name'])
    else:
        nav_html += '<span></span>'
    nav_html += '</div>'

    title = palace['name']
    body = desc_html + meta_html + people_html + events_html + nav_html

    return (PAGE_HEADER.format(
        title=title,
        entity_type='palace',
        entity_label='宫殿',
        rel_prefix=''
    ) + body + PAGE_FOOTER)


def generate_emperor_page(eid, emperor, rels, by_id, all_ids):
    """Generate an emperor detail HTML page."""
    incoming, outgoing = get_relations_for(eid, rels, by_id)

    meta_items = [
        ('年号', emperor.get('era_name', '')),
        ('朝代', emperor.get('dynasty', '')),
        ('在位', '%s–%s年' % (emperor.get('reign_start', ''), emperor.get('reign_end', ''))),
        ('生卒', '%s–%s年' % (emperor.get('birth_year', ''), emperor.get('death_year', ''))),
    ]
    if emperor.get('father') and emperor['father'] in by_id:
        meta_items.append(('父皇', '<a href="../emperors/%s.html">%s</a>' % (
            emperor['father'], by_id[emperor['father']]['name'])))
    if emperor.get('successor') and emperor['successor'] in by_id:
        meta_items.append(('继承者', '<a href="../emperors/%s.html">%s</a>' % (
            emperor['successor'], by_id[emperor['successor']]['name'])))

    meta_html = '<div class="meta">'
    for label, value in meta_items:
        meta_html += '<span class="meta-label">%s</span><span class="meta-value">%s</span>' % (label, value)
    meta_html += '</div>'

    desc_html = '<div class="desc">%s</div>' % render_wikilinks(emperor.get('description', ''))

    # Related officials (君臣 relations)
    officials = []
    for r in outgoing:
        if r.get('type') == '君臣':
            r2 = enrich_relation(r, by_id)
            officials.append(r2)
    for r in incoming:
        if r.get('type') == '辅佐':
            r2 = enrich_relation(r, by_id)
            officials.append(r2)

    # Related events
    events = []
    for r in outgoing:
        if r.get('type') == '参与事件':
            r2 = enrich_relation(r, by_id)
            events.append(r2)

    # Related palaces
    palaces = []
    for r in outgoing:
        if r.get('type') in ('执政于', '居住于'):
            r2 = enrich_relation(r, by_id)
            palaces.append(r2)

    officials_html = ''
    if officials:
        officials_html = '<h2>相关人物</h2><ul>'
        for r in officials:
            target = r.get('_target', r.get('_source', {}))
            tid = r.get('to') or r.get('from')
            name = target.get('name', tid)
            url = ''
            if tid in by_id:
                ttype = get_entity_type(tid, by_id)
                url = get_url(tid, ttype)
            line = '<span class="badge">%s</span>' % r.get('type', '')
            if url:
                line += '<a href="%s" class="entity-%s">%s</a>' % (url, get_entity_type(tid, by_id), name)
            else:
                line += '<strong>%s</strong>' % name
            if r.get('note'):
                line += ' <span class="note">— %s</span>' % r['note']
            officials_html += '<li>%s</li>' % line
        officials_html += '</ul>'

    events_html = ''
    if events:
        events_html = '<h2>参与事件</h2>'
        for r in events:
            teid = r.get('to')
            if teid and teid in by_id:
                evt = by_id[teid]
                url = get_url(teid, 'event')
                events_html += '<div class="event-card">'
                events_html += '<a href="%s" class="ename">%s</a>' % (url, evt.get('name', ''))
                if evt.get('description'):
                    events_html += '<div class="edesc">%s</div>' % render_wikilinks(evt['description'])
                events_html += '<div class="eyear">%s–%s年</div>' % (
                    evt.get('start_year', '?'), evt.get('end_year', evt.get('start_year', '?')))
                events_html += '</div>'

    palaces_html = ''
    if palaces:
        palaces_html = '<h2>相关宫殿</h2><div>'
        for r in palaces:
            teid = r.get('to')
            if teid and teid in by_id:
                pal = by_id[teid]
                url = get_url(teid, 'palace')
                palaces_html += '<a href="%s" class="related-link type-palace">%s</a>' % (url, pal.get('name', teid))
        palaces_html += '</div>'

    achievements = ''
    if emperor.get('achievements'):
        achievements = '<h2>主要成就</h2><ul class="achievements">'
        for a in emperor['achievements']:
            achievements += '<li>%s</li>' % render_wikilinks(a)
        achievements += '</ul>'

    # Navigation
    sorted_ids = sorted(all_ids['emperors'])
    idx = sorted_ids.index(eid) if eid in sorted_ids else 0
    nav_html = '<div class="nav-bottom">'
    if idx > 0:
        prev_id = sorted_ids[idx - 1]
        nav_html += '<a href="%s.html">&#8592; %s</a>' % (prev_id, by_id[prev_id]['name'])
    else:
        nav_html += '<span></span>'
    nav_html += '<a href="index.html">&#9650; 皇帝列表</a>'
    if idx < len(sorted_ids) - 1:
        next_id = sorted_ids[idx + 1]
        nav_html += '<a href="%s.html">%s &#8594;</a>' % (next_id, by_id[next_id]['name'])
    else:
        nav_html += '<span></span>'
    nav_html += '</div>'

    title = emperor['name']
    body = desc_html + meta_html + achievements + officials_html + events_html + palaces_html + nav_html

    return (PAGE_HEADER.format(
        title=title,
        entity_type='emperor',
        entity_label='皇帝',
        rel_prefix='../'
    ) + body + PAGE_FOOTER)


def generate_figure_page(fid, figure, rels, by_id, all_ids):
    """Generate a figure detail HTML page."""
    incoming, outgoing = get_relations_for(fid, rels, by_id)

    meta_items = [
        ('类别', figure.get('category', '')),
        ('朝代', figure.get('dynasty', '')),
    ]
    if figure.get('birth_year'):
        meta_items.append(('生卒', '%s–%s年' % (figure.get('birth_year', ''), figure.get('death_year', '?'))))
    elif figure.get('death_year'):
        meta_items.append(('卒年', '%s年' % figure['death_year']))

    served = figure.get('served_emperors', [])
    if served:
        emp_links = []
        for eid in served:
            if eid in by_id:
                emp_links.append('<a href="../emperors/%s.html" class="entity-emperor">%s</a>' % (
                    eid, by_id[eid].get('name', eid)))
            else:
                emp_links.append(eid)
        meta_items.append(('侍奉皇帝', '、'.join(emp_links)))

    if figure.get('consort_of') and figure['consort_of'] in by_id:
        meta_items.append(('配偶', '<a href="../emperors/%s.html">%s</a>' % (
            figure['consort_of'], by_id[figure['consort_of']]['name'])))

    meta_html = '<div class="meta">'
    for label, value in meta_items:
        meta_html += '<span class="meta-label">%s</span><span class="meta-value">%s</span>' % (label, value)
    meta_html += '</div>'

    desc_html = '<div class="desc">%s</div>' % render_wikilinks(figure.get('description', ''))

    # Related emperors
    emperor_links = []
    for r in outgoing:
        if r.get('type') == '君臣' and r.get('to') in by_id:
            ttype = get_entity_type(r['to'], by_id)
            if ttype == 'emperor':
                emperor_links.append(r)
    for r in incoming:
        if r.get('type') == '辅佐' and r.get('from') == fid and r.get('to') in by_id:
            ttype = get_entity_type(r['to'], by_id)
            if ttype == 'emperor':
                emperor_links.append(r)

    # Related figures (peers, rivals, etc.)
    peer_links = []
    for r in outgoing:
        if r.get('type') in ('政敌', '师徒', '亲属', '合作') and r.get('to') in by_id:
            peer_links.append(r)
    for r in incoming:
        if r.get('type') in ('政敌', '师徒', '亲属', '合作') and r.get('from') == fid and r.get('to') in by_id:
            peer_links.append(r)

    # Related events
    event_links = []
    for r in outgoing:
        if r.get('type') == '参与事件' and r.get('to') in by_id:
            event_links.append(r)

    related_html = ''
    if emperor_links:
        related_html += '<h2>相关皇帝</h2><div>'
        for r in emperor_links:
            teid = r.get('to')
            if teid in by_id:
                related_html += '<a href="../emperors/%s.html" class="related-link type-emperor">%s</a>' % (
                    teid, by_id[teid]['name'])
        related_html += '</div>'

    if peer_links:
        related_html += '<h2>相关人物</h2><ul>'
        for r in peer_links:
            teid = r.get('to')
            if teid in by_id:
                ent = by_id[teid]
                ttype = get_entity_type(teid, by_id)
                url = get_url(teid, ttype)
                line = '<span class="badge">%s</span>' % r.get('type', '')
                line += '<a href="%s" class="entity-%s">%s</a>' % (url, ttype, ent.get('name', teid))
                if r.get('note'):
                    line += ' <span class="note">— %s</span>' % r['note']
                related_html += '<li>%s</li>' % line
        related_html += '</ul>'

    if event_links:
        related_html += '<h2>参与事件</h2>'
        for r in event_links:
            teid = r.get('to')
            if teid in by_id:
                evt = by_id[teid]
                url = get_url(teid, 'event')
                related_html += '<div class="event-card">'
                related_html += '<a href="%s" class="ename">%s</a>' % (url, evt.get('name', ''))
                if evt.get('description'):
                    related_html += '<div class="edesc">%s</div>' % render_wikilinks(evt['description'])
                related_html += '<div class="eyear">%s–%s年</div>' % (
                    evt.get('start_year', '?'), evt.get('end_year', evt.get('start_year', '?')))
                related_html += '</div>'

    if figure.get('significance'):
        related_html += '<h2>历史意义</h2><div class="desc">%s</div>' % render_wikilinks(figure['significance'])

    # Navigation
    sorted_ids = sorted(all_ids['figures'])
    idx = sorted_ids.index(fid) if fid in sorted_ids else 0
    nav_html = '<div class="nav-bottom">'
    if idx > 0:
        prev_id = sorted_ids[idx - 1]
        nav_html += '<a href="%s.html">&#8592; %s</a>' % (prev_id, by_id[prev_id]['name'])
    else:
        nav_html += '<span></span>'
    nav_html += '<a href="index.html">&#9650; 人物列表</a>'
    if idx < len(sorted_ids) - 1:
        next_id = sorted_ids[idx + 1]
        nav_html += '<a href="%s.html">%s &#8594;</a>' % (next_id, by_id[next_id]['name'])
    else:
        nav_html += '<span></span>'
    nav_html += '</div>'

    title = figure['name']
    body = desc_html + meta_html + related_html + nav_html

    return (PAGE_HEADER.format(
        title=title,
        entity_type='figure',
        entity_label='人物',
        rel_prefix='../'
    ) + body + PAGE_FOOTER)


def generate_event_page(eid, event, rels, by_id, all_ids):
    """Generate an event detail HTML page."""
    incoming, outgoing = get_relations_for(eid, rels, by_id)

    meta_items = [
        ('类别', event.get('category', '')),
        ('时间', '%s–%s年' % (event.get('start_year', '?'), event.get('end_year', event.get('start_year', '?')))),
    ]
    if event.get('locations'):
        loc_links = []
        for lid in event['locations']:
            if lid in by_id:
                loc_links.append('<a href="../palaces/%s.html" class="entity-palace">%s</a>' % (
                    lid, by_id[lid]['name']))
            else:
                loc_links.append(lid)
        meta_items.append(('地点', '、'.join(loc_links)))

    meta_html = '<div class="meta">'
    for label, value in meta_items:
        meta_html += '<span class="meta-label">%s</span><span class="meta-value">%s</span>' % (label, value)
    meta_html += '</div>'

    desc_html = '<div class="desc">%s</div>' % render_wikilinks(event.get('description', ''))

    # Participants
    participants = event.get('participants', [])
    participants_html = ''
    if participants:
        participants_html = '<h2>参与者</h2><div>'
        for pid in participants:
            if pid in by_id:
                ent = by_id[pid]
                ttype = get_entity_type(pid, by_id)
                url = get_url(pid, ttype)
                participants_html += '<a href="%s" class="related-link type-%s">%s</a>' % (url, ttype, ent['name'])
            else:
                participants_html += '<span class="badge">%s</span>' % pid
        participants_html += '</div>'

    # Related palaces from locations
    locations_html = ''
    if event.get('locations'):
        locations_html = '<h2>相关宫殿</h2><div>'
        for lid in event['locations']:
            if lid in by_id:
                locations_html += '<a href="../palaces/%s.html" class="related-link type-palace">%s</a>' % (
                    lid, by_id[lid]['name'])
        locations_html += '</div>'

    outcome_html = ''
    if event.get('outcome'):
        outcome_html = '<h2>结果</h2><div class="desc">%s</div>' % render_wikilinks(event['outcome'])

    # Also find relations referencing this event
    rels_involving = [r for r in rels if r.get('to') == eid]
    extra_html = ''
    if rels_involving:
        extra_html = '<h2>关联</h2><ul>'
        for r in rels_involving:
            src_id = r.get('from')
            if src_id and src_id in by_id:
                ent = by_id[src_id]
                ttype = get_entity_type(src_id, by_id)
                url = get_url(src_id, ttype)
                extra_html += '<li><span class="badge">%s</span><a href="%s" class="entity-%s">%s</a>' % (
                    r.get('type', ''), url, ttype, ent['name'])
                if r.get('note'):
                    extra_html += ' <span class="note">— %s</span>' % r['note']
                extra_html += '</li>'
        extra_html += '</ul>'

    # Navigation
    sorted_ids = sorted(all_ids['events'])
    idx = sorted_ids.index(eid) if eid in sorted_ids else 0
    nav_html = '<div class="nav-bottom">'
    if idx > 0:
        prev_id = sorted_ids[idx - 1]
        nav_html += '<a href="%s.html">&#8592; %s</a>' % (prev_id, by_id[prev_id]['name'])
    else:
        nav_html += '<span></span>'
    nav_html += '<a href="index.html">&#9650; 事件列表</a>'
    if idx < len(sorted_ids) - 1:
        next_id = sorted_ids[idx + 1]
        nav_html += '<a href="%s.html">%s &#8594;</a>' % (next_id, by_id[next_id]['name'])
    else:
        nav_html += '<span></span>'
    nav_html += '</div>'

    title = event['name']
    body = desc_html + meta_html + participants_html + locations_html + outcome_html + extra_html + nav_html

    return (PAGE_HEADER.format(
        title=title,
        entity_type='event',
        entity_label='事件',
        rel_prefix='../'
    ) + body + PAGE_FOOTER)


# ── PAGES.JSON REGISTRY ──────────────────────────────────────────────────────

def build_pages_json(palaces, emperors, figures, events, alias_map):
    """Build pages.json with all names and aliases mapped to URLs."""
    pages = OrderedDict()

    # Palaces
    for pid, palace in palaces.items():
        url = "docs/palaces/%s.html" % pid
        pages[palace['name']] = {"url": url, "type": "palace"}
        for alias in palace.get('aliases', []):
            pages[alias] = {"url": url, "type": "palace"}

    # Emperors
    for eid, emp in emperors.items():
        url = "docs/emperors/%s.html" % eid
        pages[emp['name']] = {"url": url, "type": "emperor"}
        # Add era name as alias
        if emp.get('era_name'):
            pages[emp['era_name']] = {"url": url, "type": "emperor"}

    # Figures
    for fid, fig in figures.items():
        url = "docs/figures/%s.html" % fid
        pages[fig['name']] = {"url": url, "type": "figure"}

    # Events
    for eid, evt in events.items():
        url = "docs/events/%s.html" % eid
        pages[evt['name']] = {"url": url, "type": "event"}

    # Add alias_map entries
    for alias, info in alias_map.items():
        cid = info['canonical_id']
        atype = info['type']
        if atype == 'palace':
            url = "docs/palaces/%s.html" % cid
        elif atype == 'emperor':
            url = "docs/emperors/%s.html" % cid
        elif atype == 'figure':
            url = "docs/figures/%s.html" % cid
        elif atype == 'event':
            url = "docs/events/%s.html" % cid
        else:
            continue
        # Don't overwrite canonical name entries
        if alias not in pages:
            pages[alias] = {"url": url, "type": atype}

    return pages


# ── INDEX PAGE ───────────────────────────────────────────────────────────────

def generate_index(palaces, emperors, figures, events, pages_json):
    """Generate the main wiki index page."""
    total = len(palaces) + len(emperors) + len(figures) + len(events)

    # Stats section
    stats_html = """
<div class="stats-section">
  <div class="stat-card"><div class="stat-num">%d</div><div class="stat-label">宫殿</div></div>
  <div class="stat-card"><div class="stat-num">%d</div><div class="stat-label">皇帝</div></div>
  <div class="stat-card"><div class="stat-num">%d</div><div class="stat-label">人物</div></div>
  <div class="stat-card"><div class="stat-num">%d</div><div class="stat-label">事件</div></div>
  <div class="stat-card"><div class="stat-num">%d</div><div class="stat-label">词条总计</div></div>
</div>
""" % (len(palaces), len(emperors), len(figures), len(events), total)

    # App links
    app_links = """
<div class="app-links">
  <a href="../app/map/" class="app-link">🏯 故宫平面图</a>
  <a href="../app/metro/" class="app-link">🚇 时空地铁</a>
  <a href="../app/explorer/" class="app-link">🔍 图谱探索</a>
</div>
"""

    # Search box (JavaScript-based)
    search_html = """
<div class="search-box">
  <input type="text" id="searchInput" class="search-input" placeholder="搜索宫殿、皇帝、人物、事件..." autocomplete="off">
  <div id="searchResults" class="search-results"></div>
</div>
"""

    # Category nav
    cat_nav = """
<div class="category-nav">
  <a href="palaces/">宫殿 (%d)</a>
  <a href="emperors/">皇帝 (%d)</a>
  <a href="figures/">人物 (%d)</a>
  <a href="events/">事件 (%d)</a>
</div>
""" % (len(palaces), len(emperors), len(figures), len(events))

    # Description
    desc = '<div class="desc">用AI将故宫600年历史转化为可交互的空间-人物-事件知识图谱。浏览下方词条或使用搜索功能探索故宫历史。</div>'

    # Entity lists (grouped by type)
    def entity_list_html(entities, entity_type, rel_prefix):
        sorted_items = sorted(entities.values(), key=lambda x: x.get('name', ''))
        html = '<ul class="entity-list">'
        for ent in sorted_items:
            eid = ent['id']
            url = '%s%s/%s.html' % (rel_prefix, entity_type, eid)
            aliases = ''
            if ent.get('aliases'):
                aliases = ' <span class="entity-alias">（%s）</span>' % '、'.join(ent['aliases'][:3])
            html += '<li><a href="%s">%s</a>%s</li>' % (url, ent['name'], aliases)
        html += '</ul>'
        return html

    def event_list_html(events):
        sorted_items = sorted(events.values(), key=lambda x: x.get('name', ''))
        html = '<ul class="entity-list">'
        for ent in sorted_items:
            eid = ent['id']
            url = 'events/%s.html' % eid
            html += '<li><a href="%s">%s</a> <span class="entity-alias">（%s年）</span></li>' % (
                url, ent['name'], ent.get('start_year', '?'))
        html += '</ul>'
        return html

    palaces_html = '<h2>宫殿</h2>' + entity_list_html(palaces, 'palaces', '')
    emperors_html = '<h2>皇帝</h2>' + entity_list_html(emperors, 'emperors', '')
    figures_html = '<h2>人物</h2>' + entity_list_html(figures, 'figures', '')
    events_html = '<h2>事件</h2>' + event_list_html(events)

    body = (desc + stats_html + app_links + search_html + cat_nav +
            palaces_html + emperors_html + figures_html + events_html)

    # Search JavaScript
    search_js = """
<script>
(function() {
  var pages = %s;
  var searchInput = document.getElementById('searchInput');
  var searchResults = document.getElementById('searchResults');

  var cache = {};

  function escapeHtml(str) {
    return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }

  function highlightMatch(text, query) {
    var idx = text.toLowerCase().indexOf(query.toLowerCase());
    if (idx === -1) return escapeHtml(text);
    var before = text.substring(0, idx);
    var match = text.substring(idx, idx + query.length);
    var after = text.substring(idx + query.length);
    return escapeHtml(before) + '<strong style="color:#c9a227">' + escapeHtml(match) + '</strong>' + escapeHtml(after);
  }

  searchInput.addEventListener('input', function() {
    var query = this.value.trim();
    searchResults.innerHTML = '';
    if (query.length < 1) return;

    var results = [];
    for (var name in pages) {
      if (name.toLowerCase().indexOf(query.toLowerCase()) !== -1) {
        results.push({name: name, info: pages[name]});
      }
    }

    // Sort: exact match first, then by name length
    results.sort(function(a, b) {
      if (a.name === query) return -1;
      if (b.name === query) return 1;
      return a.name.length - b.name.length;
    });

    results = results.slice(0, 50);

    results.forEach(function(r) {
      var div = document.createElement('div');
      div.className = 'search-result-item';
      var typeLabel = {palace:'宫殿',emperor:'皇帝',figure:'人物',event:'事件'}[r.info.type] || r.info.type;
      div.innerHTML = '<a href="' + r.info.url.replace(/^docs\\//, '') + '">' +
        highlightMatch(r.name, query) + '</a>' +
        '<span class="result-type">' + typeLabel + '</span>';
      searchResults.appendChild(div);
    });
  });

  searchInput.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
      this.value = '';
      searchResults.innerHTML = '';
    }
  });
})();
</script>
""" % json.dumps(pages_json, ensure_ascii=False, indent=2)

    return (INDEX_HEADER + body + '</div>' + search_js + '</body>\n</html>')


# ── MAIN ─────────────────────────────────────────────────────────────────────

def main():
    print("Loading data...")
    palaces = load_json('palaces.json')
    emperors = load_json('emperors.json')
    figures = load_json('figures.json')
    events = load_json('events.json')
    rels = load_relations()
    alias_map = load_alias_map()

    print("Building lookups...")
    by_id, name_to_id, type_to_id = build_lookups(palaces, emperors, figures, events, alias_map)

    # Set globals for render_wikilinks
    global LOOKUP_NAME, LOOKUP_BY_ID
    LOOKUP_NAME = name_to_id
    LOOKUP_BY_ID = by_id

    all_ids = {
        'palaces': sorted(palaces.keys()),
        'emperors': sorted(emperors.keys()),
        'figures': sorted(figures.keys()),
        'events': sorted(events.keys()),
    }

    # Create directory structure
    print("Creating directory structure...")
    for subdir in ['palaces', 'emperors', 'figures', 'events', 'css']:
        os.makedirs(os.path.join(DOCS_DIR, subdir), exist_ok=True)

    # Generate pages.json
    print("Generating pages.json...")
    pages_json = build_pages_json(palaces, emperors, figures, events, alias_map)
    with open(os.path.join(DOCS_DIR, 'pages.json'), 'w', encoding='utf-8') as f:
        json.dump(pages_json, f, ensure_ascii=False, indent=2)
    print("  -> %d entries in pages.json" % len(pages_json))

    # Generate wiki.css
    print("Generating wiki.css...")
    with open(os.path.join(DOCS_DIR, 'css', 'wiki.css'), 'w', encoding='utf-8') as f:
        f.write(WIKI_CSS)

    # Generate palace pages
    print("Generating palace pages...")
    for pid in all_ids['palaces']:
        html = generate_palace_page(pid, palaces[pid], rels, all_ids)
        with open(os.path.join(DOCS_DIR, 'palaces', '%s.html' % pid), 'w', encoding='utf-8') as f:
            f.write(html)
    print("  -> %d palace pages" % len(palaces))

    # Generate emperor pages
    print("Generating emperor pages...")
    for eid in all_ids['emperors']:
        html = generate_emperor_page(eid, emperors[eid], rels, by_id, all_ids)
        with open(os.path.join(DOCS_DIR, 'emperors', '%s.html' % eid), 'w', encoding='utf-8') as f:
            f.write(html)
    print("  -> %d emperor pages" % len(emperors))

    # Generate figure pages
    print("Generating figure pages...")
    for fid in all_ids['figures']:
        html = generate_figure_page(fid, figures[fid], rels, by_id, all_ids)
        with open(os.path.join(DOCS_DIR, 'figures', '%s.html' % fid), 'w', encoding='utf-8') as f:
            f.write(html)
    print("  -> %d figure pages" % len(figures))

    # Generate event pages
    print("Generating event pages...")
    for eid in all_ids['events']:
        html = generate_event_page(eid, events[eid], rels, by_id, all_ids)
        with open(os.path.join(DOCS_DIR, 'events', '%s.html' % eid), 'w', encoding='utf-8') as f:
            f.write(html)
    print("  -> %d event pages" % len(events))

    # Generate index
    print("Generating index.html...")
    index_html = generate_index(palaces, emperors, figures, events, pages_json)
    with open(os.path.join(DOCS_DIR, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(index_html)

    total = len(palaces) + len(emperors) + len(figures) + len(events) + 2  # + index + pages.json
    print("\nDone! Generated %d files total:" % (total + 1))  # +1 for css
    print("  docs/index.html")
    print("  docs/pages.json")
    print("  docs/css/wiki.css")
    print("  docs/palaces/ (%d pages)" % len(palaces))
    print("  docs/emperors/ (%d pages)" % len(emperors))
    print("  docs/figures/ (%d pages)" % len(figures))
    print("  docs/events/ (%d pages)" % len(events))
    print("\nTotal: %d entity pages + index + registry + CSS" % (len(palaces) + len(emperors) + len(figures) + len(events)))


if __name__ == '__main__':
    main()
