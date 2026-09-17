import os
import shutil
from pathlib import Path
from PIL import Image
import fitz  # PyMuPDF

def process_image(src, dest):
    try:
        with Image.open(src) as img:
            if img.mode in ("RGBA", "P", "CMYK"):
                img = img.convert("RGB")
            img.thumbnail((1920, 1920), Image.Resampling.LANCZOS)
            img.save(dest, "WEBP", quality=80)
            print(f"Processed: {dest.name}")
    except Exception as e:
        print(f"Failed to process {src}: {e}")

src_base = Path(r"c:\REP-ANTIGRAVITY\temp_extract")
dest_base = Path(r"c:\REP-ANTIGRAVITY\assets\images\properties")
original_pdf_dir = Path(r"C:\Users\DXA\Downloads\LP ALEXSANDRO")

pdf_mappings = {
    "scire-connect": original_pdf_dir / "Book Scire Connect - Barreiros (3).pdf",
    "scire-view": original_pdf_dir / "BOOK VIEW 23.10.pdf",
    "scire-botanic": original_pdf_dir / "BOOKING Botanic Digital - CV (1).pdf",
    "scire-boulevard": original_pdf_dir / "BOOKING Boulevardpdf.pdf",
    "terra-golden-resort": original_pdf_dir / "Golden_Folder Digital.pdf",
    "terra-wave-resort": original_pdf_dir / "Wave_ebook.pdf"
}

def render_pdf_pages(pdf_path, dest_dir):
    try:
        doc = fitz.open(pdf_path)
        img_count = 0
        
        # Render the first 5-8 pages of the PDF to use as gallery/cover
        num_pages = min(8, len(doc))
        
        for page_num in range(num_pages):
            page = doc[page_num]
            # Zoom to get better resolution (dpi ~ 150)
            matrix = fitz.Matrix(2.0, 2.0)
            pix = page.get_pixmap(matrix=matrix)
            
            img_path = dest_dir / f"temp_{page_num}.png"
            pix.save(str(img_path))
            
            webp_path = dest_dir / f"image_{img_count}.webp"
            process_image(img_path, webp_path)
            
            # Make the first page the cover
            if img_count == 0:
                shutil.copy(webp_path, dest_dir / "cover.webp")
                
            os.remove(img_path)
            img_count += 1
            
        print(f"Successfully rendered {img_count} images for {dest_dir.name}")
    except Exception as e:
        print(f"Error rendering PDF {pdf_path}: {e}")

# Render PDFs
for prop_slug, pdf_path in pdf_mappings.items():
    prop_dir = dest_base / prop_slug
    prop_dir.mkdir(parents=True, exist_ok=True)
    if pdf_path.exists():
        render_pdf_pages(pdf_path, prop_dir)
        
print("Asset preparation completed.")
