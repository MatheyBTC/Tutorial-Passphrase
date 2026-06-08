import sys
sys.stdout.reconfigure(encoding='utf-8')

with open("D:/Claude/Proyectos/Tutorial-Passphrase/index.html", "rb") as f:
    raw = f.read()

print(f"Original size: {len(raw)}")

# All double-encoded 3-byte UTF-8 sequences
# Each entry: (bad_bytes_hex, good_bytes_hex, description)
# Logic: original UTF-8 byte sequence [E2 XX YY] was read as CP1252 chars
# and re-encoded to UTF-8. We reverse that.
# E2 -> CP1252 -> â (U+00E2) -> UTF-8 -> C3 A2
# XX -> CP1252 -> some char -> UTF-8 -> varies
# YY -> CP1252 -> some char -> UTF-8 -> varies

fixes = [
    # ➜ U+279C = E2 9E 9C
    # 9E in CP1252 = ž (U+017E) -> UTF-8 C5 BE
    # 9C in CP1252 = œ (U+0153) -> UTF-8 C5 93
    ("c3a2c5bec593", "e29e9c", "➜ arrow right"),

    # → U+2192 = E2 86 92
    # 86 in CP1252 = † (U+2020) -> UTF-8 E2 80 A0
    # 92 in CP1252 = ' (U+2019 right-single-quote) -> UTF-8 E2 80 99
    ("c3a2e280a0e28099", "e28692", "→ arrow"),

    # ═ U+2550 = E2 95 90
    # 95 in CP1252 = • (U+2022 bullet) -> UTF-8 E2 80 A2
    # 90 in CP1252 = U+0090 (control) -> UTF-8 C2 90
    ("c3a2e280a2c290", "e29590", "═ box double horiz"),

    # ─ U+2500 = E2 94 80
    # 94 in CP1252 = " (U+201D right-dbl-quote) -> UTF-8 E2 80 9D
    # 80 in CP1252 = € (U+20AC euro) -> UTF-8 E2 82 AC
    ("c3a2e2809de282ac", "e29480", "─ box single horiz"),

    # ☰ U+2630 = E2 98 B0
    # 98 in CP1252 = U+0098 (control) -> UTF-8 C2 98
    # B0 in CP1252 = ° (U+00B0 degree) -> UTF-8 C2 B0
    ("c3a2c298c2b0", "e298b0", "☰ hamburger"),

    # ✕ U+2715 = E2 9C 95
    # 9C in CP1252 = œ (U+0153) -> UTF-8 C5 93
    # 95 in CP1252 = U+0095 (control) -> UTF-8 C2 95
    ("c3a2c593c295", "e29c95", "✕ close X"),

    # ✓ U+2713 = E2 9C 93
    # 9C in CP1252 = œ (U+0153) -> UTF-8 C5 93
    # 93 in CP1252 = " (U+201C left-dbl-quote) -> UTF-8 E2 80 9C
    ("c3a2c593e2809c", "e29c93", "✓ checkmark"),

    # ⚠ U+26A0 = E2 9A A0
    # 9A in CP1252 = š (U+0161) -> UTF-8 C5 A1
    # A0 in CP1252 = nbsp (U+00A0) -> UTF-8 C2 A0
    ("c3a2c5a1c2a0", "e29aa0", "⚠ warning"),

    # ≤ U+2264 = E2 89 A4
    # 89 in CP1252 = ‰ (U+2030) -> UTF-8 E2 80 B0
    # A4 in CP1252 = ¤ (U+00A4) -> UTF-8 C2 A4
    ("c3a2e280b0c2a4", "e289a4", "≤ less-equal"),

    # ≥ U+2265 = E2 89 A5
    # 89 in CP1252 = ‰ -> E2 80 B0
    # A5 in CP1252 = ¥ (U+00A5) -> UTF-8 C2 A5
    ("c3a2e280b0c2a5", "e289a5", "≥ greater-equal"),

    # ‹ U+2039 = E2 80 B9
    # 80 -> € (U+20AC) -> E2 82 AC
    # B9 -> ¹ (U+00B9) -> C2 B9
    ("c3a2e282acc2b9", "e280b9", "‹ single left angle"),

    # – U+2013 = E2 80 93 (en-dash, already fixed as part of earlier fixes? check)
    # 80 -> € -> E2 82 AC
    # 93 -> " (U+201C) -> E2 80 9C
    ("c3a2e282ace2809c", "e28093", "– en-dash"),

    # ' U+2018 = E2 80 98 (left single quote)
    # 80 -> € -> E2 82 AC
    # 98 -> U+0098 control -> C2 98
    ("c3a2e282acc298", "e28098", "' left-single-quote"),

    # ╔ U+2554 = E2 95 94
    # 95 -> • (U+2022) -> E2 80 A2
    # 94 -> " (U+201D) -> E2 80 9D
    ("c3a2e280a2e2809d", "e29594", "╔ box corner"),

    # ╗ U+2557 = E2 95 97
    # 95 -> • -> E2 80 A2
    # 97 -> U+0097 -> C2 97
    ("c3a2e280a2c297", "e29597", "╗ box corner"),

    # ╚ U+255A = E2 95 9A
    # 95 -> • -> E2 80 A2
    # 9A -> š (U+0161) -> C5 A1
    ("c3a2e280a2c5a1", "e2959a", "╚ box corner"),

    # ╝ U+255D = E2 95 9D
    # 95 -> • -> E2 80 A2
    # 9D -> U+009D control -> C2 9D
    ("c3a2e280a2c29d", "e2959d", "╝ box corner"),

    # ║ U+2551 = E2 95 91
    # 95 -> • -> E2 80 A2
    # 91 -> ' (U+2018 left-single-quote) -> E2 80 98
    ("c3a2e280a2e28098", "e29591", "║ box vertical"),

    # ╠ U+2560 = E2 95 A0
    # 95 -> • -> E2 80 A2
    # A0 -> nbsp -> C2 A0
    ("c3a2e280a2c2a0", "e295a0", "╠ box T-right"),

    # ╣ U+2563 = E2 95 A3
    # 95 -> • -> E2 80 A2
    # A3 -> £ (U+00A3) -> C2 A3
    ("c3a2e280a2c2a3", "e295a3", "╣ box T-left"),

    # ╦ U+2566 = E2 95 A6
    # 95 -> • -> E2 80 A2
    # A6 -> ¦ (U+00A6) -> C2 A6
    ("c3a2e280a2c2a6", "e295a6", "╦ box T-top"),

    # ╩ U+2569 = E2 95 A9
    # 95 -> • -> E2 80 A2
    # A9 -> © (U+00A9) -> C2 A9
    ("c3a2e280a2c2a9", "e295a9", "╩ box T-bottom"),

    # ╬ U+256C = E2 95 AC
    # 95 -> • -> E2 80 A2
    # AC -> ¬ (U+00AC) -> C2 AC
    ("c3a2e280a2c2ac", "e295ac", "╬ box cross"),
]

