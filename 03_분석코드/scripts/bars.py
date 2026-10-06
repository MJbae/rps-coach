import sys
from PIL import Image
im = Image.open(sys.argv[1]).convert('RGB')
W, H = im.size
px = im.load()
# middle row panels: y range roughly 140..230 in original
y_base_guess = int(sys.argv[2]) if len(sys.argv) > 2 else 228
def is_white(c): return c[0] > 225 and c[1] > 225 and c[2] > 225
def is_dark(c): return sum(c) < 200
# find baseline: the long dark horizontal axis line in y range 215..235
best = None
for y in range(205, 240):
    dark = sum(1 for x in range(W) if is_dark(px[x, y]))
    if best is None or dark > best[1]:
        best = (y, dark)
print("baseline row:", best)
yb = best[0]
# scan a row 3 px above baseline for colored (non-white, non-dark) runs
y = yb - 3
runs = []
x = 0
while x < W:
    c = px[x, y]
    if not is_white(c) and not is_dark(c):
        x0 = x
        while x < W and not is_white(px[x, y]) :
            x += 1
        runs.append((x0, x - 1))
    else:
        x += 1
runs = [r for r in runs if r[1] - r[0] >= 4]
print("bars found:", len(runs))
out = []
for (x0, x1) in runs:
    xs = x0 + 1  # near left edge inside bar, avoid central error bar
    # go up until white
    yy = y
    while yy > 100 and not is_white(px[xs, yy]):
        yy -= 1
    out.append((x0, x1, yy + 1))
for o in out:
    print(o)
