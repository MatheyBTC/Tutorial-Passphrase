import re

file = "D:/Claude/Proyectos/Tutorial-Passphrase/index.html"

# Read file as raw bytes
with open(file, "rb") as f:
    raw = f.read()

print(f"File size: {len(raw)} bytes")

# Check what kind of encoding issue we have
# Look for the Configuracion pattern in bytes
idx = raw.find(b"Configuraci")
if idx >= 0:
    chunk = raw[idx:idx+25]
    print(f"'Configuraci...' hex: {chunk.hex()}")
    print(f"latin-1: {chunk.decode('latin-1')}")
    try:
        print(f"utf-8: {chunk.decode('utf-8')}")
    except Exception as e:
        print(f"utf-8 error: {e}")

# Search for 0xC3 0x83 sequence (UTF-8 encoded latin-1 'Ã')
pos = 0
mojibake_count = 0
while True:
    idx = raw.find(b"\xc3\x83", pos)
    if idx < 0:
        break
    mojibake_count += 1
    if mojibake_count <= 5:
        print(f"Found C3 83 at {idx}: {raw[idx:idx+8].hex()} = {raw[idx:idx+8].decode('latin-1')}")
    pos = idx + 1
print(f"Total C3 83 (Ã) sequences: {mojibake_count}")

# Also check for C3 B3 (valid UTF-8 'o with accent')
pos = 0
valid_count = 0
while True:
    idx = raw.find(b"\xc3\xb3", pos)
    if idx < 0:
        break
    valid_count += 1
    pos = idx + 1
print(f"Total C3 B3 (valid utf-8 o-accent) sequences: {valid_count}")
