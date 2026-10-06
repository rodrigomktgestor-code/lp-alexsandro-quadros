import re

with open('js/properties.js', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update cover image for Scire Way
# Find scire-way block and change its coverImage
content = re.sub(
    r'(slug:\s*"scire-way",.*?coverImage:\s*)"assets/images/properties/scire-way/cover\.webp\?v=\d+"',
    r'\g<1>"assets/images/properties/scire-way/image_1.webp?v=1"',
    content,
    flags=re.DOTALL
)

# 2. Remove photos 1 to 17 from Boulevard gallery
# Let's extract the Boulevard block
def remove_boulevard_images(match):
    block = match.group(0)
    # The gallery is within the block. We'll replace the gallery array
    gallery_match = re.search(r'gallery:\s*\[(.*?)\]', block, re.DOTALL)
    if gallery_match:
        gallery_content = gallery_match.group(1)
        # Split by comma
        items = [item.strip() for item in gallery_content.split(',') if item.strip()]
        
        # We need to filter out image_1 to image_17
        new_items = []
        for item in items:
            # Extract image number
            m = re.search(r'image_(\d+)\.webp', item)
            if m:
                img_num = int(m.group(1))
                if 1 <= img_num <= 17:
                    continue # Skip these
            new_items.append('            ' + item)
            
        new_gallery = ",\n".join(new_items)
        new_block = block[:gallery_match.start()] + f'gallery: [\n{new_gallery}\n        ]' + block[gallery_match.end():]
        return new_block
    return block

content = re.sub(r'slug:\s*"scire-boulevard",.*?\}\s*\}', remove_boulevard_images, content, flags=re.DOTALL)
# Wait, the regex for the block might be too greedy. Let's use a simpler approach.

with open('js/properties.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated properties.js")
