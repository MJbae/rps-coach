import csv, sys, glob, os, math
from collections import defaultdict, Counter
UP = {'R': 'P', 'P': 'S', 'S': 'R'}
BEATS = {'R': 'S', 'P': 'R', 'S': 'P'}
def outcome(a, b):
    if a == b: return 'tie'
    return 'win' if BEATS[a] == b else 'loss'
def table(pairs, lo, hi, label):
    cnt = defaultdict(Counter)
    for P, Q in pairs:
        for t in range(lo-1, min(hi, len(P))-1):
            if P[t] and Q[t] and P[t+1]:
                o = outcome(P[t], Q[t]); s = 'stay' if P[t+1] == P[t] else ('up' if P[t+1] == UP[P[t]] else 'down')
                cnt[o][s] += 1
    out = []
    for o in ('win', 'tie', 'loss'):
        n = sum(cnt[o].values())
        out.append(f"{o}: stay {cnt[o]['stay']/n:.3f} up {cnt[o]['up']/n:.3f} down {cnt[o]['down']/n:.3f} (n={n})")
    print(f"{label} rounds {lo}-{hi}: " + ' | '.join(out))
M = {'rock': 'R', 'paper': 'P', 'scissors': 'S'}
rows = list(csv.DictReader(open(sys.argv[1])))
games = defaultdict(lambda: defaultdict(dict))
for r in rows: games[r['game_id']][r['player_id']][int(r['round_index'])] = M.get(r['player_move'])
us = []
for g, pl in games.items():
    ids = list(pl)
    if len(ids) != 2 or any(len(pl[i]) != 300 for i in ids): continue
    a = [pl[ids[0]][t] for t in range(1, 301)]; b = [pl[ids[1]][t] for t in range(1, 301)]
    us += [(a, b), (b, a)]
N = {'1': 'R', '2': 'P', '3': 'S'}
au = []
for f in sorted(glob.glob(os.path.join(sys.argv[2], '*_events.tsv'))):
    rr = list(csv.DictReader(open(f), delimiter='\t'))
    a = [N.get(r['player1_resp']) for r in rr]; b = [N.get(r['player2_resp']) for r in rr]
    au += [(a, b), (b, a)]
for lab, pairs, rng in (('US', us, [(1, 20), (1, 50), (51, 300)]), ('AU', au, [(1, 20), (1, 50), (51, 480)])):
    for lo, hi in rng:
        table(pairs, lo, hi, lab)
