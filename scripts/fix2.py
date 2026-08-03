import re

file = "D:/Claude/Proyectos/Tutorial-Passphrase/index.html"
with open(file, "r", encoding="utf-8") as f:
    text = f.read()

orig_len = len(text)

# Mojibake: UTF-8 bytes read as Latin-1 then re-encoded to UTF-8
# Approach: encode each corrupt sequence back to latin-1 bytes, then decode as utf-8
def fix_mojibake(t):
    try:
        return t.encode("latin-1").decode("utf-8")
    except Exception:
        return t

# We'll do targeted replacements using the actual characters
# Using ord() values to avoid any encoding issues in this source file

bad_good = [
    # 2-byte Latin sequences
    ("\xc3\xa3".encode().decode(), "\xe3"),    # skip
    ("\xc3\xb3", "\xf3"),   # Ã³ -> ó
    ("\xc3\xa9", "\xe9"),   # Ã© -> é
    ("\xc3\xa1", "\xe1"),   # Ã¡ -> á
    ("\xc3\xad", "\xed"),   # Ã­ -> í
    ("\xc3\xba", "\xfa"),   # Ãº -> ú
    ("\xc3\xb1", "\xf1"),   # Ã± -> ñ
    ("\xc3\xbc", "\xfc"),   # Ã¼ -> ü
    ("\xc3\x93", "\xd3"),   # Ã" -> Ó
    ("\xc3\x89", "\xc9"),   # Ã‰ -> É
    ("\xc3\x9a", "\xda"),   # Ãš -> Ú
    ("\xc3\x81", "\xc1"),   # Ã -> Á
    ("\xc3\x91", "\xd1"),   # Ã' -> Ñ
    ("\xc3\x8d", "\xcd"),   # Ã -> Í
    ("\xc2\xbf", "\xbf"),   # Â¿ -> ¿
    ("\xc2\xa1", "\xa1"),   # Â¡ -> ¡
    ("\xc2\xb7", "\xb7"),   # Â· -> ·
    ("\xc2\xa0", "\xa0"),   # Â  -> nbsp
]

# Build actual replacement strings
fixes = []
for bad_bytes_str, good_byte_str in bad_good:
    # bad_bytes_str contains mojibake chars already in unicode
    # good_byte_str is the correct unicode char encoded as a byte
    bad = bad_bytes_str.encode("latin-1").decode("utf-8") if False else bad_bytes_str
    good = good_byte_str.encode("latin-1").decode("utf-8")
    fixes.append((bad, good))

# Multi-byte sequences for em-dash, quotes, etc.
# \xe2\x80\x94 = em-dash —, misread as â€" in latin-1
em_dash_bad = "\xe2\x80\x94".encode("latin-1").decode("utf-8")  # this won't work directly
# Let me try a different approach - just match on the actual characters in the file

# Read the file as bytes then decode as latin-1 to see what's there
with open(file, "rb") as f:
    raw = f.read()

# The file might be double-encoded. Let's detect and fix
# Try: if file contains Ã (U+00C3) followed by a latin char, it's mojibake
# Re-encode the problematic chars back to bytes as latin-1, then decode as utf-8

# Find all Ã sequences
result = []
i = 0
fixed_count = 0
while i < len(raw):
    # Check for mojibake pattern: 0xC3 followed by 0x80-0xBF
    # or 0xC2 followed by 0x80-0xBF
    if i + 1 < len(raw) and raw[i] in (0xC3, 0xC2) and 0x80 <= raw[i+1] <= 0xBF:
        # This could be mojibake: the original UTF-8 byte 0xC3/0xC2 was stored as a 2-byte UTF-8 sequence
        # But we need to check if this is already valid UTF-8 or mojibake
        # In valid UTF-8: 0xC3 0xA9 = é (valid)
        # In mojibake: 0xC3 0x83 0xC2 0xA9 would be Ã© (mojibake for é)
        pass
    result.append(raw[i])
    i += 1

# Better approach: decode as latin-1, fix known patterns, re-encode
text_latin1 = raw.decode("latin-1")

