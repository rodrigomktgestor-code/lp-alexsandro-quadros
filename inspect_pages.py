"""Varre cada PDF e mostra quais páginas têm predominância de imagem (pouco texto)."""
import fitz
from pathlib import Path

original_pdf_dir = Path(r"C:\Users\DXA\Downloads\LP ALEXSANDRO")

pdfs = {
    "scire-connect": original_pdf_dir / "Book Scire Connect - Barreiros (3).pdf",
    "scire-view": original_pdf_dir / "BOOK VIEW 23.10.pdf",
    "scire-botanic": original_pdf_dir / "BOOKING Botanic Digital - CV (1).pdf",
    "scire-boulevard": original_pdf_dir / "BOOKING Boulevardpdf.pdf",
    "terra-golden-resort": original_pdf_dir / "Golden_Folder Digital.pdf",
    "terra-wave-resort": original_pdf_dir / "Wave_ebook.pdf",
}

for slug, pdf_path in pdfs.items():
    if not pdf_path.exists():
        continue
    doc = fitz.open(pdf_path)
    print(f"\n=== {slug} ({len(doc)} páginas) ===")
    for i, page in enumerate(doc):
        imgs = page.get_images(full=True)
        text = page.get_text().strip()
        text_words = len(text.split())
        img_area = sum(
            (info[2] * info[3]) for info in imgs if len(info) >= 4  # width * height approx
        )
        print(f"  Pág {i:02d}: {len(imgs)} imagens, {text_words} palavras")
