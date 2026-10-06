"""
Analisa imagens do Scire Way com base em:
- Aspect ratio (renders e fotos têm proporcoes tipicas: 4:3, 16:9, 3:4, 1:1)
- Tamanho em KB (imagens com conteudo real sao maiores)
- Entropia/complexidade (imagens com conteudo real tem alta variancia de cores)
- Resolucao minima razoavel para exibicao em galeria
"""
import os
from pathlib import Path
from PIL import Image, ImageStat
import math, statistics

def image_entropy(img):
    """Calcula entropia da imagem como medida de complexidade visual."""
    img_gray = img.convert('L')
    hist = img_gray.histogram()
    total = sum(hist)
    entropy = 0
    for count in hist:
        if count > 0:
            p = count / total
            entropy -= p * math.log2(p)
    return entropy

# Numeros das imagens na galeria atual
gallery_nums = [
    1, 4, 5, 6, 9, 20, 31, 39, 40, 41, 42, 43, 44, 45, 47, 48, 49, 50,
    51, 52, 53, 54, 55, 56, 58, 59, 60, 65, 66, 67, 69, 70, 71,
    139, 140, 141, 142, 143, 144, 145, 148, 149, 150, 151, 152, 153,
    154, 155, 156, 159, 160, 161, 163, 165, 166, 167, 174, 185,
    195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207,
    208, 209, 210, 217, 221, 226, 227, 230, 231, 232, 233, 234, 235,
    243, 244, 245, 246, 248, 260, 261, 265, 266, 267, 268, 273, 274,
    278, 279, 284, 285, 286, 287, 288, 289, 409, 410, 411, 413
]

base = Path('assets/images/properties/scire-way')
results = []

for num in gallery_nums:
    f = base / f'image_{num}.webp'
    if not f.exists():
        continue
    
    size_kb = os.path.getsize(f) / 1024
    
    try:
        with Image.open(f) as img:
            w, h = img.size
            ratio = w / h
            entropy = image_entropy(img)
            
            # Stat da imagem - desvio padrao dos canais
            stat = ImageStat.Stat(img.convert('RGB'))
            std_dev = statistics.mean(stat.stddev)
            
            results.append({
                'num': num,
                'w': w, 'h': h,
                'ratio': ratio,
                'size_kb': size_kb,
                'entropy': entropy,
                'std_dev': std_dev
            })
    except Exception as e:
        print(f"Erro {num}: {e}")

# Classifica: REMOVE se:
# - entropia muito baixa (< 4.5) = imagens simples/brancas/logos
# - tamanho < 60kb = pouco conteudo
# - aspect ratio muito estranho (muito estreito/alto ou muito largo/baixo)
# - std_dev muito baixo = pouca variacao de cor

keep = []
remove = []

for r in results:
    num = r['num']
    ratio = r['ratio']
    entropy = r['entropy']
    size_kb = r['size_kb']
    std_dev = r['std_dev']
    w, h = r['w'], r['h']
    
    reasons = []
    
    # Aspect ratios ruins: muito fino/estreito
    if ratio < 0.5 or ratio > 3.0:
        reasons.append(f"bad_ratio:{ratio:.2f}")
    
    # Entropia muito baixa = conteudo visual pobre
    if entropy < 5.0:
        reasons.append(f"low_entropy:{entropy:.2f}")
    
    # Std dev muito baixo = imagem plana/monocromatica
    if std_dev < 20:
        reasons.append(f"low_stddev:{std_dev:.1f}")
    
    # Tamanho muito pequeno para o tamanho da imagem
    # (imagens de texto/branco sao pequenas mesmo sendo "grandes")
    bpp = (size_kb * 1024 * 8) / (w * h)
    if bpp < 0.15:
        reasons.append(f"low_bpp:{bpp:.3f}")
    
    if reasons:
        remove.append(num)
        print(f"REMOVE image_{num}: {r['w']}x{r['h']}, {size_kb:.0f}KB, entropy={entropy:.2f}, std={std_dev:.1f}, ratio={ratio:.2f} | {', '.join(reasons)}")
    else:
        keep.append(num)
        print(f"KEEP   image_{num}: {r['w']}x{r['h']}, {size_kb:.0f}KB, entropy={entropy:.2f}, std={std_dev:.1f}, ratio={ratio:.2f}")

print(f"\n=== SUMMARY ===")
print(f"KEEP ({len(keep)}): {keep}")
print(f"REMOVE ({len(remove)}): {remove}")
