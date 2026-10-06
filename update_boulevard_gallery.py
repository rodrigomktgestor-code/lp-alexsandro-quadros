import re

with open('js/properties.js', 'r', encoding='utf-8') as f:
    content = f.read()

# For Boulevard
start_idx = content.find('slug: "scire-boulevard"')
if start_idx != -1:
    gallery_start = content.find('gallery: [', start_idx)
    gallery_end = content.find('],', gallery_start)
    
    gallery_block = content[gallery_start:gallery_end]
    items = gallery_block.split(',')
    
    new_items = []
    for item in items:
        if 'gallery: [' in item:
            new_items.append('gallery: [\n')
            item = item.replace('gallery: [', '')
            
        m = re.search(r'image_(\d+)\.webp', item)
        if m:
            num = int(m.group(1))
            if 1 <= num <= 17:
                continue
        
        if item.strip():
            new_items.append('            ' + item.strip())
            
    new_gallery = ",\n".join(new_items)
    new_gallery = new_gallery.replace('gallery: [\n,', 'gallery: [\n')
    
    content = content[:gallery_start] + new_gallery + '\n        ' + content[gallery_end:]
    
with open('js/properties.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed Boulevard gallery")
