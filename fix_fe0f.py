import sys; sys.stdout.reconfigure(encoding='utf-8')
with open("D:/Claude/Proyectos/Tutorial-Passphrase/index.html", "rb") as f:
    raw = f.read()

# U+FE0F (variation selector-16, makes emojis colored) = EF B8 8F
# Double-encoded: EF->ï(U+00EF)->C3AF, B8->¸(U+00B8)->C2B8, 8F->ctrl(U+008F)->C28F
bad = bytes.fromhex("c3afc2b8c28f")
good = bytes.fromhex("efb88f")
cnt = raw.count(bad)
print(f"U+FE0F variation selector: {cnt}x")
raw = raw.replace(bad, good)

with open("D:/Claude/Proyectos/Tutorial-Passphrase/index.html", "wb") as f:
    f.write(raw)
print("Saved!")

with open("D:/Claude/Proyectos/Tutorial-Passphrase/index.html", "r", encoding="utf-8") as f:
    text = f.read()
print(f"UTF-8 OK, {len(text)} chars")
remaining = text.count("ï¸")
print(f"Remaining ï¸: {remaining}")
print(f"⚠️ count: {text.count(chr(0x26a0)+chr(0xfe0f))}")
