with open("D:/Claude/Proyectos/Tutorial-Passphrase/index.html", "rb") as f:
    raw = f.read()

# Check emoji patterns
print("=== Emoji analysis ===")

# 🔐 = U+1F510 = F0 9F 94 90
# When F0 9F 94 90 bytes get CP1252 decoded:
# F0 = 'ð' (U+00F0 in latin-1/cp1252)
# 9F = ' ' (U+009F control char in unicode, but in CP1252 byte 9F = Ÿ (U+0178))
# 94 = '"' (right double quote U+201D in CP1252) -> E2 80 9D in UTF-8
# 90 = control (U+0090 in unicode) ... in CP1252 byte 90 is undefined?
# Actually CP1252: byte 90 = U+0090 (control character)

# So re-encoding as UTF-8:
# ð (U+00F0) -> C3 B0
# Ÿ (U+0178) -> C5 B8
# " (U+201D) -> E2 80 9D (already fixed to U+2014? no...)
# U+0090 control -> C2 90

pattern_90 = b"\xc3\xb0\xc5\xb8"  # ðŸ
cnt = raw.count(pattern_90)
print(f"ðŸ (C3B0 C5B8) found: {cnt} times")
if cnt > 0:
    idx = raw.find(pattern_90)
    print(f"  At {idx}: {raw[idx:idx+12].hex()}")
    # What follows?
    follows = {}
    pos = 0
    while True:
        i = raw.find(pattern_90, pos)
        if i < 0:
            break
        key = raw[i+2:i+8].hex()
        follows[key] = follows.get(key, 0) + 1
        pos = i + 1
    print(f"  What follows C3B0 C5B8:")
    for k, v in sorted(follows.items(), key=lambda x: -x[1]):
        print(f"    {k}: {v}x")

# The fix: C3B0 C5B8 E28094 C290 -> F0 9F 94 90 (🔐)
# Wait, after fixing em-dash, E28094 is now em-dash again
# But in the emoji case, C2 94 (U+0094) should have become...
# Actually: byte 0x94 in CP1252 = U+201D (right double quote) = E2 80 9D
# But I ALREADY fixed E2 80 9D -> E2 80 94 in fix6.py!
# So now the 4th byte (0x94) is part of 'em-dash' E2 80 94... that's a collision!

# Let me check: after fix6.py, what does the emoji context look like?
# The emoji F0 9F 94 90 when CP1252 decoded:
# F0 -> ð (C3 B0)
# 9F -> Ÿ (C5 B8)
# 94 -> " (right double quote, now fixed to em-dash E2 80 94)
# 90 -> control U+0090 (C2 90)

# So the current file should have: C3B0 C5B8 [E28094 or E2809D] C290
# After fix6.py converted E2809D -> E28094:
fix_pattern = b"\xc3\xb0\xc5\xb8\xe2\x80\x94\xc2\x90"
cnt2 = raw.count(fix_pattern)
print(f"ðŸ+em-dash+ctrl (C3B0 C5B8 E28094 C290): {cnt2} times")

# Check without the C290
fix_pattern2 = b"\xc3\xb0\xc5\xb8\xe2\x80\x94"
cnt3 = raw.count(fix_pattern2)
print(f"ðŸ+em-dash (C3B0 C5B8 E28094): {cnt3} times")

# Show all occurrences of C3B0
pos = 0
while True:
    i = raw.find(b"\xc3\xb0", pos)
    if i < 0:
        break
    chunk = raw[i:i+12]
    print(f"C3B0 at {i}: {chunk.hex()} = {chunk.decode('utf-8', errors='replace')!r}")
    pos = i + 1

print()
# Also check the Ã§ issue
pat_ag = b"\xc3\x83\xc2\xa7"  # Ã§ double-encoded as UTF-8
cnt4 = raw.count(pat_ag)
print(f"Ã§ (C383 C2A7): {cnt4}")

# Simple Ã§ as 2-char UTF-8 sequence
pat_ag2 = "Ã§".encode("utf-8")  # = C3 83 C2 A7? no...
print(f"'Ã§' as utf-8 bytes: {pat_ag2.hex()}")
cnt5 = raw.count(pat_ag2)
print(f"Found: {cnt5}")

# What we want: is § already correct in context?
# § = U+00A7 = C2 A7 in UTF-8
# In context it's showing ASCII special chars, so § is correct
# The 'Ã' before it might be separate - let's check
sect = raw.find(b"\xc2\xa7")
if sect >= 0:
    print(f"Section sign § at {sect}: {raw[max(0,sect-5):sect+10].hex()}")
    print(f"Context: {raw[max(0,sect-15):sect+20].decode('utf-8', errors='replace')!r}")
