import csv, sys, collections, math
path = sys.argv[1]
groups = {
 'simple_transition (4 bots)': {'prev_move_positive','prev_move_negative','opponent_prev_move_positive','opponent_prev_move_nil'},
 'self_transition (2 bots)': {'prev_move_positive','prev_move_negative'},
 'outcome_conditioned (2 bots)': {'win_nil_lose_positive','win_positive_lose_negative'},
}
rows = collections.defaultdict(list)
with open(path, newline='') as f:
    for row in csv.DictReader(f):
        rows[row['game_id']].append(row)
bins = [(1,3),(4,6),(7,10),(11,15),(16,20),(21,30),(31,50)]
for gname, strats in groups.items():
    per = collections.defaultdict(list)
    for gid, rs in rows.items():
        hum = {int(x['round_index']): x for x in rs if x['is_bot']=='0'}
        if len(hum)!=300: continue
        strat = next((x['bot_strategy'] for x in rs if x['bot_strategy']), None)
        if strat not in strats: continue
        for (a,b) in bins:
            w=sum(1 for i in range(a,b+1) if hum[i]['player_outcome']=='win')
            l=sum(1 for i in range(a,b+1) if hum[i]['player_outcome']=='loss')
            per[(a,b)].append((w,l,b-a+1))
    print(gname, 'games', len(per[bins[0]]))
    for bn in bins:
        xs = per[bn]
        W=sum(x[0] for x in xs); L=sum(x[1] for x in xs); N=sum(x[2] for x in xs)
        d=[(x[0]-x[1])/x[2] for x in xs]; m=sum(d)/len(d)
        sd=math.sqrt(sum((v-m)**2 for v in d)/(len(d)-1)); se=sd/math.sqrt(len(d))
        print(f'   rounds {bn[0]}-{bn[1]}: win {W/N:.3f} loss {L/N:.3f} net {m:+.3f} (SE {se:.3f}, 95% CI {m-1.96*se:+.3f} to {m+1.96*se:+.3f})')
