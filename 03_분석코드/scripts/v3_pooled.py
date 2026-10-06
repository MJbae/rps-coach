import csv, sys, collections, math
path=sys.argv[1]
rows=collections.defaultdict(list)
with open(path, newline='') as f:
    for row in csv.DictReader(f): rows[row['game_id']].append(row)
groups={'top-3 adaptive exploiters (prev two moves; outcome x prev transition; own+opp prev move)':{'opponent_prev_two_moves','opponent_outcome_prev_transition_dual','opponent_bot_prev_move'},
        'WSLS (outcome-transition) exploiter':{'opponent_outcome_transitions'},
        'simple base-rate exploiters (own transitions; Cournot transitions)':{'opponent_transitions','opponent_courn_transitions'}}
bins=[(1,10),(11,20),(21,30),(31,50),(51,100),(101,300)]
for g,ss in groups.items():
    per=collections.defaultdict(list)
    for gid,rs in rows.items():
        hum={int(x['round_index']):x for x in rs if x['is_bot']=='0'}
        if len(hum)!=300: continue
        s=next((x['bot_strategy'] for x in rs if x['bot_strategy']),None)
        if s not in ss: continue
        for a,b in bins:
            w=sum(hum[i]['player_outcome']=='win' for i in range(a,b+1)); l=sum(hum[i]['player_outcome']=='loss' for i in range(a,b+1))
            per[(a,b)].append((w-l)/(b-a+1))
    print(g, 'games', len(per[bins[0]]))
    for bn in bins:
        d=per[bn]; m=sum(d)/len(d); se=math.sqrt(sum((x-m)**2 for x in d)/(len(d)-1))/math.sqrt(len(d))
        print(f'   human net rounds {bn[0]}-{bn[1]}: {m:+.3f} (95% CI {m-1.96*se:+.3f} to {m+1.96*se:+.3f})')
