import sys
sys.stdout.reconfigure(encoding='utf-8')

with open("D:/Claude/Proyectos/Tutorial-Passphrase/index.html", "rb") as f:
    raw = f.read()

# Key patterns to check
checks = {
    "arrow_right": ("c3a2c5bec593", "➜ U+279C"),
    "close_x":     ("c3a2c593c295", "✕ U+2715"),
    "hamburger":   ("c3a2c298c2b0", "☰ U+2630"),
    "box_double":  ("c3a2c295c290", "═ U+2550"),
    "box_single1": ("c3a2e2809de282ac", "─ U+2500 variant"),
    "a_bullet":    ("c3a2e280a2", "â• (check)"),
    "a_dagdag":    ("c3a2e280a0", "a-hat+dagger?"),
    "a_rdq":       ("c3a2e2809d", "a-hat+right-dbl-q"),
}

for name, (hex_pat, desc) in checks.items():
    pat = bytes.fromhex(hex_pat)
    cnt = raw.count(pat)
    if cnt > 0:
        idx = raw.find(pat)
        context = raw[max(0,idx-5):idx+len(pat)+5]
        print(f"{name} [{desc}]: {cnt}x")
        print(f"  hex ctx: {context.hex()}")
        print(f"  utf8 ctx: {context.decode('utf-8', errors='replace')!r}")
        print()

# Now understand c3a2e280a2:
# c3a2 = â (U+00E2), e280a2 = • (U+2022 bullet, VALID utf-8)
# So â• in the file - where does â come from?
# The bullet • was originally double-encoded as c3a2 e282ac c2a2
# After fix6, c3a2 e282ac c2a2 -> e280a2 (bullet)
# But BEFORE a bullet, was there another c3a2 that was part of a different sequence?
# If we have in the file: [c3a2 e282ac] [c3a2 e282ac c2a2]
# fix6 replaced the second triple -> e280a2
# leaving: [c3a2 e282ac] [e280a2]
# = "â€•" ... the first part "c3a2 e282ac" is now an orphaned â€ sequence!

# That's the problem! The box-drawing chars or other sequences had patterns
# that LEFT OVER c3a2 after fix6 consumed the next part.

# Let me check what c3a2e282ac looks like now (orphan â€)
orphan = bytes.fromhex("c3a2e282ac")
cnt_orphan = raw.count(orphan)
print(f"Orphan ae (c3a2e282ac): {cnt_orphan}x")
if cnt_orphan > 0:
    idx = raw.find(orphan)
    print(f"  context: {raw[max(0,idx-3):idx+15].decode('utf-8',errors='replace')!r}")
