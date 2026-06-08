import sys
sys.stdout.reconfigure(encoding='utf-8')

with open("D:/Claude/Proyectos/Tutorial-Passphrase/index.html", "rb") as f:
    raw = f.read()

# Show context for each unique pattern
patterns = [
    b"\xc3\xa2\xe2\x80\xa2",  # a-hat + bullet
    b"\xc3\xa2\xe2\x80\x9d",  # a-hat + right-dbl-quote (used in em-dash?)
    b"\xc3\xa2\xe2\x80\xa0",  # a-hat + dagger?
    b"\xc3\xa2\xc5\xbe\xc5\x93",  # azebc -> should be arrow ➜
    b"\xc3\xa2\xc5\xa1\xc2\xa0",  # another pattern
]

for pat in patterns:
    idx = raw.find(pat)
    if idx >= 0:
        chunk = raw[max(0,idx-3):idx+12]
        print(f"Pattern {pat.hex()}:")
        try:
            print(f"  context bytes: {chunk.hex()}")
            print(f"  as utf8: {chunk.decode('utf-8', errors='replace')!r}")
        except Exception as e:
            print(f"  error: {e}")

        # Decode the pattern itself treating as double-encoded:
        # Each byte of the ORIGINAL sequence was double-encoded
        # Original: what single char/sequence do these represent?
        # c3a2 = U+00E2 (â), byte 0xE2
        # e280a2 = U+2022 (bullet •)
        # But 0xE2 followed by... if these were originally UTF-8 bytes:
        # 0xE2 is the start of a 3-byte UTF-8 sequence
        # The next 2 bytes when read as CP1252 chars become the following chars
        print()

# Show what the box-drawing comment looks like
idx = raw.find(b"â\x94\x80")  # might not be there
# Let's try the comment markers
for marker in [b"//", b"DATA", b"LANG", b"SECTIONS"]:
    idx = raw.find(marker)
    if idx >= 0:
        chunk = raw[max(0,idx-20):idx+50]
        print(f"Near '{marker}': {chunk.decode('utf-8', errors='replace')!r}")
        break

# Check specifically the ➜ arrow case
# ➜ = U+279C = E2 9E 9C
# Double-encoded: E2->C3A2, 9E->CP1252: ž=U+017E=C5BE, 9C->CP1252: œ=U+0153=C593
pat_arrow = bytes.fromhex("c3a2c5bec593")
cnt = raw.count(pat_arrow)
print(f"\nArrow ➜ pattern (c3a2c5bec593): {cnt}x")

# ✕ = U+2715 = E2 9C 95
# Double-encoded: E2->C3A2, 9C->CP1252: œ=U+0153=C5 93, 95->CP1252: U+0095=C2 95
pat_x = bytes.fromhex("c3a2c593c295")
cnt2 = raw.count(pat_x)
print(f"Close X ✕ pattern (c3a2c593c295): {cnt2}x")

# ☰ = U+2630 = E2 98 B0
# Double-encoded: E2->C3A2, 98->CP1252: U+0098=C2 98, B0->CP1252: °=U+00B0=C2 B0
pat_hamb = bytes.fromhex("c3a2c298c2b0")
cnt3 = raw.count(pat_hamb)
print(f"Hamburger ☰ pattern (c3a2c298c2b0): {cnt3}x")

# ═ = U+2550 = E2 95 90
# ─ = U+2500 = E2 94 80
# These box drawing chars in comments
# U+2550: E2->C3A2, 95->C295, 90->C290
pat_box1 = bytes.fromhex("c3a2c295c290")
cnt4 = raw.count(pat_box1)
print(f"Box = (c3a2c295c290): {cnt4}x")

# U+2500: E2->C3A2, 94->CP1252: right-dbl-quote U+201D=E2809D (now fixed to E28094=em-dash)
# After fix6: the em-dash E2 80 94 would be there
# So ─ double-encoded after fix6 = C3A2 E28094 C280
pat_box2 = bytes.fromhex("c3a2e28094c280")
cnt5 = raw.count(pat_box2)
print(f"Box - after em-dash fix (c3a2e28094c280): {cnt5}x")

# U+2500 originally: E2 94 80
# 94 in CP1252 = right-double-quote U+201D, but wait...
# Actually I need to re-examine: the em-dash I fixed was E2 80 94 (3 bytes),
# but U+2500 = E2 94 80 (different byte order!)
# 94 in CP1252 = " (right double quote U+201D)
# 80 in CP1252 = euro € (U+20AC)
# So U+2500 double-encoded = C3A2 + (94->CP1252->U+201D->E2809D) + (80->CP1252->U+20AC->E282AC)
# = C3A2 E2809D E282AC
# But fix6 converted E2809D -> E28094 (only when preceded by C3A2 E282AC)
# So the standalone E2809D in C3A2 E2809D E282AC was NOT changed by fix6!
# But wait, was C3A2 E2809D a different order? Let me check
pat_box3 = bytes.fromhex("c3a2e2809de282ac")
cnt6 = raw.count(pat_box3)
print(f"Box - U+2500: {cnt6}x")
