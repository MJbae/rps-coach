import csv, sys, collections, math
path = sys.argv[1]
rows = collections.defaultdict(list)
with open(path, newline='') as f:
    r = csv.DictReader(f)
    for row in r:
        rows[row['game_id']].append(row)
# per game: identify human rows and bot strategy
games = {}
for gid, rs in rows.items():
    humans = [x for x in rs if x['is_bot'] == '0']
    bots = [x for x in rs if x['is_bot'] == '1']
    strat = None
    for x in rs:
        if x['bot_strategy']:
            strat = x['bot_strategy']; break
    rounds = sorted(set(int(x['round_index']) for x in humans))
    games[gid] = (strat, humans, bots, rounds)
complete = {g: v for g, v in games.items() if len(v[3]) == 300 and len(v[1]) == 300}
print('games total', len(games), 'complete', len(complete))
bins = [(1,5),(6,10),(11,20),(21,30),(31,50),(51,100),(101,200),(201,300)]
by = collections.defaultdict(lambda: collections.defaultdict(lambda: [0,0,0]))  # strat -> bin -> [win, loss, tie]
pergame = collections.defaultdict(lambda: collections.defaultdict(list))
for g, (strat, humans, bots, rounds) in complete.items():
    hb = {int(x['round_index']): x for x in humans}
    for (a,b) in bins:
        w=l=t=0
        for i in range(a,b+1):
            o = hb[i]['player_outcome']
            if o == 'win': w+=1
            elif o == 'loss': l+=1
            elif o == 'tie': t+=1
        by[strat][(a,b)][0]+=w; by[strat][(a,b)][1]+=l; by[strat][(a,b)][2]+=t
        n = w+l+t
        if n: pergame[strat][(a,b)].append((w-l)/n)
for strat in sorted(by):
    ng = len(pergame[strat][bins[0]])
    print('\n', strat, 'n_games=', ng)
    for bn in bins:
        w,l,t = by[strat][bn]; n=w+l+t
        diffs = pergame[strat][bn]
        m = sum(diffs)/len(diffs)
        sd = math.sqrt(sum((d-m)**2 for d in diffs)/(len(diffs)-1)) if len(diffs)>1 else 0
        se = sd/math.sqrt(len(diffs))
        print(f'  rounds {bn[0]:>3}-{bn[1]:<3}: win {w/n:.3f} loss {l/n:.3f} tie {t/n:.3f}  net(win-loss) {m:+.3f} (SE {se:.3f})')
