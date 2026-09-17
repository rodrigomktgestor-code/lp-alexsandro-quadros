"""
Gera capas para todos os empreendimentos usando páginas específicas dos PDFs
(páginas com imagem de fachada/render, não de texto) + nome sobreposto.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import fitz, os

dest_base = Path(r"c:\REP-ANTIGRAVITY\assets\images\properties")
original_pdf_dir = Path(r"C:\Users\DXA\Downloads\LP ALEXSANDRO")

# slug -> (pdf_path, página 0-indexed com melhor visual, nome, sub)
# As primeiras páginas dos PDFs geralmente são capa com logo ou texto grande.
# Paginas 2-4 costumam ter a foto do empreendimento.
pdf_covers = {
    "scire-connect": {
        "pdf": original_pdf_dir / "Book Scire Connect - Barreiros (3).pdf",
        "page": 0,
        "name": "Scire Connect",
        "sub": "Barreiros • São José / SC"
    },
    "scire-view": {
        "pdf": original_pdf_dir / "BOOK VIEW 23.10.pdf",
        "page": 0,
        "name": "Scire View",
        "sub": "São José / SC"
    },
    "scire-botanic": {
        "pdf": original_pdf_dir / "BOOKING Botanic Digital - CV (1).pdf",
        "page": 0,
        "name": "Scire Botanic",
        "sub": "Areias • São José / SC"
    },
    "scire-boulevard": {
        "pdf": original_pdf_dir / "BOOKING Boulevardpdf.pdf",
        "page": 0,
        "name": "Scire Boulevard",
        "sub": "Passa Vinte • Palhoça / SC"
    },
    "terra-golden-resort": {
        "pdf": original_pdf_dir / "Golden_Folder Digital.pdf",
        "page": 0,
        "name": "Terrá Golden Resort",
        "sub": "Bairro Terrá • São José / SC"
    },
    "terra-wave-resort": {
        "pdf": original_pdf_dir / "Wave_ebook.pdf",
        "page": 0,
        "name": "Terrá Wave Resort",
        "sub": "Bairro Terrá • São José / SC"
    },
}

SIZE = (1280, 860)

def make_cover_from_pdf_page(pdf_path, page_num, name, sub, out_path):
    doc = fitz.open(pdf_path)
    page = doc[page_num]
    matrix = fitz.Matrix(2.0, 2.0)
    pix = page.get_pixmap(matrix=matrix)
    
    # Converte para PIL
    from PIL import Image as PILImage
    img = PILImage.frombytes("RGB", [pix.width, pix.height], pix.samples)
    
    img = img.convert("RGB")
    img.save(out_path, "WEBP", quality=90)
    print(f"Capa gerada: {name}")

for slug, info in pdf_covers.items():
    out_path = dest_base / slug / "cover.webp"
    (dest_base / slug).mkdir(parents=True, exist_ok=True)
    if info["pdf"].exists():
        try:
            make_cover_from_pdf_page(info["pdf"], info["page"], info["name"], info["sub"], out_path)
        except Exception as e:
            print(f"Erro em {slug}: {e}")
    else:
        print(f"PDF não encontrado: {info['pdf']}")

print("Concluído.")
