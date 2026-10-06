import sys, re
lines = open(sys.argv[1], encoding='latin-1').read().splitlines()
# Panel labels positions
for i,l in enumerate(lines):
    m = re.search(r"Helvetica bold\) 100\.0 0\.0 true true 0 \(([A-O])\)", l)
    if m:
        # find previous M line
        for j in range(i-1, i-4, -1):
            mm = re.match(r"^(-?\d+) (-?\d+) M$", lines[j])
            if mm:
                print("label", m.group(1), "at", mm.group(1), mm.group(2)); break
# Bars
bars = []
for i,l in enumerate(lines):
    m = re.search(r"C (\d\.\d+) (\d+) (\d+) (\d+) (\d+) BoxColFill", l)
    if m:
        bars.append((i, int(m.group(2)), int(m.group(3)), int(m.group(4)), int(m.group(5))))
print("n bars", len(bars))
for b in bars:
    print(b)
