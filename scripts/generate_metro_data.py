#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate metro_data.json from emperors.json and reign_periods.json"""
import json
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
KG_DIR = os.path.join(os.path.dirname(__file__), '..', 'kg', 'chronology', 'data')
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'app', 'metro', 'data')

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def main():
    emperors = load_json(os.path.join(DATA_DIR, 'emperors.json'))
    reign_periods = load_json(os.path.join(KG_DIR, 'reign_periods.json'))
    events = load_json(os.path.join(DATA_DIR, 'events.json'))

    # Sort emperors by dynasty then by reign_start
    ming_emperors = []
    qing_emperors = []
    for eid, emp in emperors.items():
        entry = {
            "id": eid,
            "name": emp.get("name", ""),
            "era_name": emp.get("era_name", ""),
            "reign_start": emp.get("reign_start", 0),
            "reign_end": emp.get("reign_end", 0),
            "description": emp.get("description", ""),
            "achievements": emp.get("achievements", [])
        }
        if emp.get("dynasty") == "明":
            ming_emperors.append(entry)
        elif emp.get("dynasty") == "清":
            qing_emperors.append(entry)

    ming_emperors.sort(key=lambda x: x["reign_start"])
    qing_emperors.sort(key=lambda x: x["reign_start"])

    # Gather key events that relate to emperors
    timeline_events = []
    for eid, evt in events.items():
        participants = evt.get("participants", [])
        emp_participants = [p for p in participants if p in emperors]
        if emp_participants:
            timeline_events.append({
                "id": eid,
                "name": evt.get("name", ""),
                "year": evt.get("start_year", 0),
                "category": evt.get("category", ""),
                "emperor_ids": emp_participants
            })
    timeline_events.sort(key=lambda x: x["year"])

    metro_data = {
        "ming_emperors": ming_emperors,
        "qing_emperors": qing_emperors,
        "timeline_events": timeline_events,
        "year_range": {
            "min": 1368,
            "max": 1912
        }
    }

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = os.path.join(OUTPUT_DIR, 'metro_data.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(metro_data, f, ensure_ascii=False, indent=2)

    print(f"Generated {output_path}")
    print(f"  Ming emperors: {len(ming_emperors)}")
    print(f"  Qing emperors: {len(qing_emperors)}")
    print(f"  Timeline events: {len(timeline_events)}")

if __name__ == '__main__':
    main()