# All the mojibake patterns when the file is read as latin-1
# (file was UTF-8, got read as latin-1, then re-saved as UTF-8 of those latin-1 chars)
FIXES_L1 = [
    ("Ã³", "ó"),
    ("Ã©", "é"),
    ("Ã¡", "á"),
    ("Ã­", "í"),
    ("Ãº", "ú"),
    ("Ã±", "ñ"),
    ("Ã¼", "ü"),
    ("Ã\"", "Ó"),
    ("Ã‰", "É"),
    ("Ãš", "Ú"),
    ("Ã", "Á"),
    ("Ã'", "Ñ"),
    ("Ã", "Í"),
    ("Â¿", "¿"),
    ("Â¡", "¡"),
    ("Â·", "·"),
    ("â€"", "—"),
    ("â€™", "’"),
    ("â€œ", "“"),
    ("â€\x9d", "”"),
    ("â€¢", "•"),
    ("â˜°", "☰"),
    ("âœ•", "✕"),
    ("âœ"", "✓"),
    ("â ï¸", "⚠️"),
    ("ðŸ"", "🔐"),
    ("ðŸ"·", "📷"),
    ("Â ", " "),
]

for bad, good in FIXES_L1:
    count = text_latin1.count(bad)
    if count > 0:
        print(f"Fixed {count}x: {repr(bad)} -> {repr(good)}")
        text_latin1 = text_latin1.replace(bad, good)

# Now re-encode the fixed text as UTF-8
# The fixed text_latin1 should now have proper unicode chars
# But we need to remove any stray Â or Ã chars that might remain as artifacts
# Let's check what remains
remaining = re.findall(r"[ÃÂ][^\s<>\"'(){};,.]", text_latin1)
if remaining:
    print(f"\nStill has {len(remaining)} potential issues:")
    for r in sorted(set(remaining))[:20]:
        idx = text_latin1.find(r)
        print(f"  {repr(r)}: ...{repr(text_latin1[max(0,idx-15):idx+25])}...")

# Save back as UTF-8
out_bytes = text_latin1.encode("utf-8")
# But wait - the file currently has valid UTF-8 for the already-correct chars
# and double-encoded UTF-8 for the mojibake chars
# Reading as latin-1 means the correct UTF-8 sequences will ALSO be there as latin-1 sequences
# So we can safely re-encode to UTF-8

# Actually this approach will BREAK existing correct UTF-8 chars
# because reading UTF-8 as latin-1 gives us the raw bytes interpreted as latin-1 chars
# then encoding back as UTF-8 gives us the same bytes back

# So the flow is:
# CORRECT: file has 0xC3 0xA9 (valid UTF-8 for é)
#   -> read as latin-1: gives us "Ã©" (two chars: 0xC3, 0xA9)
#   -> we replace "Ã©" with "é"
#   -> "é" encodes to UTF-8 as 0xC3 0xA9 -> SAME! OK.
#
# MOJIBAKE: file has 0xC3 0x83 0xC2 0xA9 (double-encoded)
#   -> read as latin-1: gives us "Ã©" (but from double-encoded bytes: Ã=0xC3,ƒ=0x83,Â=0xC2,©=0xA9)
#   Hmm, this is 4 bytes: 0xC3 0x83 0xC2 0xA9
#   As latin-1: Ã + \x83 + Â + ©
#   But \x83 is not a printable latin-1 char...

# Let me just check what's actually in the file
print("\n--- Checking actual bytes in file ---")
# Find "Configuraci" and show surrounding bytes
idx = raw.find(b"Configuraci")
if idx >= 0:
    chunk = raw[idx:idx+20]
    print(f"'Configuraci...' bytes: {chunk.hex()}")
    print(f"As latin-1: {chunk.decode('latin-1')}")
    print(f"As utf-8 (ignore errors): {chunk.decode('utf-8', errors='replace')}")

# Find a known mojibake pattern
idx = raw.find(b"Ã")
if idx < 0:
    idx = raw.find("Ã".encode("utf-8"))
print(f"\nSearching for Ã (UTF-8 0xC3 0x83)...")
target = "Ã".encode("utf-8")  # = 0xC3 0x83
idx = raw.find(target)
if idx >= 0:
    print(f"Found at byte {idx}: {raw[idx-5:idx+15].hex()}")
    print(f"Context: {repr(raw[idx-5:idx+15].decode('utf-8', errors='replace'))}")
else:
    print("Not found as UTF-8 encoded Ã")
