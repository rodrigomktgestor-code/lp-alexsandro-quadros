import re

with open('js/properties.js', 'r', encoding='utf-8') as f:
    content = f.read()

content = re.sub(
    r'(slug:\s*"scire-way",.*?coverImage:\s*)"assets/images/properties/scire-way/cover\.webp\?v=1"',
    r'\g<1>"assets/images/properties/scire-way/cover.webp?v=2"',
    content,
    flags=re.DOTALL
)

with open('js/properties.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated version")
