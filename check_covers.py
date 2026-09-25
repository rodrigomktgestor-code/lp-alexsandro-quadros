import re

with open(r'c:\REP-ANTIGRAVITY\js\properties.js', encoding='utf-8') as f:
    content = f.read()

for m in re.finditer(r'slug:\s*"([^"]+)"[\s\S]*?coverImage:\s*"([^"]+)"', content):
    print(f'{m.group(1):30} -> {m.group(2)}')
