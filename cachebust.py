import re

with open(r'c:\REP-ANTIGRAVITY\js\properties.js', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('.webp"', '.webp?v=2"')

with open(r'c:\REP-ANTIGRAVITY\js\properties.js', 'w', encoding='utf-8') as f:
    f.write(content)
