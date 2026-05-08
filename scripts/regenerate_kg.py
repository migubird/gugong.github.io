#!/usr/bin/env python3
"""Regenerate kg/ infrastructure from expanded data."""
import json, os

DATA = '/home/admin/gugong/data'
KG = '/home/admin/gugong/kg'

# Load all data
palaces = json.load(open(f'{DATA}/palaces.json'))
emperors = json.load(open(f'{DATA}/emperors.json'))
figures = json.load(open(f'{DATA}/figures.json'))
events = json.load(open(f'{DATA}/events.json'))
rels_data = json.load(open(f'{DATA}/relations.json'))
relations = rels_data['relations']

# --- kg/entities/data/ ---
os.makedirs(f'{KG}/entities/data', exist_ok=True)

# palaces_index.json (already exists but regenerate)
json.dump(palaces, open(f'{KG}/entities/data/palaces_index.json','w'), indent=2, ensure_ascii=False)

# emperors_index.json
json.dump(emperors, open(f'{KG}/entities/data/emperors_index.json','w'), indent=2, ensure_ascii=False)

# figures_index.json
json.dump(figures, open(f'{KG}/entities/data/figures_index.json','w'), indent=2, ensure_ascii=False)

# alias_map.json
alias_map = {}
for pid, p in palaces.items():
    aliases = p.get('aliases', [])
    for a in aliases:
        alias_map[a] = {'canonical_id': pid, 'type': 'palace'}
    alias_map[p['name']] = {'canonical_id': pid, 'type': 'palace'}

for eid, e in emperors.items():
    era = e.get('era_name','')
    name = e.get('name','')
    if era:
        alias_map[era] = {'canonical_id': eid, 'type': 'emperor'}
    if name:
        alias_map[name] = {'canonical_id': eid, 'type': 'emperor'}

for fid, f in figures.items():
    name = f.get('name','')
    if name:
        alias_map[name] = {'canonical_id': fid, 'type': 'figure'}

for ev_id, ev in events.items():
    name = ev.get('name','')
    if name:
        alias_map[name] = {'canonical_id': ev_id, 'type': 'event'}

json.dump(alias_map, open(f'{KG}/entities/data/alias_map.json','w'), indent=2, ensure_ascii=False)
print(f'alias_map: {len(alias_map)} entries')

# person_categories.json
cats = {}
for fid, f in figures.items():
    cat = f.get('category', '其他')
    cats.setdefault(cat, []).append(fid)
json.dump(cats, open(f'{KG}/entities/data/person_categories.json','w'), indent=2, ensure_ascii=False)
print(f'person_categories: {len(cats)} categories')

# place_categories.json
place_cats = {}
for pid, p in palaces.items():
    zone = p.get('category', '其他')
    place_cats.setdefault(zone, []).append(pid)
json.dump(place_cats, open(f'{KG}/entities/data/place_categories.json','w'), indent=2, ensure_ascii=False)
print(f'place_categories: {len(place_cats)} categories')

# --- kg/events/data/ ---
os.makedirs(f'{KG}/events/data', exist_ok=True)

all_events_list = []
for eid, ev in events.items():
    all_events_list.append(ev)
json.dump(all_events_list, open(f'{KG}/events/data/all_events.json','w'), indent=2, ensure_ascii=False)
print(f'all_events: {len(all_events_list)} events')

# event_relations - events that share participants or locations
event_rels = []
event_ids = list(events.keys())
for i in range(len(event_ids)):
    for j in range(i+1, len(event_ids)):
        e1 = events[event_ids[i]]
        e2 = events[event_ids[j]]
        p1 = set(e1.get('participants',[]))
        p2 = set(e2.get('participants',[]))
        shared = p1 & p2
        if shared:
            event_rels.append({'from': e1['id'], 'to': e2['id'], 'type': '共享参与者', 'shared': list(shared)})
json.dump(event_rels, open(f'{KG}/events/data/event_relations.json','w'), indent=2, ensure_ascii=False)
print(f'event_relations: {len(event_rels)}')

# --- kg/relations/data/ ---
os.makedirs(f'{KG}/relations/data', exist_ok=True)

# Split relations by type
family_types = {'父子', '夫妻', '兄弟', '家族'}
political_types = {'君臣', '辅佐', '敌对', '政敌'}
spatial_types = {'居住于', '主持修建', '发生于'}

