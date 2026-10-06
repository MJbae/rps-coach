import csv, sys, math
from collections import defaultdict, Counter
rows = csv.DictReader(open(sys.argv[1]))
games = defaultdict(lambda: {'bot': None, 'strategy': None, 'rounds': defaultdict(dict)})
for r in rows:
    g = games[r['game_id']]
    g['strategy'] = r['bot_strategy']
    who = 'bot' if r['is_bot'] == '1' else 'human'
    g['rounds'][int(r['round_index'])][who] = r
def mean(xs): return sum(xs)/len(xs)
def sd(xs):
    m = mean(xs); return math.sqrt(sum((x-m)**2 for x in xs)/(len(xs)-1))
by = defaultdict(list)
lens = Counter()
for gid, g in games.items():
    rs = g['rounds']
    n = len([k for k, v in rs.items() if 'bot' in v and 'human' in v])
    lens[n] += 1
    if n != 300: continue
    bw = sum(1 for k, v in rs.items() if v['bot']['player_outcome'] == 'win')
    hw = sum(1 for k, v in rs.items() if v['human']['player_outcome'] == 'win')
    by[g['strategy']].append(bw - hw)
print('round count distribution:', lens.most_common(8))
for s, xs in sorted(by.items(), key=lambda kv: mean(kv[1])):
    n = len(xs); m = mean(xs); t = m / (sd(xs)/math.sqrt(n))
    print(f"{s:35s} n={n:3d} mean_bot_diff={m:+7.1f} per-round={m/300*100:+5.1f}pp t={t:+.2f} bot_ahead={sum(1 for x in xs if x>0)} human>=0={sum(1 for x in xs if x<=0)}")
