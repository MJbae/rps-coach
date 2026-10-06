import sys, statistics as st
sys.path.insert(0, '/private/tmp/claude-501/-Users-baemanjin-orca-projects-----/9282a235-4fc4-4c50-add0-37a1d5aaa853/scratchpad/pylib')
import xlrd
sh = xlrd.open_workbook(sys.argv[1]).sheet_by_index(0)
# header rows
for r in range(0, 5):
    print('ROW', r, [(c, sh.cell_value(r, c)) for c in range(sh.ncols) if str(sh.cell_value(r, c)).strip() != ''])
# data rows: find rows whose col0 is numeric
data_rows = [r for r in range(5, sh.nrows) if isinstance(sh.cell_value(r, 0), float) and sh.cell_value(r, 0) != '']
print('data rows', data_rows[0], '..', data_rows[-1], 'n=', len(data_rows))
for r in range(data_rows[-1] + 1, sh.nrows):
    print('TAIL ROW', r, [(c, sh.cell_value(r, c)) for c in range(sh.ncols) if str(sh.cell_value(r, c)).strip() != ''])
def col(c):
    return [sh.cell_value(r, c) for r in data_rows if sh.cell_value(r, c) != '']
def ms(c):
    v = col(c); return st.mean(v), st.stdev(v) / len(v) ** 0.5, len(v)
print('Item n: R,P,S', [round(ms(c)[0], 4) for c in (1, 2, 3)])
print('Outcome n (cols 6,7,8 =', [sh.cell_value(4, c) for c in (6, 7, 8)], ')', [round(ms(c)[0], 4) for c in (6, 7, 8)])
items = ['ROCK', 'PAPER', 'SCISSORS']
cells = {}
for i, it in enumerate(items):
    for j in range(3):
        oc = sh.cell_value(3, 12 + i * 9 + j * 3)
        for k in range(3):
            c = 12 + i * 9 + j * 3 + k
            strat = sh.cell_value(4, c)
            m, se, n = ms(c)
            cells[(it, oc, strat)] = (m, se, n)
            print(f"{it:9s} {oc:5s} {strat:5s} col{c} mean={m:.3f} sem={se:.3f} n={n}")
print('--- outcome-level (mean over the 3 item cells, per participant then averaged) ---')
for oc in ('WIN', 'LOSE', 'DRAW'):
    out = []
    for strat in ('STAY', 'UP', 'DOWN'):
        cs = [12 + i * 9 + j * 3 + k for i in range(3) for j in range(3) for k in range(3)
              if sh.cell_value(3, 12 + i * 9 + j * 3) == oc and sh.cell_value(4, 12 + i * 9 + j * 3 + k) == strat]
        per = []
        for r in data_rows:
            vals = [sh.cell_value(r, c) for c in cs if sh.cell_value(r, c) != '']
            if vals: per.append(st.mean(vals))
        out.append(f"{strat}={st.mean(per):.3f} (sem {st.stdev(per)/len(per)**0.5:.3f}, n={len(per)})")
    print(oc, ' '.join(out))
print('--- second-order: strategy n+1 x n+2 ---')
for b, s1 in enumerate(('STAY', 'UP', 'DOWN')):
    row = []
    for k, s2 in enumerate(('STAY', 'UP', 'DOWN')):
        c = 41 + b * 3 + k
        m, se, n = ms(c)
        row.append(f"{sh.cell_value(4, c)}={m:.3f}(sem {se:.3f})")
    print('n+1', sh.cell_value(3, 41 + b * 3), '->', ' '.join(row))
