import csv, sys, statistics as st
from collections import defaultdict, Counter
games = defaultdict(list)
for r in csv.DictReader(open(sys.argv[1])):
    games[r['game_id']].append(r)
per_strat = defaultdict(list)
for g, rs in games.items():
    bots = [r for r in rs if r['is_bot'] == '1']; hum = [r for r in rs if r['is_bot'] == '0']
    if not bots or not hum: continue
    strat = bots[0]['bot_strategy']
    rounds = len(set(r['round_index'] for r in hum))
    bw = sum(1 for r in bots if r['player_outcome'] == 'win'); hw = sum(1 for r in hum if r['player_outcome'] == 'win')
    if rounds == 300: per_strat[strat].append((bw - hw, rounds, bw, hw))
print('games:', sum(len(v) for v in per_strat.values()))
for s, v in sorted(per_strat.items(), key=lambda kv: st.mean(x[0] for x in kv[1])):
    d = [x[0] for x in v]; n = len(d)
    rounds = Counter(x[1] for x in v)
    m = st.mean(d); se = st.stdev(d) / n ** 0.5
    print('%-40s n=%2d rounds=%s  mean bot win-count diff %+6.1f (SEM %.1f; t=%.2f)  per-round %+.3f  bots ahead in %d/%d' % (
        s, n, dict(rounds), m, se, m / se, m / 300, sum(1 for x in d if x > 0), n))
