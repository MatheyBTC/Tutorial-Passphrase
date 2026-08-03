with open("D:/Claude/Proyectos/Tutorial-Passphrase/index.html", "rb") as f:
    raw = f.read()

# Find the 'a-hat euro' pattern bytes
# 'a' with circumflex = U+00E2 -> UTF-8: C3 A2
# 'euro' U+20AC -> UTF-8: E2 82 AC
pattern = b"\xc3\xa2\xe2\x82\xac"
count = raw.count(pattern)
print(f"Found 'ae' pattern (C3A2 E28AAC): {count} times")
if count > 0:
    idx = raw.find(pattern)
    print(f"At byte {idx}: {raw[idx:idx+12].hex()}")
    print(f"Surrounding: {raw[max(0,idx-5):idx+15]}")

# What follows the ae pattern?
if count > 0:
    results = {}
    pos = 0
    while True:
        idx = raw.find(pattern, pos)
        if idx < 0:
            break
        next_bytes = raw[idx+5:idx+8].hex()
        results[next_bytes] = results.get(next_bytes, 0) + 1
        pos = idx + 1
    print("What follows ae pattern:")
    for k, v in sorted(results.items(), key=lambda x: -x[1]):
        print(f"  {k}: {v} times")
        # Try to decode
        try:
            val = bytes.fromhex(k).decode("utf-8")
            print(f"    = {repr(val)}")
        except Exception:
            print(f"    = (not valid utf-8)")

# Also check what 'ae' + next 3 bytes should map to
# The original chars in CP1252 after 'a'(E2) and 'euro'(80) would be:
# 0x93 = ' (left double quote), 0x94 = ' (right double quote), 0x96 = - (en-dash), 0x97 = - (em-dash)
# Actually in CP1252: 0x80 = euro, 0x93 = left-quote, 0x94 = right-quote, 0x96 = en-dash, 0x97 = em-dash
# Wait, that's wrong. Let me reconsider.
# Original UTF-8 U+2014 (em-dash) = E2 80 94
# Read as CP1252: E2=a-circumflex, 80=euro, 94=right-double-quote (U+201D)
# right-double-quote U+201D in UTF-8 = E2 80 9D
# So double-encoded em-dash = C3A2 + E282AC + E2809D

print()
# Check specifically for em-dash double-encoding
em_dash_bad = bytes.fromhex("c3a2e282ace2809d")  # ae + right-double-quote
print(f"Testing em-dash bad sequence {em_dash_bad.hex()}: {raw.count(em_dash_bad)}")

# right single quote (curly ') CP1252: 0x92 -> U+2018 -> E2 80 98...
# actually 0x92 in CP1252 = U+2019 (right single quote) -> E2 80 99
right_sq_bad = bytes.fromhex("c3a2e282ace2809c")  # ae + left-double-quote U+201C
right_sq_bad2 = bytes.fromhex("c3a2e282ace28099")  # ae + right-single U+2019
print(f"Left double quote bad: {raw.count(right_sq_bad)}")
print(f"Right single quote bad: {raw.count(right_sq_bad2)}")

# Try all combinations
for next_hex in ["e28094", "e2809d", "e2809c", "e28099", "e28093", "e280a2", "e28098"]:
    bad = bytes.fromhex("c3a2e282ac" + next_hex)
    cnt = raw.count(bad)
    if cnt > 0:
        val = bytes.fromhex(next_hex).decode("utf-8")
        print(f"  ae+{next_hex} -> {repr(val)}: {cnt} times")