total = 0
for bad_hex, good_hex, desc in fixes:
    bad = bytes.fromhex(bad_hex)
    good = bytes.fromhex(good_hex)
    cnt = raw.count(bad)
    if cnt > 0:
        raw = raw.replace(bad, good)
        print(f"  {desc}: {cnt}x")
        total += cnt

print(f"\nTotal: {total} replacements")
print(f"New size: {len(raw)}")

# Check remaining c3a2 patterns
pos = 0
remaining = {}
while True:
    i = raw.find(b"\xc3\xa2", pos)
    if i < 0:
        break
    key = raw[i:i+6].hex()
    remaining[key] = remaining.get(key, 0) + 1
    pos = i + 1

if remaining:
    print(f"\nStill has {len(remaining)} c3a2 patterns:")
    for k, v in sorted(remaining.items(), key=lambda x: -x[1]):
        print(f"  {k}: {v}x")
else:
    print("\nAll c3a2 patterns resolved!")

with open("D:/Claude/Proyectos/Tutorial-Passphrase/index.html", "wb") as f:
    f.write(raw)
print("Saved!")

# Verify UTF-8
with open("D:/Claude/Proyectos/Tutorial-Passphrase/index.html", "r", encoding="utf-8") as f:
    text = f.read()
print(f"UTF-8 OK: {len(text)} chars")
