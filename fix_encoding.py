file = "D:/Claude/Proyectos/Tutorial-Passphrase/index.html"

with open(file, 'r', encoding='utf-8') as f:
    text = f.read()

fixes = [
    ('Â¿', '¿'),      # Â¿ → ¿
    ('â', '—'), # â€" → —
    ('Â ', ' '),            # Â  → space
    ('Ã', 'Ó'),       # Ã" → Ó
    ('Ã', 'É'),       # Ã‰ → É
    ('Ã', 'Ú'),       # Ãš → Ú
    ('Ã', 'Á'),       # Ã → Á
    ('Ã', 'Ñ'),       # Ã' → Ñ
    ('Ã³', 'ó'),       # Ã³ → ó
    ('Ã©', 'é'),       # Ã© → é
    ('Ã¡', 'á'),       # Ã¡ → á
    ('Ã­', 'í'),       # Ã­ → í
    ('Ãº', 'ú'),       # Ãº → ú
    ('Ã±', 'ñ'),       # Ã± → ñ
    ('Ã¼', 'ü'),       # Ã¼ → ü
    ('Ã', 'Í'),       # Ã → Í  (for Ícono)
    ('Ãcono', 'Ícono'),          # fallback for Ícono
    ('ð', '🔐'), # emoji lock
    ('ð·', '📷'), # emoji camera
    ('â°', '☰'),     # hamburger
    ('â', '✕'),     # X close
    ('â', '✓'),     # checkmark
    ('â ï¸', '⚠️'), # warning emoji
    ('â ', '⚠'),    # warning simple
    ('Â·', '·'),           # Â· → ·
    ('â', '’'),  # â€™ → '
    ('â', '“'),  # â€œ → "
    ('â', '”'),  # â€ → "
    ('Ã2', '×'),      # × for 5×5
    ('5Ã5', '5×5'),   # 5×5
    ('240Ã240', '240×240'), # 240×240
]

for bad, good in fixes:
    text = text.replace(bad, good)

with open(file, 'w', encoding='utf-8') as f:
    f.write(text)

import re
remaining = set(re.findall(r'[ÃÂ][-¿-]', text))
print("Remaining issues:", remaining if remaining else "NONE - all clean")
print("Done")
