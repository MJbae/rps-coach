import sys, csv, glob, os, random, math
from collections import Counter, defaultdict
random.seed(1)
beats = {'R':'S','P':'R','S':'P'}; beaten_by = {v:k for k,v in beats.items()}
def load_moerel(D):
    H={1:'R',2:'P',3:'S'}; players=[]
    for f in sorted(glob.glob(os.path.join(D,'sub-*_events.tsv'))):
        rows=sorted(csv.DictReader(open(f),delimiter='\t'), key=lambda r:int(r['trial_num']))
        s1=[(H.get(int(r['player1_resp'])),H.get(int(r['player2_resp']))) for r in rows]
        s2=[(b,a) for a,b in s1]
        players.append((f,1,s1)); players.append((f,2,s2))
    return players
def load_brock(path, complete_only=True):
    M={'rock':'R','paper':'P','scissors':'S'}
    games=defaultdict(lambda: defaultdict(dict))
    for r in csv.DictReader(open(path)):
        games[r['game_id']][r['player_id']][int(r['round_index'])]=r['player_move']
    players=[]
    for g,pl in games.items():
        ids=list(pl)
        if len(ids)!=2: continue
        a,b=ids; n=max(max(pl[a]),max(pl[b]))
        if complete_only and n<300: continue
        sa=[(M.get(pl[a].get(i)),M.get(pl[b].get(i))) for i in range(1,n+1)]
        players.append((g,1,sa)); players.append((g,2,[(y,x) for x,y in sa]))
    return players
def counts(p):
    c=Counter()
    for t in range(len(p)-1):
        own,opp=p[t]; nxt=p[t+1][0]
        if own and opp and nxt and own==opp:
            c['stay' if nxt==own else ('up' if nxt==beaten_by[own] else 'down')]+=1
    return c
def marg(p):
    return Counter(o for o,_ in p if o)
def summarize(name, players):
    # cluster bootstrap over pairs (both players of a pair resampled together)
    pairs=defaultdict(list)
    for key,idx,p in players: pairs[key].append(p)
    keys=list(pairs)
    def stat(sel):
        c=Counter(); m=Counter()
        for k in sel:
            for p in pairs[k]:
                c+=counts(p); m+=marg(p)
        n=sum(c.values()); tm=sum(m.values())
        s,u,d=c['stay']/n,c['up']/n,c['down']/n
        return dict(stay=s,up=u,down=d, Z=u-s, Y=s-d, X=d-u, R=m['R']/tm, P=m['P']/tm, S=m['S']/tm, paper_net=(m['R']-m['S'])/tm)
    base=stat(keys)
    B=[stat([random.choice(keys) for _ in keys]) for _ in range(2000)]
    print(name, 'pairs', len(keys))
    for k in ['R','P','S','paper_net','stay','up','down','Z','Y','X']:
        vals=sorted(b[k] for b in B)
        print('  %-9s %6.1f  [95%% CI %6.1f, %6.1f]' % (k, 100*base[k], 100*vals[50], 100*vals[1949]))
summarize('Moerel (AUS, fixed human pairs)', load_moerel(sys.argv[1]))
summarize('Brockbank (US, fixed human dyads, complete games)', load_brock(sys.argv[2]))