all_rels = []
family = []
political = []
spatial = []
temporal = []

for r in relations:
    rtype = r.get('type', '')
    all_rels.append(r)
    if rtype in family_types:
        family.append(r)
    elif rtype in political_types:
        political.append(r)
    elif rtype in spatial_types:
        spatial.append(r)
    else:
        temporal.append(r)

# Add auto-generated 君臣 relations from figures who served emperors
existing_meridian = set()
for r in relations:
    if r['type'] == '君臣':
        existing_meridian.add((r['from'], r['to']))

for fid, f in figures.items():
    served = f.get('served_emperors', [])
    for eid in served:
        if eid in emperors and (eid, fid) not in existing_meridian:
            rel = {'from': eid, 'to': fid, 'type': '君臣', 'period': f.get('dynasty',''), 'note': f'{f["name"]}服务于{emperors[eid].get("era_name","")}帝'}
            all_rels.append(rel)
            political.append(rel)

# Add 居住于 relations for emperors who lived in palaces
emperor_palaces = {
    'yongzheng': [('yangxin-dian', '自雍正起以此为寝宫')],
    'qianlong': [('ning-shou-gong', '退位后居宁寿宫'), ('huang-ji-dian', '禅位后受朝贺')],
    'kangxi': [('qianqing-gong', '日常起居')],
    'yongle': [('qianqing-gong', '迁都后居住')],
}
for eid, pal_list in emperor_palaces.items():
    for pid, note in pal_list:
        if pid in palaces and eid in emperors:
            rel = {'from': eid, 'to': pid, 'type': '居住于', 'period': emperors[eid].get('era_name',''), 'note': note}
            all_rels.append(rel)
            spatial.append(rel)

# Add 发生于 relations for events at palace locations
for eid, ev in events.items():
    for loc in ev.get('locations', []):
        if loc in palaces:
            rel = {'from': eid, 'to': loc, 'type': '发生于', 'period': f'{ev.get("start_year","")}', 'note': ev.get('name','')}
            all_rels.append(rel)
            spatial.append(rel)

json.dump(all_rels, open(f'{KG}/relations/data/all_relations.json','w'), indent=2, ensure_ascii=False)
json.dump(family, open(f'{KG}/relations/data/family.json','w'), indent=2, ensure_ascii=False)
json.dump(political, open(f'{KG}/relations/data/political.json','w'), indent=2, ensure_ascii=False)
json.dump(spatial, open(f'{KG}/relations/data/spatial.json','w'), indent=2, ensure_ascii=False)
json.dump(temporal, open(f'{KG}/relations/data/temporal.json','w'), indent=2, ensure_ascii=False)
print(f'Total relations: {len(all_rels)} (family:{len(family)}, political:{len(political)}, spatial:{len(spatial)}, temporal:{len(temporal)})')

# --- kg/chronology/data/ ---
os.makedirs(f'{KG}/chronology/data', exist_ok=True)

# year_ce_map.json
year_map = {}
for eid, e in emperors.items():
    era = e.get('era_name', '')
    if era:
        year_map[era] = {
            'start': e.get('reign_start', 0),
            'end': e.get('reign_end', 0),
            'emperor': eid
        }
json.dump(year_map, open(f'{KG}/chronology/data/year_ce_map.json','w'), indent=2, ensure_ascii=False)
print(f'year_ce_map: {len(year_map)} eras')

# reign_periods.json
reign = {}
for eid, e in emperors.items():
    reign[eid] = {
        'name': e.get('name', ''),
        'era_name': e.get('era_name', ''),
        'reign_start': e.get('reign_start', 0),
        'reign_end': e.get('reign_end', 0),
        'dynasty': e.get('dynasty', '')
    }
json.dump(reign, open(f'{KG}/chronology/data/reign_periods.json','w'), indent=2, ensure_ascii=False)

# Also update data/relations.json
json.dump({'relations': all_rels}, open(f'{DATA}/relations.json','w'), indent=2, ensure_ascii=False)
print(f'Updated data/relations.json: {len(all_rels)} relations')

print('\n=== kg/ infrastructure regenerated ===')
print(f'Palaces: {len(palaces)}')
print(f'Emperors: {len(emperors)}')
print(f'Figures: {len(figures)}')
print(f'Events: {len(events)}')
print(f'Relations: {len(all_rels)}')
