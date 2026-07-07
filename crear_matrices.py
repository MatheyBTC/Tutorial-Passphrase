# -*- coding: utf-8 -*-
"""
crear_matrices.py - Genera 3 matrices de 6 imagenes apiladas verticalmente

Logica:
  - Carga las 18 imagenes activas (sin _descartar) de /procesadas, ordenadas
  - Re-cropea el producto de cada una (elimina fondo blanco)
  - Apila 6 productos por matrix con:
      * Padding exterior (arriba/abajo/izq/der) = 10% del lado mayor del producto mas grande
      * Gap entre imagenes = mismo valor que el padding (un solo margen, no doble)
  - Ancho del canvas = producto_mas_ancho + padding*2 (igual que las individuales)
  - Guarda: matriz_01-06.png, matriz_07-12.png, matriz_13-18.png en /procesadas

Uso: python crear_matrices.py <carpeta_procesadas>
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from pathlib import Path
from PIL import Image
import numpy as np

BG_THRESHOLD = 247
BG_COLOR     = (255, 255, 255)
PADDING_RATIO = 0.10


def crop_object(img: Image.Image):
    arr = np.array(img.convert("RGB"))
    mask = ~(
        (arr[:, :, 0] > BG_THRESHOLD) &
        (arr[:, :, 1] > BG_THRESHOLD) &
        (arr[:, :, 2] > BG_THRESHOLD)
    )
    rows = np.any(mask, axis=1)
    cols = np.any(mask, axis=0)
    if not rows.any() or not cols.any():
        return img
    rmin, rmax = np.where(rows)[0][[0, -1]]
    cmin, cmax = np.where(cols)[0][[0, -1]]
    return img.crop((int(cmin), int(rmin), int(cmax)+1, int(rmax)+1))


def build_matrix(crops, canvas_w, cell_w, cell_h, pad_px, gap_px, label):
    """
    Apila los crops en celdas fijas (cell_w x cell_h).
    Cada producto se centra dentro de su celda → grilla perfectamente simetrica.
    """
    total_h = pad_px + cell_h * len(crops) + gap_px * (len(crops)-1) + pad_px
    canvas = Image.new("RGB", (canvas_w, total_h), BG_COLOR)
    y = pad_px
    for crop in crops:
        # Escalar el producto para que quepa en la celda manteniendo aspect ratio
        scale = min(cell_w / crop.width, cell_h / crop.height)
        nw, nh = int(crop.width * scale), int(crop.height * scale)
        resized = crop.resize((nw, nh), Image.LANCZOS)
        # Centrar dentro de la celda
        x = (canvas_w - nw) // 2
        cy = y + (cell_h - nh) // 2
        canvas.paste(resized, (x, cy))
        y += cell_h + gap_px
    print(f"  {label}: {canvas_w}x{total_h} px  (celda={cell_w}x{cell_h}, gap={gap_px}px, pad={pad_px}px)")
    return canvas


def main(folder: str):
    src = Path(folder)
    if not src.exists():
        print(f"[X] Carpeta no encontrada: {src}")
        sys.exit(1)

    # Cargar 18 activas ordenadas (excluir _descartar y el ejemplo)
    images = sorted([
        f for f in src.iterdir()
        if f.suffix.lower() == ".png"
        and "_descartar" not in f.name
        and "ejemplo" not in f.name.lower()
        and "TEST_" not in f.name
        and "matriz_" not in f.name
    ])

    if len(images) != 18:
        print(f"[!] Se esperaban 18 imagenes activas, se encontraron {len(images)}:")
        for f in images:
            print(f"    {f.name}")
        sys.exit(1)

    # Re-cropear todas
    crops = [crop_object(Image.open(f).convert("RGB")) for f in images]

    # Dimensiones de referencia
    max_w = max(c.width  for c in crops)
    max_h = max(c.height for c in crops)
    pad_px    = int(max(max_w, max_h) * PADDING_RATIO)
    canvas_w  = max_w + pad_px * 2
    gap_px    = pad_px   # un solo margen entre imagenes

    # Celda fija = producto más grande del set completo (mismo para las 3 matrices)
    cell_w   = max_w
    cell_h   = max_h
    canvas_w = cell_w + pad_px * 2

    print(f"\n{'─'*60}")
    print(f"  Imagenes            : {len(images)}")
    print(f"  Celda fija          : {cell_w}x{cell_h} px  (todos los productos iguales)")
    print(f"  Padding exterior    : {pad_px} px")
    print(f"  Gap entre imagenes  : {gap_px} px")
    print(f"  Ancho canvas        : {canvas_w} px")
    print(f"{'─'*60}\n")

    grupos = [
        (crops[0:6],   images[0:6],   "matriz_01-06"),
        (crops[6:12],  images[6:12],  "matriz_07-12"),
        (crops[12:18], images[12:18], "matriz_13-18"),
    ]

    for group_crops, group_files, label in grupos:
        print(f"  Grupo {label}:")
        for f in group_files:
            print(f"    {f.name}")
        matrix = build_matrix(group_crops, canvas_w, cell_w, cell_h, pad_px, gap_px, label)
        out = src / f"{label}.png"
        matrix.save(out, "PNG", optimize=True)
        print(f"  -> Guardado: {out.name}\n")

    print("  Listo. 3 matrices generadas.")
    print(f"{'─'*60}\n")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python crear_matrices.py <carpeta_procesadas>")
        sys.exit(1)
    main(sys.argv[1])
