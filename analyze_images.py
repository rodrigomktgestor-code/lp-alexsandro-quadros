from pathlib import Path
import os
from PIL import Image

def analyze_dir(d):
    print(f"\nAnalyzing {d}")
    path = Path(d)
    if not path.exists(): return
    images = []
    for f in path.glob("*.webp"):
        if f.name == "cover.webp": continue
        size_kb = os.path.getsize(f) / 1024
        try:
            with Image.open(f) as img:
                w, h = img.size
                # calculate a basic "compressibility" score: file size / total pixels
                # Renders are complex and have high bits per pixel
                # Text/flat colors have very low bits per pixel
                bpp = (os.path.getsize(f) * 8) / (w * h)
                images.append({"name": f.name, "size": size_kb, "w": w, "h": h, "bpp": bpp})
        except:
            pass
            
    images.sort(key=lambda x: int(x['name'].split('_')[1].split('.')[0]))
    for img in images:
        print(f"{img['name']}: {img['w']}x{img['h']}, {img['size']:.1f} KB, bpp: {img['bpp']:.3f}")

analyze_dir(r'assets\images\properties\scire-boulevard')
analyze_dir(r'assets\images\properties\scire-way')
