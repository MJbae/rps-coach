import sys, glob, os, csv, math
D = sys.argv[1]
files = sorted(glob.glob(os.path.join(D, 'sub-*_events.tsv')))
H = {1:'R',2:'P',3:'S'}
beats = {'R':'S','P':'R','S':'P'}   # key beats value
beaten_by = {v:k for k,v in beats.items()}  # hand that beats key
def outcome(a,b):
    if a==b: return 'D'
    return 'W' if beats[a]==b else 'L'
players = []  # list of sequences of (own, opp)
for f in files:
    rows = list(csv.DictReader(open(f), delimiter='\t'))
    rows.sort(key=lambda r:int(r['trial_num']))
    s1=[]; s2=[]
    for r in rows:
        a=int(r['player1_resp']); b=int(r['player2_resp'])
        s1.append((H.get(a), H.get(b))); s2.append((H.get(b), H.get(a)))
    players.append(s1); players.append(s2)
print('players', len(players), 'trials per player', set(len(p) for p in players))
# marginals
from collections import Counter
c=Counter(); first=Counter(); noresp=0
for p in players:
    if p[0][0]: first[p[0][0]]+=1
    for own,opp in p:
        if own: c[own]+=1
        else: noresp+=1
tot=sum(c.values())
print('no responses', noresp, 'valid', tot)
print('overall', {k: round(100*c[k]/tot,2) for k in 'RPS'})
print('first game', dict(first))
# per-player marginal; most-played
mp=Counter()
for p in players:
    cc=Counter(o for o,_ in p if o)
    mp[max('RPS', key=lambda k: cc[k])]+=1
print('most-played hand counts', dict(mp))
# transitions
def trans_stats(cond=None):
    st=Counter(); per=[]
    for p in players:
        pc=Counter()
        for t in range(len(p)-1):
            own,opp = p[t]; nxt = p[t+1][0]
            if not own or not opp or not nxt: continue
            o = outcome(own,opp)
            if cond and o!=cond: continue
            if nxt==own: k='stay'
            elif nxt==beaten_by[own]: k='up'      # hand that beats own previous
            else: k='down'                         # hand own previous beats
            st[k]+=1; pc[k]+=1
        n=sum(pc.values())
        if n: per.append({k:pc[k]/n for k in ('stay','up','down')})
    n=sum(st.values())
    pooled={k: round(100*st[k]/n,1) for k in ('stay','up','down')}
    meanper={k: round(100*sum(d[k] for d in per)/len(per),1) for k in ('stay','up','down')}
    return n, pooled, meanper, per
for cond in [None,'W','L','D']:
    n,pooled,meanper,per = trans_stats(cond)
    print('after', cond or 'ANY', 'n=',n, 'pooled', pooled, 'mean-of-players', meanper)
n,pooled,meanper,per = trans_stats(None)
below = sum(1 for d in per if d['stay']<1/3)
print('players with overall stay <1/3:', below, 'of', len(per), 'min %.3f max %.3f' % (min(d['stay'] for d in per), max(d['stay'] for d in per)))
# after draw by tied hand
for X in 'RPS':
    st=Counter()
    for p in players:
        for t in range(len(p)-1):
            own,opp=p[t]; nxt=p[t+1][0]
            if not own or not opp or not nxt: continue
            if own==opp==X:
                st[nxt]+=1
    n=sum(st.values())
    print('after draw on',X,'n=',n, {k: round(100*st[k]/n,1) for k in 'RPS'})
# third in a row
st=Counter()
for p in players:
    for t in range(len(p)-2):
        a,b,cc = p[t][0],p[t+1][0],p[t+2][0]
        if not a or not b or not cc: continue
        if a==b:
            st['same' if cc==a else 'diff']+=1
n=sum(st.values()); print('P(third same | two same) = %.3f (n=%d)' % (st['same']/n, n))
# opponent-relative: after draw, best response values (pooled)
n,pooled,meanper,per = trans_stats('D')
S,U,Dn = pooled['stay'],pooled['up'],pooled['down']
print('after draw best-response nets (pp): throw hand that beats X (beats stay): %.1f; throw hand X beats (beats up): %.1f; repeat X (beats down): %.1f' % (S-Dn, U-S, Dn-U))
