import sys, csv
from collections import Counter, defaultdict
rows = list(csv.DictReader(open(sys.argv[1])))
print('rows', len(rows))
print('moves', Counter(r['player_move'] for r in rows))
print('outcomes', Counter(r['player_outcome'] for r in rows))
print('points by outcome', {o: Counter(r['player_points'] for r in rows if r['player_outcome']==o) for o in ('win','loss','tie')})
games = defaultdict(lambda: defaultdict(dict))
for r in rows:
    games[r['game_id']][r['player_id']][int(r['round_index'])] = r['player_move']
M = {'rock':'R','paper':'P','scissors':'S'}
beats = {'R':'S','P':'R','S':'P'}
beaten_by = {v:k for k,v in beats.items()}
players=[]
for g, pl in games.items():
    ids = list(pl.keys())
    if len(ids)!=2: continue
    a,b = ids
    n = max(max(pl[a]), max(pl[b]))
    sa=[]; sb=[]
    for i in range(1, n+1):
        ma = M.get(pl[a].get(i)); mb = M.get(pl[b].get(i))
        sa.append((ma,mb)); sb.append((mb,ma))
    players += [sa, sb]
print('games', len(games), 'players', len(players), 'rounds per player', Counter(len(p) for p in players))
c=Counter(); first=Counter()
for p in players:
    if p[0][0]: first[p[0][0]]+=1
    for o,_ in p:
        if o: c[o]+=1
tot=sum(c.values()); print('overall', {k: round(100*c[k]/tot,2) for k in 'RPS'}, 'n', tot)
print('first round', dict(first), {k: round(100*first[k]/sum(first.values()),1) for k in 'RPS'})
def outcome(a,b):
    if a==b: return 'D'
    return 'W' if beats[a]==b else 'L'
def trans(cond=None):
    st=Counter(); per=[]
    for p in players:
        pc=Counter()
        for t in range(len(p)-1):
            own,opp=p[t]; nxt=p[t+1][0]
            if not own or not opp or not nxt: continue
            if cond and outcome(own,opp)!=cond: continue
            k='stay' if nxt==own else ('up' if nxt==beaten_by[own] else 'down')
            st[k]+=1; pc[k]+=1
        n=sum(pc.values())
        if n: per.append({k: pc[k]/n for k in ('stay','up','down')})
    n=sum(st.values())
    return n, {k: round(100*st[k]/n,1) for k in ('stay','up','down')}, {k: round(100*sum(d[k] for d in per)/len(per),1) for k in ('stay','up','down')}, per
for cond in [None,'W','L','D']:
    n,pooled,mp,per = trans(cond)
    print('after', cond or 'ANY', 'n', n, 'pooled', pooled, 'mean-of-players', mp)
n,pooled,mp,per = trans(None)
print('players with stay<1/3:', sum(1 for d in per if d['stay']<1/3), 'of', len(per))
for X in 'RPS':
    st=Counter()
    for p in players:
        for t in range(len(p)-1):
            own,opp=p[t]; nxt=p[t+1][0]
            if own and opp and nxt and own==opp==X: st[nxt]+=1
    n=sum(st.values()); print('after draw on', X, 'n', n, {k: round(100*st[k]/n,1) for k in 'RPS'})
st=Counter()
for p in players:
    for t in range(len(p)-2):
        a,b,cc=p[t][0],p[t+1][0],p[t+2][0]
        if a and b and cc and a==b: st['same' if cc==a else 'diff']+=1
print('P(third same | two same) = %.3f n=%d' % (st['same']/sum(st.values()), sum(st.values())))
n,pooled,mp,per = trans('D')
S,U,Dn = pooled['stay'],pooled['up'],pooled['down']
print('after draw nets: throw hand beating X %.1f; throw hand X beats %.1f; repeat X %.1f' % (S-Dn, U-S, Dn-U))
