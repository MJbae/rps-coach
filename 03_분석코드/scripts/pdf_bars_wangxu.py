import sys, re
sys.path.insert(0, '/private/tmp/claude-501/-Users-baemanjin-orca-projects-----/9282a235-4fc4-4c50-add0-37a1d5aaa853/scratchpad/pylib')
from pypdf import PdfReader
for path in sys.argv[1:]:
    data = PdfReader(path).pages[0].get_contents().get_data().decode('latin-1')
    # y ticks: short horizontal segments starting at the left axis x=935.832
    yt = sorted(set(float(m.group(1)) for m in re.finditer(r'935\.832 (-?[\d.]+) m\s+99[01][\d.]* \1 l', data)))
    labels = [float(x) for x in re.findall(r'\((\d(?:\.\d+)?)\)Tj', data)]
    rects = [tuple(map(float, x)) for x in re.findall(r'(-?[\d.]+) (-?[\d.]+) (-?[\d.]+) (-?[\d.]+) re', data)]
    print(path.split('/')[-1], 'yticks', yt)
    # assume baseline 475 -> 0 and top 3995.83 -> ? ; infer from ticks
    if len(yt) >= 2:
        unit = (yt[-1] - yt[0])
    print('  rect count', len(rects))
    aval = ['1', '1.1', '2', '4', '9', '100', 'inf']
    # group by x position: bars at x0 + k*697.5 + j*155
    out = {}
    for (x, y, w, h) in rects:
        k = round((x - 1400) / 697.5) if x < 1555 or True else None
        # determine which of 3 sticks: offset
        base = 1400 + round((x - 1400) / 697.5 - 0.0) * 697.5
        out.setdefault(round((x - 1400) // 697.5), []).append((x, h))
    for k in sorted(out):
        sticks = sorted(out[k])
        print('  a=', aval[int(k)] if 0 <= k < 7 else k, ['%.3f' % (h / 3520.83) for _, h in sticks])
