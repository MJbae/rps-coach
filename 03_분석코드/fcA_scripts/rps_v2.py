import csv, sys, math
from collections import defaultdict, Counter
csv.field_size_limit(10**9)
rows = csv.DictReader(open(sys.argv[1]))
games = defaultdict(lambda: {'strategy': None, 'rounds': defaultdict(dict)})
for r in rows:
    g = games[r['game_id']]
    g['strategy'] = r['bot_strategy']
    who = 'bot' if r['is_bot'] == '1' else 'human'
    g['rounds'][int(r['round_index'])][who] = r['player_outcome']
def mean(xs): return sum(xs)/len(xs)
by = defaultdict(list); lens = Counter()
for gid, g in games.items():
    rs = g['rounds']
    n = len([k for k, v in rs.items() if 'bot' in v and 'human' in v])
    lens[n] += 1
    if n != 300: continue
    hw = sum(1 for v in rs.values() if v['human'] == 'win')
    hl = sum(1 for v in rs.values() if v['human'] == 'loss')
    by[g['strategy']].append((hw/300, hl/300))
print('round counts:', lens.most_common(6))
tot = 0
for s, xs in sorted(by.items(), key=lambda kv: mean([x[0] for x in kv[1]])):
    tot += len(xs)
    print(f"{s:40s} n={len(xs):3d} human win rate={mean([x[0] for x in xs])*100:5.1f}% loss rate={mean([x[1] for x in xs])*100:5.1f}%")
print('total complete', tot)
