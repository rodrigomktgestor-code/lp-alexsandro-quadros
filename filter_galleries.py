import re
import os
from pathlib import Path
from PIL import Image

def get_good_images(slug):
    d = Path(f'assets/images/properties/{slug}')
    good_images = []
    
    if not d.exists():
        return []
        
    images = []
    for f in d.glob('*.webp'):
        if f.name == 'cover.webp':
            continue
        try:
            size_kb = os.path.getsize(f) / 1024
            with Image.open(f) as img:
                w, h = img.size
                
            # Filter criteria: substantial size and dimensions
            if w >= 600 and h >= 600 and size_kb >= 50:
                images.append(f)
        except:
            pass
            
    # Sort by number in filename
    images.sort(key=lambda x: int(x.name.split('_')[1].split('.')[0]))
    
    return [f'            "assets/images/properties/{slug}/{f.name}?v=2"' for f in images]

boulevard_gallery = get_good_images('scire-boulevard')
way_gallery = get_good_images('scire-way')

with open('js/properties.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace Boulevard gallery
def repl_blv(m):
    return f'gallery: [\n{chr(10).join(boulevard_gallery)}\n        ]'
content = re.sub(r'(slug:\s*"scire-boulevard",.*?)gallery:\s*\[.*?\]', r'\g<1>' + repl_blv(None), content, flags=re.DOTALL)

# Replace Way gallery
def repl_way(m):
    return f'gallery: [\n{chr(10).join(way_gallery)}\n        ]'
content = re.sub(r'(slug:\s*"scire-way",.*?)gallery:\s*\[.*?\]', r'\g<1>' + repl_way(None), content, flags=re.DOTALL)

with open('js/properties.js', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Boulevard photos kept: {len(boulevard_gallery)}")
print(f"Way photos kept: {len(way_gallery)}")
