import sys
sys.stdout.reconfigure(encoding='utf-8')

with open("D:/Claude/Proyectos/Tutorial-Passphrase/index.html", "rb") as f:
    raw = f.read()

print(f"Size: {len(raw)}")

fixes = [
    # lock emoji
    (bytes.fromhex("c3b0c5b8e2809dc290"), bytes.fromhex("f09f9490")),
    # camera emoji
    (bytes.fromhex("c3b0c5b8e2809cc2b7"), bytes.fromhex("f09f93b7")),
    # section sign double-encoded
    (bytes.fromhex("c382c2a7"), bytes.fromhex("c2a7")),
]

for bad, good in fixes:
    cnt = raw.count(bad)
    if cnt > 0:
        print(f"Fixing {bad.hex()} -> {good.hex()}: {cnt}x")
        raw = raw.replace(bad, good)

with open("D:/Claude/Proyectos/Tutorial-Passphrase/index.html", "wb") as f:
    f.write(raw)
print("Saved!")

import re
with open("D:/Claude/Proyectos/Tutorial-Passphrase/index.html", "r", encoding="utf-8") as f:
    text = f.read()
print(f"UTF-8 OK: {len(text)} chars")
bad = re.findall(r"[ÃÂ][^\sa-zA-Z<>\"'(){};,._\-/\\0-9\n\r\t!?]", text)
print(f"Remaining Ã/Â sequences: {len(bad)}")
print(f"Lock emojis: {text.count(chr(0x1f510))}, Camera: {text.count(chr(0x1f4f7))}")
