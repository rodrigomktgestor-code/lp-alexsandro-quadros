import re

with open('js/properties.js', 'r', encoding='utf-8') as f:
    content = f.read()

m = re.search(r'slug:\s*"scire-boulevard",.*?gallery:\s*\[(.*?)\]', content, re.DOTALL)
if m:
    print(m.group(1).strip()[:200] + "\n...\n" + m.group(1).strip()[-200:])
else:
    print("Not found")
