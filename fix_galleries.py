import re, os
from pathlib import Path
from PIL import Image

def build_gallery(slug, min_size_kb=50, min_dim=600):
    d = Path(f'assets/images/properties/{slug}')
    images = []
    files = []
    for f in d.glob('*.webp'):
        if f.name == 'cover.webp': continue
        try:
            n = int(f.name.replace('image_','').replace('.webp',''))
            files.append((n, f))
        except: pass
    files.sort(key=lambda x: x[0])
    
    for _, f in files:
        try:
            size_kb = os.path.getsize(f) / 1024
            with Image.open(f) as img:
                w, h = img.size
            if w >= min_dim and h >= min_dim and size_kb >= min_size_kb:
                images.append(f'            "assets/images/properties/{slug}/{f.name}?v=2"')
        except:
            pass
    return images

boulevard_items = build_gallery('scire-boulevard')
way_items = build_gallery('scire-way')

print(f'Boulevard: {len(boulevard_items)} photos')
print(f'Way: {len(way_items)} photos')

content = open('js/properties.js', 'r', encoding='utf-8').read()

def replace_gallery(content, slug, items):
    slug_pos = content.find(f'slug: "{slug}"')
    if slug_pos == -1:
        print(f'ERROR: slug {slug} not found')
        return content
    gallery_pos = content.find('gallery:', slug_pos)
    open_bracket = content.find('[', gallery_pos)
    depth = 0
    pos = open_bracket
    while pos < len(content):
        if content[pos] == '[': depth += 1
        elif content[pos] == ']':
            depth -= 1
            if depth == 0: break
        pos += 1
    close_bracket = pos
    new_gallery = 'gallery: [\n' + ',\n'.join(items) + '\n        ]'
    content = content[:gallery_pos] + new_gallery + content[close_bracket+1:]
    return content

content = replace_gallery(content, 'scire-boulevard', boulevard_items)
content = replace_gallery(content, 'scire-way', way_items)

open('js/properties.js', 'w', encoding='utf-8').write(content)

# Verify
content2 = open('js/properties.js', 'r', encoding='utf-8').read()
blvd_pos = content2.find('slug: "scire-boulevard"')
g_pos = content2.find('gallery:', blvd_pos)
g_open = content2.find('[', g_pos)
print('Boulevard gallery snippet after fix:')
print(content2[g_pos:g_pos+200])
print('Done!')
