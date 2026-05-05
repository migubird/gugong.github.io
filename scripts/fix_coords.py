#!/usr/bin/env python3
import json

# Read the JS file
with open('app/map/map-data.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Parse PALACES
start = content.index('const PALACES = ')
end = content.index('const EMPERORS = ')
palaces_str = content[start:end].replace('const PALACES = ', '').strip().rstrip(';')
palaces = json.loads(palaces_str)

# Flip y coordinates: newY = 800 - oldY
for pid, p in palaces.items():
    old_y = p['coordinates']['y']
    p['coordinates']['y'] = 800 - old_y

# Convert back to JS
new_palaces_js = 'const PALACES = ' + json.dumps(palaces, ensure_ascii=False, indent=2) + ';\n\n'

# Replace
new_content = content[:start] + new_palaces_js + content[end:]

with open('app/map/map-data.js', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Coordinates flipped:")
for pid, p in palaces.items():
    print(f"  {pid}: y={p['coordinates']['y']} ({p['name']})")
