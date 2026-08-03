import sys

file = "D:/Claude/Proyectos/Tutorial-Passphrase/index.html"

# Read raw bytes
with open(file, "rb") as f:
    raw = f.read()

print(f"File size: {len(raw)} bytes")

# The file is UTF-8 but some sections have DOUBLE-ENCODED chars.
# Double encoding: original UTF-8 bytes were read as Latin-1, then re-encoded as UTF-8.
# Example: 'o' with accent = C3 B3 in UTF-8
# If read as latin-1: gives 'Ã' (U+00C3) + 'o' (U+00B3)
# Then re-encoded as UTF-8: 'Ã'->C3 83, 'o'->C2 B3
# So double-encoded 'o-accent' = C3 83 C2 B3 in the file bytes
#
# Strategy: replace all double-encoded sequences with their single-encoded equivalents

# Build the replacement table (bad_bytes -> good_bytes)
replacements = []

# All UTF-8 2-byte sequences (U+0080 to U+07FF) that could be mojibaked
# When a byte sequence [0xCx, 0xYY] (valid UTF-8) gets re-encoded:
# 0xCx as a unicode char -> in latin-1 it's 'Ã' or similar -> UTF-8: C3 (8x or Cx)
# 0xYY as a unicode char -> in latin-1 it's some char -> UTF-8 varies

# Specific known mojibake patterns (latin-1 repr -> correct UTF-8 bytes)
# Format: (bad_bytes_hex, good_bytes_hex)
mojibake_pairs = [
    # Lowercase accented letters
    ("c3b3", "c3b3"),  # ó (already correct) - skip
    # The ACTUAL mojibake patterns (double-encoded):
    # Ã³ (U+00C3 U+00B3) encoded as UTF-8 = C3 83 C2 B3
    ("c383c2b3", "c3b3"),  # Ã³ -> ó
    ("c383c2a9", "c3a9"),  # Ã© -> é
    ("c383c2a1", "c3a1"),  # Ã¡ -> á
    ("c383c2ad", "c3ad"),  # Ã­ -> í
    ("c383c2ba", "c3ba"),  # Ãº -> ú
    ("c383c2b1", "c3b1"),  # Ã± -> ñ
    ("c383c2bc", "c3bc"),  # Ã¼ -> ü
    ("c383e2809c", "e2809c"),  # Ã" followed by... no wait
    # Capital letters
    ("c383c293", "c393"),  # Ã" -> Ó (U+00D3)
    ("c383c289", "c389"),  # Ã‰ -> É (U+00C9)
    ("c383c29a", "c39a"),  # Ãš -> Ú (U+00DA)
    ("c383c281", "c381"),  # Ã -> Á (U+00C1)
    ("c383c291", "c391"),  # Ã' -> Ñ (U+00D1)
    ("c383c28d", "c38d"),  # Ã -> Í (U+00CD)
    # Â sequences -> single byte
    ("c382c2bf", "c2bf"),  # Â¿ -> ¿ (U+00BF)
    ("c382c2a1", "c2a1"),  # Â¡ -> ¡ (U+00A1)
    ("c382c2b7", "c2b7"),  # Â· -> · (U+00B7)
    ("c382c2a0", "c2a0"),  # Â  -> nbsp
    # em-dash: U+2014 = E2 80 94 in UTF-8
    # mojibaked: â=U+00E2->C3A2, €=U+0080->C280, "=U+0094->C294
    ("c3a2e2809e", "e28094"),  # approximation... need to check
    # Let's do em-dash properly:
    # â€" = U+00E2 U+20AC U+201C ... no
    # â€" in latin-1: â=0xE2, €=0x80, "=0x94
    # As UTF-8 chars: 0xE2->C3A2, 0x80->C280, 0x94->C294
    ("c3a2c280c294", "e28094"),  # â€" -> —
    # right single quote U+2019 = E2 80 99
    ("c3a2c280c299", "e28099"),  # â€™ -> '
    # left double quote U+201C = E2 80 9C
    ("c3a2c280c29c", "e2809c"),  # â€œ -> "
    # right double quote U+201D = E2 80 9D
    ("c3a2c280c29d", "e2809d"),  # â€ -> "
    # bullet U+2022 = E2 80 A2
    ("c3a2c280c2a2", "e280a2"),  # â€¢ -> •
    # ☰ U+2630 = E2 98 B0
    ("c3a2c298c2b0", "e298b0"),  # â˜° -> ☰
    # ✕ U+2715 = E2 9C 95
    ("c3a2c29cc295", "e29c95"),  # âœ• -> ✕
    # ✓ U+2713 = E2 9C 93
    ("c3a2c29cc293", "e29c93"),  # âœ" -> ✓
    # 🔐 U+1F510 = F0 9F 94 90
    # mojibaked: ð=0xF0->C3B0, Ÿ=0x9F->C29F, "=0x94->C294, =0x90->C290
    ("c3b0c29fc294c290", "f09f9490"),  # ð -> 🔐
    # 📷 U+1F4F7 = F0 9F 93 B7
    ("c3b0c29fc293c2b7", "f09f93b7"),  # 📷
]

data = raw
count_total = 0
for bad_hex, good_hex in mojibake_pairs:
    if bad_hex == good_hex:
        continue
    bad = bytes.fromhex(bad_hex)
    good = bytes.fromhex(good_hex)
    count = data.count(bad)
    if count > 0:
        print(f"Replacing {bad_hex} -> {good_hex}: {count}x")
        data = data.replace(bad, good)
        count_total += count

print(f"\nTotal replacements: {count_total}")
print(f"New size: {len(data)} bytes")

# Verify no remaining C3 83 sequences
remaining = data.count(b"\xc3\x83")
print(f"Remaining C3 83 (Ã) sequences: {remaining}")
if remaining > 0:
    idx = data.find(b"\xc3\x83")
    print(f"First at byte {idx}: ...{data[max(0,idx-10):idx+20].hex()}...")

# Save
with open(file, "wb") as f:
    f.write(data)
print("Saved!")

# Verify it reads back as valid UTF-8
with open(file, "r", encoding="utf-8") as f:
    text = f.read()
print(f"UTF-8 read OK, {len(text)} chars")

# Show a sample of Configuracion
import re
matches = [(m.start(), m.group()) for m in re.finditer(r'Configuraci.n', text)]
print(f"'Configuraci?n' samples: {matches[:5]}")
