# -*- coding: utf-8 -*-
"""
procesar_prints.py - Normaliza imagenes de producto para Tutorial-Passphrase

Logica:
  1. Recorta el fondo blanco de cada imagen
  2. Todos los productos escalan con el MISMO factor (el mas grande define la escala)
  3. Padding = 15% del lado mas largo del producto mas grande escalado
  4. Canvas = producto_max_escalado + padding*2 en cada lado
     → mismo canvas para TODAS las imagenes del set
  5. Productos mas chicos quedan centrados con un poco mas de margen (correcto)

Uso: python procesar_prints.py <carpeta> [--apply] [--scale 0.8]
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from pathlib import Path
from PIL import Image
import numpy as np

# -- Configuracion --------------------------------------------------------------
PADDING_RATIO = 0.10   # 15% del lado mas largo del producto mas grande
BG_COLOR      = (255, 255, 255)
BG_THRESHOLD  = 247

# Zona de muestreo para clasificacion de texto en pantalla
SAMPLE_X1, SAMPLE_X2 = 0.30, 0.70
SAMPLE_Y1, SAMPLE_Y2 = 0.15, 0.55


def crop_object(img: Image.Image):
    """Recorta fondo blanco. Devuelve (img_recortada, bbox)."""
    arr = np.array(img.convert("RGB"))
    mask = ~(
        (arr[:, :, 0] > BG_THRESHOLD) &
        (arr[:, :, 1] > BG_THRESHOLD) &
        (arr[:, :, 2] > BG_THRESHOLD)
    )
    rows = np.any(mask, axis=1)
    cols = np.any(mask, axis=0)
    if not rows.any() or not cols.any():
        return img, (0, 0, img.width, img.height)
    rmin, rmax = np.where(rows)[0][[0, -1]]
    cmin, cmax = np.where(cols)[0][[0, -1]]
    bbox = (int(cmin), int(rmin), int(cmax) + 1, int(rmax) + 1)
    return img.crop(bbox), bbox


def sample_screen_rgb(obj: Image.Image):
    w, h = obj.size
    region = np.array(obj.convert("RGB"))[
        int(h * SAMPLE_Y1):int(h * SAMPLE_Y2),
        int(w * SAMPLE_X1):int(w * SAMPLE_X2)
    ]
    bright = region[(region[:, :, 0] > 180) | (region[:, :, 1] > 180) | (region[:, :, 2] > 180)]
    if len(bright) == 0:
        return (0, 0, 0)
    return (int(bright[:, 0].mean()), int(bright[:, 1].mean()), int(bright[:, 2].mean()))


def classify_text(rgb):
    r, g, b = rgb
    if r == g == b == 0:
        return "sin datos"
    if (b - r) > 20 and b > 200:
        return "celeste"
    return "blanco"


def process_folder(folder: str, dry_run: bool = True, scale_override: float = None):
    src = Path(folder)
    if not src.exists():
        print(f"[X] Carpeta no encontrada: {src}")
        sys.exit(1)

    images = sorted([f for f in src.iterdir()
                     if f.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp")])
    if not images:
        print("[X] No se encontraron imagenes.")
        sys.exit(1)

    # -- Paso 1: recortar todas -------------------------------------------------
    crops = []
    for f in images:
        img = Image.open(f).convert("RGB")
        cropped, _ = crop_object(img)
        crops.append((f, img, cropped))

    max_crop_w = max(c.width  for _, _, c in crops)
    max_crop_h = max(c.height for _, _, c in crops)

    # -- Paso 2: scale factor ---------------------------------------------------
    # Por defecto scale=1 (resolucion original). Se puede bajar con --scale
    scale = scale_override if scale_override else 1.0

    # Dimensiones del producto mas grande escalado
    ref_w = int(max_crop_w * scale)
    ref_h = int(max_crop_h * scale)

    # Padding = 15% del lado mas largo del producto de referencia
    pad_px = int(max(ref_w, ref_h) * PADDING_RATIO)

    # Canvas identico para todas las imagenes
    canvas_w = ref_w + pad_px * 2
    canvas_h = ref_h + pad_px * 2

    print(f"\n{'-'*74}")
    print(f"  Carpeta :  {src}")
    print(f"  Imagenes:  {len(images)}")
    print(f"  Scale   :  {scale:.3f}")
    print(f"  Producto mas grande (recortado) : {max_crop_w}x{max_crop_h} px")
    print(f"  Producto mas grande (escalado)  : {ref_w}x{ref_h} px")
    print(f"  Padding (15% de {max(ref_w,ref_h)}px)          : {pad_px} px en los 4 lados")
    print(f"  Canvas UNICO para todo el set   : {canvas_w}x{canvas_h} px")
    print(f"{'-'*74}\n")
    print(f"  {'Archivo':<42} {'Recortado':>11}  {'Escalado':>11}  {'Margen V':>8}  {'Margen H':>8}  Clasif")
    print(f"  {'-'*42} {'-'*11}  {'-'*11}  {'-'*8}  {'-'*8}  {'-'*7}")

    results = []
    for f, img, cropped in crops:
        sw = int(cropped.width  * scale)
        sh = int(cropped.height * scale)
        margin_v = (canvas_h - sh) // 2
        margin_h = (canvas_w - sw) // 2
        rgb = sample_screen_rgb(cropped)
        cls = classify_text(rgb)
        print(f"  {f.name:<42} {cropped.width}x{cropped.height:>4}  {sw}x{sh:>4}  {margin_v:>8}  {margin_h:>8}  {cls}")
        results.append((f, cropped, cls))

    if dry_run:
        print(f"\n{'-'*74}")
        print("  Sin cambios aplicados.")
        print("  -> Corre con --apply para guardar en /procesadas")
        print(f"{'-'*74}\n")
        return

    # -- Paso 3: guardar --------------------------------------------------------
    out_dir = src / "procesadas"
    out_dir.mkdir(exist_ok=True)
    print(f"\n{'-'*74}")
    print(f"  Guardando en: {out_dir}\n")
    for f, cropped, cls in results:
        sw = int(cropped.width  * scale)
        sh = int(cropped.height * scale)
        resized = cropped.resize((sw, sh), Image.LANCZOS)
        canvas = Image.new("RGB", (canvas_w, canvas_h), BG_COLOR)
        x = (canvas_w - sw) // 2
        y = (canvas_h - sh) // 2
        canvas.paste(resized, (x, y))
        out_path = out_dir / (f.stem + ".png")
        canvas.save(out_path, "PNG", optimize=True)
        print(f"  OK  {f.name}  ->  {canvas_w}x{canvas_h}")
    print(f"\n  Listo. {len(results)} imagenes procesadas.")
    print(f"{'-'*74}\n")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python procesar_prints.py <carpeta> [--apply] [--scale 0.8]")
        sys.exit(1)

    folder = sys.argv[1]
    apply  = "--apply" in sys.argv

    scale_val = None
    if "--scale" in sys.argv:
        idx = sys.argv.index("--scale")
        scale_val = float(sys.argv[idx + 1])

    process_folder(folder, dry_run=not apply, scale_override=scale_val)
