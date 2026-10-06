import sys, csv, glob, os
from collections import Counter, defaultdict
beats = {'R':'S','P':'R','S':'P'}; beaten_by = {v:k for k,v in beats.items()}
def load_moerel(D):
    H={1:'R',2:'P',3:'S'}; out=[]
    for f in sorted(glob.glob(os.path.join(D,'sub-*_events.tsv'))):
        rows=sorted(csv.DictReader(open(f),delimiter='\t'), key=lambda r:int(r['trial_num']))
        s1=[(H.get(int(r['player1_resp'])),H.get(int(r['player2_resp']))) for r in rows]
        out.append(s1); out.append([(b,a) for a,b in s1])
    return out
def load_brock(path):
    M={'rock':'R','paper':'P','scissors':'S'}
    games=defaultdict(lambda: defaultdict(dict))
    for r in csv.DictReader(open(path)):
        games[r['game_id']][r['player_id']][int(r['round_index'])]=r['player_move']
    out=[]
    for g,pl in games.items():
        ids=list(pl)
        if len(ids)!=2: continue
        a,b=ids; n=max(max(pl[a]),max(pl[b]))
        if n<300: continue
        sa=[(M.get(pl[a].get(i)),M.get(pl[b].get(i))) for i in range(1,n+1)]
        out.append(sa); out.append([(y,x) for x,y in sa])
    return out
def per(players, name):
    stay_lt=0; zpos=0; ypos=0; n=0
    for p in players:
        c=Counter()
        for t in range(len(p)-1):
            own,opp=p[t]; nxt=p[t+1][0]
            if own and opp and nxt and own==opp:
                c['stay' if nxt==own else ('up' if nxt==beaten_by[own] else 'down')]+=1
        tot=sum(c.values())
        if tot<10: continue
        n+=1
        s,u,d=c['stay']/tot,c['up']/tot,c['down']/tot
        stay_lt += s<1/3; zpos += (u-s)>0; ypos += (s-d)>0
    print(name, 'players', n, 'after-draw stay<1/3:', stay_lt, '| Z net>0:', zpos, '| Y net>0:', ypos)
per(load_moerel(sys.argv[1]), 'Moerel')
per(load_brock(sys.argv[2]), 'Brockbank')
