import os, json, re
from pathlib import Path

prop_file = r'c:\REP-ANTIGRAVITY\js\properties.js'
with open(prop_file, 'r', encoding='utf-8') as f:
    content = f.read()

base = Path(r'c:\REP-ANTIGRAVITY\assets\images\properties')
props = ['terra-golden-resort', 'scire-view', 'scire-botanic', 'san-george', 'viva-serenita', 'the-line', 'bamburgo', 'gran-malltech', 'vivanti', 'aura']

for slug in props:
    p = base / slug
    if not p.exists(): continue
    
    images = sorted([f for f in os.listdir(p) if f.startswith('image_') and f.endswith('.webp')], 
                    key=lambda x: int(x.split('_')[1].split('.')[0]))
    
    gallery_arr = []
    for img in images:
        gallery_arr.append(f'            "assets/images/properties/{slug}/{img}?v=3"')
    
    gallery_str = 'gallery: [\n' + ',\n'.join(gallery_arr) + '\n        ],'
    
    # replace gallery array for this slug
    pattern = r'(slug:\s*"' + slug + r'"[\s\S]*?)gallery:\s*\[[\s\S]*?\],'
    
    def repl(m):
        return m.group(1) + gallery_str
        
    content = re.sub(pattern, repl, content)

with open(prop_file, 'w', encoding='utf-8') as f:
    f.write(content)
print('Updated properties.js')
