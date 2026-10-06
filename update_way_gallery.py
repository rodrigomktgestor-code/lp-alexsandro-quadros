import re

with open('js/properties.js', 'r', encoding='utf-8') as f:
    content = f.read()

gallery_items = []
# Only add up to 50 images to avoid performance issues
for i in range(min(50, 414)):
    gallery_items.append(f'            "assets/images/properties/scire-way/image_{i}.webp?v=1"')

gallery_str = ",\n".join(gallery_items)
replacement = f'        gallery: [\n{gallery_str}\n        ],'

pattern = re.compile(r'(slug:\s*"scire-way",.*?)gallery:\s*\[\],', re.DOTALL)
content = pattern.sub(r'\g<1>' + replacement, content)

with open('js/properties.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated properties.js for Scire Way")
