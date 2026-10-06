import fitz
from pathlib import Path
from PIL import Image
import io

def extract_pdf_images(pdf_path, output_dir, prefix='image'):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(pdf_path)
    count = 0
    
    for i in range(len(doc)):
        for img in doc.get_page_images(i):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image['image']
            image_ext = base_image['ext']
            
            try:
                img_pil = Image.open(io.BytesIO(image_bytes))
                if img_pil.mode not in ('RGB', 'RGBA'):
                    img_pil = img_pil.convert('RGB')
                
                # Resize if too large to save space
                img_pil.thumbnail((1920, 1080), Image.Resampling.LANCZOS)
                
                out_path = output_dir / f"{prefix}_{count}.webp"
                img_pil.save(out_path, "WEBP", quality=80)
                count += 1
            except Exception as e:
                print(f"Error extracting image {xref}: {e}")
                
    print(f"Extracted {count} images to {output_dir}")

extract_pdf_images(r'C:\Users\DXA\Downloads\LP ALEXSANDRO\Scire Way Book.pdf', r'c:\REP-ANTIGRAVITY\assets\images\properties\scire-way')
