import sys, math
sys.path.insert(0, sys.argv[1])
import openpyxl
from collections import Counter, defaultdict
UP = {'R': 'P', 'P': 'S', 'S': 'R'}
BEATS = {'R': 'S', 'P': 'R', 'S': 'P'}
def outcome(a, b):
    if a == b: return 'tie'
    return 'win' if BEATS[a] == b else 'loss'
def mean(xs): return sum(xs)/len(xs)
def sd(xs):
    m = mean(xs); return math.sqrt(sum((x-m)**2 for x in xs)/(len(xs)-1))
def sem(xs): return sd(xs)/math.sqrt(len(xs))
results = []
per = defaultdict(list); marg = Counter(); nm = 0
for path in sys.argv[2:]:
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    for ws in wb.worksheets:
        rows = list(ws.iter_rows(values_only=True))
        # find header row
        hi = next(i for i, r in enumerate(rows) if r[0] and isinstance(r[0], str) and 'Round number' in r[0])
        header = rows[hi]
        mcol = next(j for j, h in enumerate(header) if h and 'Multi AI played' in str(h))
        data = [r for r in rows[hi+1:] if isinstance(r[0], (int, float))]
        seq = [(str(r[1]).strip(), str(r[mcol]).strip()) for r in data]
        seq = [(h, a) for h, a in seq if h in UP and a in UP]
        w = sum(1 for h, a in seq if outcome(a, h) == 'win')
        l = sum(1 for h, a in seq if outcome(a, h) == 'loss')
        results.append((path.split('_')[-2], ws.title, len(seq), w, l, w - l))
        for h, a in seq: marg[h] += 1; nm += 1
        cnt = defaultdict(Counter)
        for t in range(len(seq) - 1):
            (h0, a0), (h1, a1) = seq[t], seq[t+1]
            o = outcome(h0, a0)
            s = 'stay' if h1 == h0 else ('up' if h1 == UP[h0] else 'down')
            cnt[o][s] += 1
        for o in ('win', 'tie', 'loss'):
            n = sum(cnt[o].values())
            if n == 0: continue
            for s in ('stay', 'up', 'down'):
                per[(o, s)].append(cnt[o][s] / n)
print('players:', len(results), 'rounds per player:', Counter(r[2] for r in results))
for grp in ('MOESM1', 'MOESM2'):
    nets = [r[5] for r in results if r[0] == grp]
    print(grp, 'n', len(nets), 'AI net mean', round(mean(nets), 2), 'sd', round(sd(nets), 2))
nets = [r[5] for r in results]
W = sum(r[3] for r in results); L = sum(r[4] for r in results); N = sum(r[2] for r in results)
print('overall AI net mean', round(mean(nets), 2), 'AI win rate', round(W/N, 4), 'loss rate', round(L/N, 4), 'AI ahead', sum(1 for x in nets if x > 0), 'tied', sum(1 for x in nets if x == 0))
print('max AI net:', max(results, key=lambda r: r[5]))
print('human marginals', {k: round(v/nm, 3) for k, v in marg.items()})
for o in ('win', 'tie', 'loss'):
    print('human after', o, {s: (round(mean(per[(o, s)]), 3), round(sem(per[(o, s)]), 3), len(per[(o, s)])) for s in ('stay', 'up', 'down')})
import statistics
nets_all = [r[5] for r in results]
print('median AI net', statistics.median(nets_all))
ex = [r[5] for r in results if not (r[0] == 'MOESM1' and r[1] == 'Player 20')]
print('mean excluding P20', round(mean(ex), 2), 'n', len(ex))
W2 = sum(r[3] for r in results if not (r[0]=='MOESM1' and r[1]=='Player 20')); L2 = sum(r[4] for r in results if not (r[0]=='MOESM1' and r[1]=='Player 20')); N2 = sum(r[2] for r in results if not (r[0]=='MOESM1' and r[1]=='Player 20'))
print('excl P20 win', round(W2/N2,4), 'loss', round(L2/N2,4))
print('sorted nets', sorted(nets_all))
