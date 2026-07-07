# -*- coding: utf-8 -*-
"""
reemplazar_pantalla.py - Toma la imagen 09 como base y reemplaza
la pantalla con el contenido de cada una de las otras 17 imagenes.

Resultado: 18 imagenes con el cuerpo de la foto 09 + pantalla de cada paso.
Guardado en: /procesadas/con_pantalla_09/

Uso: python reemplazar_pantalla.py <carpeta_procesadas>
"""

import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from pathlib import Path
from PIL import Image
import numpy as np

BG_THRESHOLD  = 247
# Coordenadas de la pantalla detectadas en imagen 09 (fijas)
SCR_X1, SCR_X2 = 476, 851
SCR_Y1, SCR_Y2 = 198, 508

# Franja de busqueda de pantalla en otras imagenes (% del device)
SEARCH_X_MIN = 0.20
SEARCH_X_MAX = 0.42


def get_device_bbox(arr):
    mask = ~((arr[:,:,0]>BG_THRESHOLD) & (arr[:,:,1]>BG_THRESHOLD) & (arr[:,:,2]>BG_THRESHOLD))
    rows = np.where(np.any(mask, axis=1))[0]
    cols = np.where(np.any(mask, axis=0))[0]
    return int(cols[0]), int(rows[0]), int(cols[-1]), int(rows[-1])


def detect_screen(arr, dev_x1, dev_y1, dev_x2, dev_y2):
    """Detecta la region de pantalla en una imagen fuente."""
    dev_w = dev_x2 - dev_x1
    dev_h = dev_y2 - dev_y1
    xs = dev_x1 + int(dev_w * SEARCH_X_MIN)
    xe = dev_x1 + int(dev_w * SEARCH_X_MAX)
    zone = arr[dev_y1:dev_y2, xs:xe]

    bright = (zone[:,:,0]>160) & (zone[:,:,1]>160) & (zone[:,:,2]>160)
    col_sum = bright.sum(axis=0)
    row_sum = bright.sum(axis=1)
    active_cols = np.where(col_sum > max(col_sum.max()*0.03, 1))[0]
    active_rows = np.where(row_sum > max(row_sum.max()*0.03, 1))[0]

    if len(active_cols) == 0 or len(active_rows) == 0:
        return None

    margin = 30
    x1 = max(xs + int(active_cols[0])  - margin, dev_x1)
    x2 = min(xs + int(active_cols[-1]) + margin, xe)
    y1 = max(dev_y1 + int(active_rows[0])  - margin, dev_y1)
    y2 = min(dev_y1 + int(active_rows[-1]) + margin, dev_y2)
    return x1, y1, x2, y2


def main(folder: str):
    src = Path(folder)
    if not src.exists():
        print(f"[X] Carpeta no encontrada: {src}")
        sys.exit(1)

    images = sorted([
        f for f in src.iterdir()
        if f.suffix.lower() == ".png"
        and "_descartar" not in f.name
        and "ejemplo" not in f.name.lower()
        and "TEST_" not in f.name
        and "matriz_" not in f.name
        and "DEBUG_" not in f.name
        and "con_pantalla" not in f.name
    ])

    if len(images) != 18:
        print(f"[!] Se esperaban 18 imagenes, se encontraron {len(images)}:")
        for f in images:
            print(f"    {f.name}")
        sys.exit(1)

    # Cargar imagen base (09)
    base_file = next((f for f in images if "09_" in f.name), None)
    if not base_file:
        print("[X] No se encontro la imagen 09.")
        sys.exit(1)

    base_img = Image.open(base_file).convert("RGB")
    scr_w = SCR_X2 - SCR_X1
    scr_h = SCR_Y2 - SCR_Y1

    out_dir = src / "con_pantalla_09"
    out_dir.mkdir(exist_ok=True)

    print(f"\n{'-'*68}")
    print(f"  Base     : {base_file.name}")
    print(f"  Pantalla : x={SCR_X1}-{SCR_X2}  y={SCR_Y1}-{SCR_Y2}  ({scr_w}x{scr_h}px)")
    print(f"  Salida   : {out_dir}")
    print(f"{'-'*68}\n")
    print(f"  {'Archivo':<45} {'Pantalla detectada':>22}  Estado")
    print(f"  {'-'*45} {'-'*22}  {'-'*8}")

    for f in images:
        arr = np.array(Image.open(f).convert("RGB"))
        dx1, dy1, dx2, dy2 = get_device_bbox(arr)
        screen = detect_screen(arr, dx1, dy1, dx2, dy2)

        if screen is None:
            print(f"  {f.name:<45} {'no detectada':>22}  [SKIP]")
            continue

        sx1, sy1, sx2, sy2 = screen
        # Extraer contenido de pantalla de la imagen fuente
        screen_content = Image.fromarray(arr[sy1:sy2, sx1:sx2])
        # Redimensionar al tamaño exacto de la pantalla de la 09
        screen_resized = screen_content.resize((scr_w, scr_h), Image.LANCZOS)

        # Pegar sobre copia de la imagen 09
        result = base_img.copy()
        result.paste(screen_resized, (SCR_X1, SCR_Y1))

        out_name = f.stem + ".png"
        result.save(out_dir / out_name, "PNG", optimize=True)
        detected = f"{sx2-sx1}x{sy2-sy1}"
        print(f"  {f.name:<45} {detected:>22}  OK")

    print(f"\n  Listo. Imagenes en: {out_dir}")
    print(f"{'-'*68}\n")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python reemplazar_pantalla.py <carpeta_procesadas>")
        sys.exit(1)
    main(sys.argv[1])
