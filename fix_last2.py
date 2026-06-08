import sys
sys.stdout.reconfigure(encoding='utf-8')

with open("D:/Claude/Proyectos/Tutorial-Passphrase/index.html", "rb") as f:
    raw = f.read()

fixes = [
    # ≠ U+2260 = E2 89 A0
    ("c3a2e280b0c2a0", "e289a0", "≠"),
    # ↑ U+2191 = E2 86 91
    ("c3a2e280a0e28098", "e28691", "↑"),
    # ⋯ U+22EF = E2 8B AF
    ("c3a2e280b9c2af",  "e28baf", "⋯"),
    # ✕ U+2715 = E2 9C 95 (close X)
    ("c3a2c593e280a2",  "e29c95", "✕"),
    # ✅ U+2705 = E2 9C 85
    ("c3a2c593e280a6",  "e29c85", "✅"),
    # ▼ U+25BC = E2 96 BC
    ("c3a2e28093c2bc",  "e296bc", "▼"),
    # ▶ U+25B6 = E2 96 B6
    ("c3a2e28093c2b6",  "e296b6", "▶"),
]

for bad_hex, good_hex, desc in fixes:
    bad = bytes.fromhex(bad_hex)
    good = bytes.fromhex(good_hex)
    cnt = raw.count(bad)
    if cnt > 0:
        raw = raw.replace(bad, good)
        print(f"  {desc}: {cnt}x")

# Final check
pos = 0
remaining = {}
while True:
    i = raw.find(b"\xc3\xa2", pos)
    if i < 0: break
    key = raw[i:i+9].hex()
    remaining[key] = remaining.get(key, 0) + 1
    pos = i + 1

if remaining:
    print(f"\nStill has c3a2 patterns: {len(remaining)} unique")
    for k, v in sorted(remaining.items(), key=lambda x: -x[1])[:10]:
        try:
            val = bytes.fromhex(k).decode('utf-8', errors='replace')
        except: val = '?'
        print(f"  {k}: {v}x = {val!r}")
else:
    print("\nAll clean!")

with open("D:/Claude/Proyectos/Tutorial-Passphrase/index.html", "wb") as f:
    f.write(raw)
print("Saved!")
