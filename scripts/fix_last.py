import sys
sys.stdout.reconfigure(encoding='utf-8')

with open("D:/Claude/Proyectos/Tutorial-Passphrase/index.html", "rb") as f:
    raw = f.read()

# Find the remaining 5 patterns
patterns = ["c3a2e280b0c2", "c3a2e280a0e2", "c3a2e280b9c2", "c3a2c593e280", "c3a2e28093c2"]
for p in patterns:
    pat = bytes.fromhex(p)
    cnt = raw.count(pat)
    if cnt > 0:
        idx = raw.find(pat)
        chunk = raw[idx:idx+9]
        print(f"{p} ({cnt}x): {chunk.hex()} -> {chunk.decode('utf-8',errors='replace')!r}")

# Fixes:
# c3a2e280b0c2XX:
#  80 in CP1252 = € (U+20AC) ... wait no, I already said 89 in CP1252 = ‰
# Actually: c3a2=â(E2), e280b0=‰(U+2030), c2XX=?
# U+2030 ‰ in CP1252 = byte 0x89, not 0x80
# So the original UTF-8 was E2 89 XX where XX depends on what follows c2
# Looking at c3a2e280b0c2: next byte matters. Let's check what follows
pos = 0
seen = {}
for pat_hex in ["c3a2e280b0c2", "c3a2e280a0e2", "c3a2e280b9c2", "c3a2c593e280", "c3a2e28093c2"]:
    pat = bytes.fromhex(pat_hex)
    pos = 0
    vals = {}
    while True:
        i = raw.find(pat, pos)
        if i < 0: break
        full = raw[i:i+9].hex()
        vals[full] = vals.get(full, 0) + 1
        pos = i + 1
    print(f"\n{pat_hex}:")
    for k, v in vals.items():
        print(f"  {k}: {v}x -> {bytes.fromhex(k).decode('utf-8',errors='replace')!r}")
