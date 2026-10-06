import sys, re
lines = open(sys.argv[1], encoding='latin-1').read().splitlines()
start, end = int(sys.argv[2]), int(sys.argv[3])  # line range containing CR panels
y0 = 2030.0
scale = (2830.0 - 2030.0) / 0.6   # units per probability 1.0, from tick labels 0.2@2297,0.4@2564,0.6@2830
results = []  # list of (plotblock, bars[], errbars[])
cur = None
for i in range(start, end):
    l = lines[i]
    if '% Begin plot' in l:
        cur = {'bars': [], 'err': [], 'pos': None, 'in_err': False}
        results.append(cur)
        continue
    if cur is None: continue
    m = re.search(r"C (\d\.\d+) (\d+) (\d+) (\d+) (\d+) BoxColFill", l)
    if m:
        x, y, w, h = map(int, m.groups()[1:])
        cur['bars'].append((x, h - 1))  # outline height = fill height - 1
        continue
    if l.startswith('PL LCb setrgbcolor'):
        cur['in_err'] = True; continue
    if cur['in_err']:
        mm = re.match(r"^(-?\d+) (-?\d+) (M|R|V)$", l)
        if mm:
            a, b, op = int(mm.group(1)), int(mm.group(2)), mm.group(3)
            if op == 'M':
                cur['pos'] = (a, b)
            elif op == 'R':
                cur['pos'] = (cur['pos'][0] + a, cur['pos'][1] + b)
            elif op == 'V':
                p0 = cur['pos']; p1 = (p0[0] + a, p0[1] + b)
                if a == 0 and b != 0:
                    cur['err'].append((p0[0], min(p0[1], p1[1]), max(p0[1], p1[1])))
                cur['pos'] = p1
        if '% End plot' in l:
            cur['in_err'] = False
panels = ['F (a=1.1)', 'G (a=2)', 'H (a=4)', 'I (a=9)', 'J (a=100)']
names = ['W', 'T', 'L']
sub = ['-', '0', '+']
for k, blk in enumerate(results):
    p = panels[k // 3]; o = names[k % 3]
    row = []
    for j, (x, h) in enumerate(blk['bars']):
        mean = h / scale
        if j < len(blk['err']):
            ex, lo, hi = blk['err'][j]
            sem = (hi - lo) / 2.0 / scale
            mid = ((hi + lo) / 2.0 - y0) / scale
        else:
            sem = float('nan'); mid = float('nan')
        row.append(f"{o}{sub[j]}={mean:.3f}(SEM {sem:.3f}; errbar-mid {mid:.3f})")
    tot = sum(h for _, h in blk['bars']) / scale
    print(p, ' '.join(row), f"sum={tot:.3f}")
