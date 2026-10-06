import sys
sys.path.insert(0, sys.argv[1])
import openpyxl
from collections import defaultdict, Counter
UP = {'R': 'P', 'P': 'S', 'S': 'R'}
BEATS = {'R': 'S', 'P': 'R', 'S': 'P'}
def outcome(a, b):
    if a == b: return 'tie'
    return 'win' if BEATS[a] == b else 'loss'
pairs = []
for path in sys.argv[2:]:
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    for ws in wb.worksheets:
        rws = list(ws.iter_rows(values_only=True))
        hi = next(i for i, r in enumerate(rws) if r[0] and isinstance(r[0], str) and 'Round number' in r[0])
        mcol = next(j for j, h in enumerate(rws[hi]) if h and 'Multi AI played' in str(h))
        data = [r for r in rws[hi+1:] if isinstance(r[0], (int, float))]
        pairs.append(([str(r[1]).strip() for r in data], [str(r[mcol]).strip() for r in data]))
for lo, hi in ((1, 20), (1, 50), (51, 300)):
    cnt = defaultdict(Counter)
    for P, Q in pairs:
        for t in range(lo-1, min(hi, len(P))-1):
            o = outcome(P[t], Q[t]); s = 'stay' if P[t+1] == P[t] else ('up' if P[t+1] == UP[P[t]] else 'down')
            cnt[o][s] += 1
    print(f"WangL rounds {lo}-{hi}: " + ' | '.join(f"{o}: stay {cnt[o]['stay']/sum(cnt[o].values()):.3f} up {cnt[o]['up']/sum(cnt[o].values()):.3f} down {cnt[o]['down']/sum(cnt[o].values()):.3f} (n={sum(cnt[o].values())})" for o in ('win','tie','loss')))
