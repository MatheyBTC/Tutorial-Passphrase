with open("D:/Claude/Proyectos/Tutorial-Passphrase/index.html", "rb") as f:
    raw = f.read()

print(f"Original size: {len(raw)}")

# Fix the remaining mojibake: 3-byte original UTF-8 sequences
# that were double-encoded through CP1252
# Pattern: C3A2 E282AC + (trailing bytes)
# -> restore to original E2 80 XX

fixes = [
    # em-dash U+2014 = E2 80 94
    # CP1252 decode: E2->a, 80->euro, 94->right-dbl-quote(U+201D=E2809D)
    (bytes.fromhex("c3a2e282ace2809d"), bytes.fromhex("e28094")),
    # bullet U+2022 = E2 80 A2
    # CP1252: 80->euro, A2->cent(0xA2 in cp1252=U+00A2=C2A2 in utf8)
    (bytes.fromhex("c3a2e282acc2a2"), bytes.fromhex("e280a2")),
    # ellipsis U+2026 = E2 80 A6
    # CP1252: A6->broken-bar(0xA6=U+00A6=C2A6 in utf8)
    (bytes.fromhex("c3a2e282acc2a6"), bytes.fromhex("e280a6")),
    # left single quote U+2018 = E2 80 98
    # CP1252: 0x98->tilde(U+02DC) ... hmm, let's check if it exists
    # left double quote U+201C = E2 80 9C
    # CP1252: 0x9C->OE-ligature? no... 0x93->left-double-quote
    # Actually in CP1252: 0x93=U+201C=left-dbl-quote -> E2809C in UTF-8
    (bytes.fromhex("c3a2e282ace2809c"), bytes.fromhex("e2809c")),
    # right single quote U+2019 = E2 80 99
    # CP1252: 0x92=U+2019 -> E28099 in UTF-8
    (bytes.fromhex("c3a2e282ace28099"), bytes.fromhex("e28099")),
    # en-dash U+2013 = E2 80 93
    (bytes.fromhex("c3a2e282ace28093"), bytes.fromhex("e28093")),
]

total = 0
for bad, good in fixes:
    cnt = raw.count(bad)
    if cnt > 0:
        try:
            good_char = good.decode("utf-8")
        except Exception:
            good_char = "?"
        print(f"Fixing {bad.hex()} -> {good.hex()} ({repr(good_char)}): {cnt}x")
        raw = raw.replace(bad, good)
        total += cnt

print(f"\nTotal fixes: {total}")
print(f"New size: {len(raw)}")

# Verify
remaining = raw.count(b"\xc3\xa2\xe2\x82\xac")
print(f"Remaining ae+euro patterns: {remaining}")

with open("D:/Claude/Proyectos/Tutorial-Passphrase/index.html", "wb") as f:
    f.write(raw)
print("Saved!")

# Final UTF-8 validation
with open("D:/Claude/Proyectos/Tutorial-Passphrase/index.html", "r", encoding="utf-8") as f:
    text = f.read()
print(f"UTF-8 read OK: {len(text)} chars")
