"""Apenas regenera as capas do Scire Connect e Scire Boulevard."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import fitz

dest_base = Path(r"c:\REP-ANTIGRAVITY\assets\images\properties")
original_pdf_dir = Path(r"C:\Users\DXA\Downloads\LP ALEXSANDRO")

pdf_covers = {
    "scire-connect": {
        "pdf": original_pdf_dir / "Book Scire Connect - Barreiros (3).pdf",
        "page": 6,
        "name": "Scire Connect",
        "sub": "Barreiros • São José / SC"
    },

}

SIZE = (1280, 860)

def make_cover_from_pdf_page(pdf_path, page_num, name, sub, out_path):
    doc = fitz.open(pdf_path)
    page = doc[page_num]
    matrix = fitz.Matrix(2.0, 2.0)
    pix = page.get_pixmap(matrix=matrix)
    from PIL import Image as PILImage
    img = PILImage.frombytes("RGB", [pix.width, pix.height], pix.samples)
    w, h = img.size
    target_ratio = SIZE[0] / SIZE[1]
    img_ratio = w / h
    if img_ratio > target_ratio:
        new_h = SIZE[1]; new_w = int(new_h * img_ratio)
    else:
        new_w = SIZE[0]; new_h = int(new_w / img_ratio)
    img = img.resize((new_w, new_h), PILImage.Resampling.LANCZOS)
    left = (new_w - SIZE[0]) // 2; top = (new_h - SIZE[1]) // 2
    img = img.crop((left, top, left + SIZE[0], top + SIZE[1]))
    overlay = PILImage.new("RGBA", SIZE, (0, 0, 0, 0))
    draw_ov = ImageDraw.Draw(overlay)
    for y in range(SIZE[1]):
        alpha = int(255 * 0.80 * (y / SIZE[1]) ** 0.65)
        draw_ov.line([(0, y), (SIZE[0], y)], fill=(0, 0, 0, alpha))
    img = img.convert("RGBA")
    img = PILImage.alpha_composite(img, overlay).convert("RGB")
    draw = ImageDraw.Draw(img)
    def load_font(candidates, sz):
        for f in candidates:
            try: return ImageFont.truetype(f, sz)
            except: pass
        return ImageFont.load_default()
    ft = load_font(["C:/Windows/Fonts/segoeui.ttf","C:/Windows/Fonts/arial.ttf"], 80)
    fs = load_font(["C:/Windows/Fonts/segoeuil.ttf","C:/Windows/Fonts/arial.ttf"], 30)
    px, py = 72, SIZE[1] - 160
    draw.text((px+3, py+3), name, font=ft, fill=(0,0,0,100))
    draw.text((px, py), name, font=ft, fill=(255,255,255))
    draw.text((px+3, py+98), sub, font=fs, fill=(200,200,200))
    img.save(out_path, "WEBP", quality=82)
    print(f"Capa gerada: {name} (pág {page_num})")

for slug, info in pdf_covers.items():
    out_path = dest_base / slug / "cover.webp"
    if info["pdf"].exists():
        make_cover_from_pdf_page(info["pdf"], info["page"], info["name"], info["sub"], out_path)
    else:
        print(f"PDF não encontrado: {info['pdf']}")

print("Concluído.")
