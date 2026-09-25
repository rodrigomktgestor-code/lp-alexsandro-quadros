import os
from pathlib import Path

base = Path(r'c:\REP-ANTIGRAVITY\assets\images\properties')
html = '<html><body style="background:#333;color:white;font-family:sans-serif">'

# Auto-discover all property folders
slugs = sorted([d for d in os.listdir(base) if (base / d).is_dir()])

for slug in slugs:
    p = base / slug
    images = sorted([f for f in os.listdir(p) if f.endswith('.webp')])
    if not images:
        continue
    html += f'<h2 style="color:#ffdd55;border-bottom:1px solid #555;padding-bottom:4px">{slug} ({len(images)} imagens)</h2>'
    html += '<div style="display:flex;flex-wrap:wrap;gap:10px;margin-bottom:30px">'
    for f in images:
        html += f'<div style="text-align:center"><img src="assets/images/properties/{slug}/{f}" height="180" style="border:2px solid #555"><br><small>{f}</small></div>'
    html += '</div>'

html += '</body></html>'

with open(r'c:\REP-ANTIGRAVITY\picker.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f'picker.html gerado com {len(slugs)} empreendimentos.')
