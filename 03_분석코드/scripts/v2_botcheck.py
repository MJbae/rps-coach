import csv, sys, collections
path = sys.argv[1]
rows = collections.defaultdict(list)
with open(path, newline='') as f:
    for row in csv.DictReader(f):
        rows[row['game_id']].append(row)
BEATS = {'rock':'scissors','paper':'rock','scissors':'paper'}  # key beats value
UP = {'rock':'paper','paper':'scissors','scissors':'rock'}       # hand that beats key
DOWN = {v:k for k,v in UP.items()}                                # hand that key beats
stats = collections.defaultdict(lambda: collections.Counter())
for gid, rs in rows.items():
    hum = {int(x['round_index']): x for x in rs if x['is_bot']=='0'}
    bot = {int(x['round_index']): x for x in rs if x['is_bot']=='1'}
    if len(hum)!=300 or len(bot)!=300: continue
    strat = next((x['bot_strategy'] for x in rs if x['bot_strategy']), None)
    for i in range(2,301):
        b0, b1 = bot[i-1]['player_move'], bot[i]['player_move']
        h0 = hum[i-1]['player_move']
        bo = bot[i-1]['player_outcome']
        if b0 not in UP or b1 not in UP or h0 not in UP: continue
        selft = 'stay' if b1==b0 else ('up' if b1==UP[b0] else 'down')
        oppt = 'copy' if b1==h0 else ('beat' if b1==UP[h0] else 'lose')
        stats[strat]['self_'+selft]+=1
        stats[strat]['opp_'+oppt]+=1
        stats[strat][f'{bo}_self_{selft}']+=1
for s,c in sorted(stats.items()):
    n = c['self_stay']+c['self_up']+c['self_down']
    print(s, 'n', n)
    print('   self: stay %.3f up %.3f down %.3f' % (c['self_stay']/n, c['self_up']/n, c['self_down']/n))
    print('   vs human prev: copy %.3f beat %.3f lose %.3f' % (c['opp_copy']/n, c['opp_beat']/n, c['opp_lose']/n))
    for o in ['win','loss','tie']:
        m = c[f'{o}_self_stay']+c[f'{o}_self_up']+c[f'{o}_self_down']
        if m: print('   after bot %s: stay %.3f up %.3f down %.3f' % (o, c[f'{o}_self_stay']/m, c[f'{o}_self_up']/m, c[f'{o}_self_down']/m))
