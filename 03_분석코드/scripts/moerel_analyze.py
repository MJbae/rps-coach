import csv, sys, glob, statistics as st
from collections import Counter
M = {'1': 'R', '2': 'P', '3': 'S'}
UP = {'R': 'P', 'P': 'S', 'S': 'R'}
BEATS = {'R': 'S', 'P': 'R', 'S': 'P'}
def outc(me, op):
    if me == op: return 'T'
    return 'W' if BEATS[me] == op else 'L'
mar = Counter(); pooled = {o: Counter() for o in 'WTL'}; perp = []
nets = []
for f in sorted(glob.glob(sys.argv[1] + '/sub-*_events.tsv')):
    rows = list(csv.DictReader(open(f), delimiter='\t'))
    rows.sort(key=lambda r: int(r['trial_num']))
    seqs = [[M.get(r['player1_resp']) for r in rows], [M.get(r['player2_resp']) for r in rows]]
    w1 = sum(1 for a, b in zip(*seqs) if a and b and outc(a, b) == 'W'); l1 = sum(1 for a, b in zip(*seqs) if a and b and outc(a, b) == 'L')
    nets.append(abs(w1 - l1))
    for i in (0, 1):
        me, op = seqs[i], seqs[1 - i]
        pc = {o: Counter() for o in 'WTL'}
        for m in me:
            if m: mar[m] += 1
        for t in range(len(rows) - 1):
            if not (me[t] and op[t] and me[t + 1]): continue
            o = outc(me[t], op[t])
            tr = 'stay' if me[t + 1] == me[t] else ('up' if me[t + 1] == UP[me[t]] else 'down')
            pooled[o][tr] += 1; pc[o][tr] += 1
        perp.append(pc)
N = sum(mar.values())
print('players', len(perp), 'pairs', len(nets), 'moves', N)
print('marginals R %.4f P %.4f S %.4f' % (mar['R'] / N, mar['P'] / N, mar['S'] / N))
print('mean |wins-losses| per pair over 480 games: %.1f (median %.1f)' % (st.mean(nets), st.median(nets)))
for o in 'WTL':
    tot = sum(pooled[o].values())
    vals = {k: [pc[o][k] / sum(pc[o].values()) for pc in perp if sum(pc[o].values()) >= 10] for k in ('stay', 'up', 'down')}
    print('after %s pooled n=%d: stay %.3f up %.3f down %.3f | mean of %d players: stay %.3f(±%.3f) up %.3f(±%.3f) down %.3f(±%.3f)' % (
        o, tot, pooled[o]['stay'] / tot, pooled[o]['up'] / tot, pooled[o]['down'] / tot, len(vals['stay']),
        st.mean(vals['stay']), st.stdev(vals['stay']) / len(vals['stay']) ** .5, st.mean(vals['up']), st.stdev(vals['up']) / len(vals['up']) ** .5,
        st.mean(vals['down']), st.stdev(vals['down']) / len(vals['down']) ** .5))
