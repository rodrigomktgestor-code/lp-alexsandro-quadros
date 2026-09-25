"""
Gera uma capa profissional para cada empreendimento:
  - Pega a melhor foto de fundo disponível
  - Escurece com um gradiente
  - Escreve o nome do empreendimento com tipografia limpa
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import textwrap, shutil, os

dest_base = Path(r"c:\REP-ANTIGRAVITY\assets\images\properties")
src_images = Path(r"c:\REP-ANTIGRAVITY\temp_extract")

# Mapeamento: slug -> (arquivo de fundo, nome exibido, subtítulo)
# Para empreendimentos cujas imagens já foram extraídas para assets/,
# apontamos diretamente para a imagem desejada como capa.
covers = {

    "scire-connect": {
        "bg": dest_base / "scire-connect/cover.webp",
        "name": "Scire Connect",
        "sub": "Barreiros • São José / SC"
    },
    "scire-view": {
        "bg": dest_base / "scire-view/image_1.webp",
        "name": "Scire View",
        "sub": "Centro Histórico • São José / SC"
    },
    "scire-botanic": {
        "bg": dest_base / "scire-botanic/image_1.webp",
        "name": "Scire Botanic",
        "sub": "Areias • São José / SC"
    },
    "terra-golden-resort": {
        "bg": dest_base / "terra-golden-resort/image_104_right.webp",
        "name": "Terrá Golden Resort",
        "sub": "Terrá • São José / SC"
    },
    "terra-wave-resort": {
        "bg": dest_base / "terra-wave-resort/cover.webp",
        "name": "Terrá Wave Resort",
        "sub": "Terrá • São José / SC"
    },
    "san-george": {
        "bg": dest_base / "san-george/image_12.webp",
        "name": "San George",
        "sub": "Velha • Blumenau / SC"
    },
    "the-line": {
        "bg": dest_base / "the-line/image_0.webp",
        "name": "The Line",
        "sub": "Londrina / PR"
    },
    "viva-serenita": {
        "bg": dest_base / "viva-serenita/image_102.webp",
        "name": "Viva Serenità",
        "sub": "Fundos • Biguaçu / SC"
    },
    "bamburgo": {
        "bg": dest_base / "bamburgo/image_100.webp",
        "name": "Bamburgo",
        "sub": "Blumenau / SC"
    },
    "gran-malltech": {
        "bg": dest_base / "gran-malltech/image_100.webp",
        "name": "Gran Malltech",
        "sub": ""
    },
    "vivanti": {
        "bg": dest_base / "vivanti/image_100.webp",
        "name": "Palhoça Vivanti",
        "sub": "Pedra Branca • Palhoça / SC"
    },
    "aura": {
        "bg": dest_base / "aura/image_100.webp",
        "name": "Aurora (Aura)",
        "sub": ""
    },
}

def make_cover(bg_path: Path, name: str, sub: str, out_path: Path, size=(1280, 860)):
    # Abre e recorta o fundo
    with Image.open(bg_path) as img:
        if img.mode in ("RGBA", "P", "CMYK"):
            img = img.convert("RGB")
        # Redimensiona mantendo proporção e recorta ao centro
        img_ratio = img.width / img.height
        target_ratio = size[0] / size[1]
        if img_ratio > target_ratio:
            new_h = size[1]
            new_w = int(new_h * img_ratio)
        else:
            new_w = size[0]
            new_h = int(new_w / img_ratio)
        img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
        left = (new_w - size[0]) // 2
        top = (new_h - size[1]) // 2
        img = img.crop((left, top, left + size[0], top + size[1]))
        base = img.copy()

    # Gradiente escuro cobrindo parte inferior
    overlay = Image.new("RGBA", size, (0, 0, 0, 0))
    draw_ov = ImageDraw.Draw(overlay)
    for y in range(size[1]):
        # Gradiente: transparente no topo, opaco (0.75) na base
        alpha = int(255 * 0.75 * (y / size[1]) ** 0.7)
        draw_ov.line([(0, y), (size[0], y)], fill=(0, 0, 0, alpha))

    base = base.convert("RGBA")
    base = Image.alpha_composite(base, overlay).convert("RGB")

    # Texto
    draw = ImageDraw.Draw(base)

    # Tenta fontes disponíveis no Windows
    font_candidates_bold = [
        "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arial.ttf",
    ]
    font_candidates_reg = [
        "C:/Windows/Fonts/segoeuil.ttf",
        "C:/Windows/Fonts/ariali.ttf",
        "C:/Windows/Fonts/arial.ttf",
    ]

    def load_font(candidates, size_pt):
        for f in candidates:
            try:
                return ImageFont.truetype(f, size_pt)
            except Exception:
                pass
        return ImageFont.load_default()

    font_title = load_font(font_candidates_bold, 90)
    font_sub   = load_font(font_candidates_reg, 32)

    pad_x = 72
    pad_y = size[1] - 160

    # Sombra suave no nome
    shadow_offset = 3
    draw.text((pad_x + shadow_offset, pad_y + shadow_offset), name,
              font=font_title, fill=(0, 0, 0, 120))
    draw.text((pad_x, pad_y), name, font=font_title, fill=(255, 255, 255))

    # Subtítulo
    draw.text((pad_x + 4, pad_y + 106), sub, font=font_sub, fill=(200, 200, 200))

    base.save(out_path, "WEBP", quality=82)
    print(f"Capa gerada: {out_path.name} ({name})")


for slug, info in covers.items():
    prop_dir = dest_base / slug
    prop_dir.mkdir(parents=True, exist_ok=True)
    out = prop_dir / "cover.webp"

    if info["bg"].exists():
        make_cover(info["bg"], info["name"], info["sub"], out)
    else:
        print(f"AVISO: imagem de fundo não encontrada para {slug}: {info['bg']}")

print("Concluído.")
