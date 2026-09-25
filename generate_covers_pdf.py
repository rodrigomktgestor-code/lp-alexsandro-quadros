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
        "pdf": original_pdf_dir / "VIEW/BOOK VIEW 23.10.pdf",
        "page": 0,
        "name": "Scire View",
        "sub": "Centro Histórico • São José / SC"
    },
    "scire-botanic": {
        "pdf": original_pdf_dir / "BOOKING Botanic Digital - CV (1).pdf",
        "page": 0,
        "name": "Scire Botanic",
        "sub": "Areias • São José / SC"
    },
    "terra-golden-resort": {
        "pdf": original_pdf_dir / "GOLDEN/Golden_Folder Digital.pdf",
        "page": 0,
        "name": "Terrá Golden Resort",
        "sub": "Bairro Terrá • São José / SC"
    },
    "terra-wave-resort": {
        "pdf": original_pdf_dir / "Wave_ebook.pdf",
        "page": 7,
        "name": "Terrá Wave Resort",
        "sub": "Bairro Terrá • São José / SC"
    },
    "san-george": {
        "pdf": original_pdf_dir / "SAN GEORGE/BOOK CLIENTE- SAN GEORGE.pdf",
        "page": 0,
        "name": "San George",
        "sub": "Velha • Blumenau / SC"
    },
    "viva-serenita": {
        "pdf": original_pdf_dir / "Viva Serenità/Book_Viva Serenita.pdf",
        "page": 0,
        "name": "Viva Serenità",
        "sub": "Fundos • Biguaçu / SC"
    },
    "bamburgo": {
        "pdf": original_pdf_dir / "BAMBURGO/BOOK CLIENTE - BAMBURGO.pdf",
        "page": 0,
        "name": "Bamburgo",
        "sub": "Blumenau / SC"
    },
    "gran-malltech": {
        "pdf": original_pdf_dir / "GRAN MALLTECH/01257 1 - GRAN MALLTECH - APRESENTAÇÃO DIGITA0_V05 (1).pdf",
        "page": 0,
        "name": "Gran Malltech",
        "sub": ""
    },
    "vivanti": {
        "pdf": original_pdf_dir / "VIVANTI/treinamento técnico.pdf",
        "page": 0,
        "name": "Palhoça Vivanti",
        "sub": "Pedra Branca • Palhoça / SC"
    },
    "aura": {
        "pdf": original_pdf_dir / "AURA/AURA-MAIO26-MATERIALDEVENDAS.pdf",
        "page": 0,
        "name": "Aurora (Aura)",
        "sub": ""
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
