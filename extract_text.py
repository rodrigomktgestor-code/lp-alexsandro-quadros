import fitz

doc = fitz.open(r'C:\Users\DXA\Downloads\LP ALEXSANDRO\Scire Way Book.pdf')
text = ''
for i in range(min(20, len(doc))):  # just the first 20 pages for basic info
    text += doc.get_page_text(i)

print(text)
