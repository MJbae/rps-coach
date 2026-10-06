import csv, sys, math
from collections import defaultdict, Counter
path = sys.argv[1]
rows = list(csv.DictReader(open(path)))
print('rows', len(rows))
print('moves', Counter(r['player_move'] for r in rows))
print('outcomes', Counter(r['player_outcome'] for r in rows))
games = defaultdict(lambda: defaultdict(dict))
for r in rows:
    games[r['game_id']][r['player_id']][int(r['round_index'])] = r
print('games', len(games))
sizes = Counter()
complete = []
for g, players in games.items():
    np_ = len(players)
    nr = [len(v) for v in players.values()]
    sizes[(np_, tuple(sorted(nr)))] += 1
    if np_ == 2 and all(n == 300 for n in nr) and all(set(v.keys()) == set(range(1, 301)) for v in players.values()):
        complete.append(g)
print('game size distribution (top):', sizes.most_common(10))
print('complete games:', len(complete))
UP = {'rock': 'paper', 'paper': 'scissors', 'scissors': 'rock'}
DOWN = {'rock': 'scissors', 'paper': 'rock', 'scissors': 'paper'}
def mean(xs): return sum(xs)/len(xs)
def sem(xs):
    m = mean(xs); return math.sqrt(sum((x-m)**2 for x in xs)/(len(xs)-1))/math.sqrt(len(xs))
per = defaultdict(list)  # (outcome, strat) -> list of per-player proportions
marg = Counter(); nmoves = 0
overall_stay = []
cournot = []
for g in complete:
    for pid, rounds in games[g].items():
        cnt = defaultdict(Counter)
        st = Counter()
        for t in range(1, 300):
            a, b = rounds[t], rounds[t+1]
            m0, m1, o = a['player_move'], b['player_move'], a['player_outcome']
            if m0 not in UP or m1 not in UP: continue
            s = 'stay' if m1 == m0 else ('up' if m1 == UP[m0] else 'down')
            cnt[o][s] += 1
            st[s] += 1
        for t in range(1, 301):
            m = rounds[t]['player_move']
            if m in UP: marg[m] += 1; nmoves += 1
        tot = sum(st.values()); overall_stay.append(st['stay']/tot)
        for o in ('win', 'tie', 'loss'):
            n = sum(cnt[o].values())
            if n == 0: continue
            for s in ('stay', 'up', 'down'):
                per[(o, s)].append(cnt[o][s]/n)
print('players:', len(overall_stay), 'moves:', nmoves)
print('marginals:', {k: round(v/nmoves, 3) for k, v in marg.items()})
print('overall stay mean:', round(mean(overall_stay), 3))
for o in ('win', 'tie', 'loss'):
    print(o, {s: (round(mean(per[(o, s)]), 3), round(sem(per[(o, s)]), 3), len(per[(o, s)])) for s in ('stay', 'up', 'down')})
