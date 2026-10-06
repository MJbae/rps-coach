import csv, sys, glob, os
from collections import Counter, defaultdict
N = {'1': 'R', '2': 'P', '3': 'S'}
BEATS = {'R': 'S', 'P': 'R', 'S': 'P'}
def outcome(a, b):
    if a == b: return 'tie'
    return 'win' if BEATS[a] == b else 'loss'
pooled = defaultdict(Counter)
perplayer = defaultdict(list)
for f in sorted(glob.glob(os.path.join(sys.argv[1], '*_events.tsv'))):
    rr = list(csv.DictReader(open(f), delimiter='\t'))
    a = [N.get(r['player1_resp']) for r in rr]; b = [N.get(r['player2_resp']) for r in rr]
    for P, Q in ((a, b), (b, a)):
        c = defaultdict(Counter)
        for t in range(len(P)-1):
            if P[t] and Q[t] and P[t+1]:
                c[(outcome(P[t], Q[t]), P[t])][P[t+1]] += 1
        for k, v in c.items():
            pooled[k].update(v)
            n = sum(v.values())
            perplayer[k].append({h: v[h]/n for h in 'RPS'})
for k in [('win','R'), ('win','P'), ('win','S'), ('loss','R'), ('tie','R')]:
    v = pooled[k]; n = sum(v.values())
    pm = {h: round(sum(d[h] for d in perplayer[k])/len(perplayer[k]), 3) for h in 'RPS'}
    print(k, 'pooled', {h: round(v[h]/n, 3) for h in 'RPS'}, 'n', n, 'per-player mean', pm, 'players', len(perplayer[k]))
