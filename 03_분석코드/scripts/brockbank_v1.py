import csv, sys, statistics as st
from collections import Counter, defaultdict
UP = {'rock': 'paper', 'paper': 'scissors', 'scissors': 'rock'}
rows = list(csv.DictReader(open(sys.argv[1])))
games = defaultdict(list)
for r in rows: games[r['game_id']].append(r)
complete = {g: rs for g, rs in games.items() if len(rs) == 600 and len(set(r['round_index'] for r in rs)) == 300}
print('games total', len(games), 'complete (600 rows/300 rounds):', len(complete))
mar = Counter(); per_player = defaultdict(lambda: {o: Counter() for o in ('win', 'tie', 'loss')})
pooled = {o: Counter() for o in ('win', 'tie', 'loss')}
opp_rel = {o: Counter() for o in ('win', 'tie', 'loss')}  # next move relative to OPPONENT's previous move
outcomes = Counter()
for g, rs in complete.items():
    byp = defaultdict(dict)
    for r in rs: byp[r['player_id']][int(r['round_index'])] = r
    pids = list(byp)
    if len(pids) != 2: continue
    for i, p in enumerate(pids):
        q = pids[1 - i]
        for t in range(1, 301):
            m = byp[p][t]['player_move']
            if m in UP: mar[m] += 1; outcomes[byp[p][t]['player_outcome']] += 1
        for t in range(1, 300):
            a, b = byp[p][t], byp[p][t + 1]
            o = a['player_outcome']; m0, m1 = a['player_move'], b['player_move']; om0 = byp[q][t]['player_move']
            if o not in pooled or m0 not in UP or m1 not in UP or om0 not in UP: continue
            tr = 'stay' if m1 == m0 else ('up' if m1 == UP[m0] else 'down')
            pooled[o][tr] += 1; per_player[p][o][tr] += 1
            trq = 'stay' if m1 == om0 else ('up' if m1 == UP[om0] else 'down')
            opp_rel[o][trq] += 1
N = sum(mar.values())
print('marginals: rock %.4f paper %.4f scissors %.4f (N=%d moves)' % (mar['rock'] / N, mar['paper'] / N, mar['scissors'] / N, N))
print('outcome counts (player-rounds):', dict(outcomes))
for o in ('win', 'tie', 'loss'):
    tot = sum(pooled[o].values())
    vals = {k: [per_player[p][o][k] / sum(per_player[p][o].values()) for p in per_player if sum(per_player[p][o].values()) >= 10] for k in ('stay', 'up', 'down')}
    sem = {k: st.stdev(v) / len(v) ** 0.5 for k, v in vals.items()}
    print('after %-4s pooled n=%5d: stay %.3f up %.3f down %.3f | mean of %d players: stay %.3f(±%.3f) up %.3f(±%.3f) down %.3f(±%.3f)' % (
        o, tot, pooled[o]['stay'] / tot, pooled[o]['up'] / tot, pooled[o]['down'] / tot, len(vals['stay']),
        st.mean(vals['stay']), sem['stay'], st.mean(vals['up']), sem['up'], st.mean(vals['down']), sem['down']))
    t2 = sum(opp_rel[o].values())
    print('     relative to OPPONENT prev move: copy %.3f  beat-it(up) %.3f  lose-to-it(down) %.3f' % (opp_rel[o]['stay'] / t2, opp_rel[o]['up'] / t2, opp_rel[o]['down'] / t2))
