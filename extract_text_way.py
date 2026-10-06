import fitz

doc = fitz.open(r'C:\Users\DXA\Downloads\LP ALEXSANDRO\Scire Way Book.pdf')
text = ''
for i in range(min(40, len(doc))):
    text += doc.get_page_text(i)

with open('scire_way_info.txt', 'w', encoding='utf-8') as f:
    f.write(text)
