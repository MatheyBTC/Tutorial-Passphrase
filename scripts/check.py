import re

with open("D:/Claude/Proyectos/Tutorial-Passphrase/index.html", "r", encoding="utf-8") as f:
    text = f.read()

bad = re.findall(r"[ÃÂ][^a-zA-Z\s<>\"'(){};,.\-_/\\0-9\n\r\t]", text)
print("Remaining patterns:", len(bad), sorted(set(bad)))
for b in sorted(set(bad)):
    idx = text.find(b)
    print(repr(text[max(0,idx-40):idx+60]))
    print()

# Check for em-dash patterns
bad2 = text.count("â€")
print("'a with hat+euro' sequences:", bad2)

# Verify inverted question marks are in right places
for m in re.finditer("\xbf", text):
    print("  pos", m.start(), repr(text[max(0,m.start()-10):m.start()+20]))
