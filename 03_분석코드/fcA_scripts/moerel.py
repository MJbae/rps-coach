import csv, sys, math, glob, os
from collections import Counter, defaultdict
files = sorted(glob.glob(os.path.join(sys.argv[1], '*_events.tsv')))
print('pair files:', len(files))
NAME = {'1': 'R', '2': 'P', '3': 'S'}
UP = {'R': 'P', 'P': 'S', 'S': 'R'}
DOWN = {'R': 'S', 'P': 'R', 'S': 'P'}
BEATS = {'R': 'S', 'P': 'R', 'S': 'P'}
def outcome(a, b):
    if a == b: return 'tie'
    return 'win' if BEATS[a] == b else 'loss'
def mean(xs): return sum(xs)/len(xs)
def sem(xs):
    m = mean(xs); return math.sqrt(sum((x-m)**2 for x in xs)/(len(xs)-1))/math.sqrt(len(xs))
per = defaultdict(list); stays = []; marg = Counter(); nm = 0; most = Counter(); ntr = 0
mismatch = 0; ngames = []
for f in files:
    rows = list(csv.DictReader(open(f), delimiter='\t'))
    ngames.append(len(rows))
    for me, opp in (('player1_resp', 'player2_resp'), ('player2_resp', 'player1_resp')):
        seq = []
        for r in rows:
            a = NAME.get(r[me]); b = NAME.get(r[opp])
            seq.append((a, b))
        # check file outcome coding for player1
        if me == 'player1_resp':
            for r in rows:
                a = NAME.get(r['player1_resp']); b = NAME.get(r['player2_resp'])
                if a and b:
                    o = outcome(a, b); code = {'tie': '1', 'win': '2', 'loss': '3'}[o]
                    if code != r['outcome']: mismatch += 1
        c = Counter(a for a, b in seq if a)
        for k, v in c.items(): marg[k] += v; nm += v
        top = max(c.values()); 
        for k, v in c.items():
            if v == top: most[k] += 1
        cnt = defaultdict(Counter); st = Counter()
        for t in range(len(seq)-1):
            (a0, b0), (a1, b1) = seq[t], seq[t+1]
            if not (a0 and b0 and a1): continue
            o = outcome(a0, b0)
            s = 'stay' if a1 == a0 else ('up' if a1 == UP[a0] else 'down')
            cnt[o][s] += 1; st[s] += 1; ntr += 1
        stays.append(st['stay']/sum(st.values()))
        for o in ('win', 'tie', 'loss'):
            n = sum(cnt[o].values())
            for s in ('stay', 'up', 'down'):
                per[(o, s)].append(cnt[o][s]/n)
print('games per pair:', Counter(ngames))
print('outcome-code mismatches:', mismatch)
print('players:', len(stays), 'moves:', nm, 'transitions:', ntr)
print('marginals:', {k: round(v/nm, 3) for k, v in marg.items()})
print('most-played share (ties counted for each):', {k: round(v/len(stays), 4) for k, v in most.items()})
print('overall stay:', round(mean(stays), 3))
for o in ('win', 'tie', 'loss'):
    print(o, {s: (round(mean(per[(o, s)]), 3), round(sem(per[(o, s)]), 3)) for s in ('stay', 'up', 'down')})
