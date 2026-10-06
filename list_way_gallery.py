import re
content = open('js/properties.js', 'r', encoding='utf-8').read()
way_pos = content.find('slug: "scire-way"')
g_pos = content.find('gallery:', way_pos)
g_open = content.find('[', g_pos)
depth = 0
pos = g_open
while pos < len(content):
    if content[pos] == '[': depth += 1
    elif content[pos] == ']':
        depth -= 1
        if depth == 0: break
    pos += 1
gallery_block = content[g_open+1:pos]
items = [i.strip().strip('"') for i in gallery_block.split(',') if 'webp' in i]
print('\n'.join(items))
print(f'\nTotal: {len(items)} images')
