import os
import shutil
from pathlib import Path
from PIL import Image

def process_image(src, dest):
    try:
        with Image.open(src) as img:
            # Convert to RGB if needed (e.g. RGBA pngs to WebP, or CMYK)
            if img.mode in ("RGBA", "P", "CMYK"):
                img = img.convert("RGB")
            # Resize if too large (max 1920x1920)
            img.thumbnail((1920, 1920), Image.Resampling.LANCZOS)
            img.save(dest, "WEBP", quality=80)
            print(f"Processed: {dest.name}")
    except Exception as e:
        print(f"Failed to process {src}: {e}")

src_base = Path(r"c:\REP-ANTIGRAVITY\temp_extract")
dest_base = Path(r"c:\REP-ANTIGRAVITY\assets\images\properties")

property_mappings = {
    "residencial-becker": src_base / "BECKER/BECKER",
    "san-george": src_base / "SAN_GEORGE/Imagens",
    "the-line": src_base / "the_line/IMAGENS",
    "viva-serenita": src_base / "viva_serenita"
}

# Since we don't have ZIPs for Scire Connect, Scire View, Botanic, Boulevard, Golden Resort, Wave Resort
# I will need to extract images from their PDFs!
# Let me write a function to extract images from PDFs.
import fitz

def extract_pdf_images(pdf_path, dest_dir):
    try:
        doc = fitz.open(pdf_path)
        img_count = 0
        for page_num in range(len(doc)):
            page = doc[page_num]
            image_list = page.get_images(full=True)
            for img_index, img_info in enumerate(image_list):
                xref = img_info[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]
                
                # Only save reasonably sized images (skip small icons)
                if len(image_bytes) < 100000: # 100kb threshold roughly
                    continue
                    
                img_path = dest_dir / f"extracted_{page_num}_{img_index}.{image_ext}"
                with open(img_path, "wb") as f:
                    f.write(image_bytes)
                
                # Convert to webp
                webp_path = dest_dir / f"image_{img_count}.webp"
                process_image(img_path, webp_path)
                
                # if it's the first image, make it cover
                if img_count == 0:
                    shutil.copy(webp_path, dest_dir / "cover.webp")
                    
                # Clean up original
                os.remove(img_path)
                img_count += 1
                if img_count >= 5: # Limit to 5 best images for now
                    return
    except Exception as e:
        print(f"Error extracting from {pdf_path}: {e}")

pdf_mappings = {
    "scire-connect": src_base / "Book Scire Connect - Barreiros (3).pdf",
    "scire-view": src_base / "BOOK VIEW 23.10.pdf",
    "scire-botanic": src_base / "BOOKING Botanic Digital - CV (1).pdf",
    "scire-boulevard": src_base / "BOOKING Boulevardpdf.pdf",
    "terra-golden-resort": src_base / "Golden_Folder Digital.pdf",
    "terra-wave-resort": src_base / "Wave_ebook.pdf"
}

for prop_slug, pdf_path in pdf_mappings.items():
    prop_dir = dest_base / prop_slug
    prop_dir.mkdir(parents=True, exist_ok=True)
    if pdf_path.exists():
        extract_pdf_images(pdf_path, prop_dir)

# Process ZIP folders
for prop_slug, src_dir in property_mappings.items():
    prop_dir = dest_base / prop_slug
    prop_dir.mkdir(parents=True, exist_ok=True)
    
    if src_dir.exists():
        img_count = 0
        for img_file in src_dir.glob("*"):
            if img_file.suffix.lower() in [".jpg", ".jpeg", ".png", ".webp"]:
                webp_path = prop_dir / f"image_{img_count}.webp"
                process_image(img_file, webp_path)
                if img_count == 0:
                    shutil.copy(webp_path, prop_dir / "cover.webp")
                img_count += 1
                if img_count >= 8:
                    break
