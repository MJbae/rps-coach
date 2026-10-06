import sys, csv, glob, os
from collections import Counter, defaultdict
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
beats = {'R':'S','P':'R','S':'P'}; beaten_by = {v:k for k,v in beats.items()}
def load_moerel(D):
    H={1:'R',2:'P',3:'S'}; out=[]
    for f in sorted(glob.glob(os.path.join(D,'sub-*_events.tsv'))):
        rows=sorted(csv.DictReader(open(f),delimiter='\t'), key=lambda r:int(r['trial_num']))
        out.append([H.get(int(r['player1_resp'])) for r in rows]); out.append([H.get(int(r['player2_resp'])) for r in rows])
    return out
def load_brock(path):
    M={'rock':'R','paper':'P','scissors':'S'}
    games=defaultdict(lambda: defaultdict(dict))
    for r in csv.DictReader(open(path)):
        games[r['game_id']][r['player_id']][int(r['round_index'])]=r['player_move']
    out=[]
    for g,pl in games.items():
        for pid,mv in pl.items():
            n=max(mv)
            if n<300: continue
            out.append([M.get(mv.get(i)) for i in range(1,n+1)])
    return out
def step(a,b):
    if a==b: return 'stay'
    return 'up' if b==beaten_by[a] else 'down'
def analyze(name, seqs):
    c=defaultdict(Counter)
    for s in seqs:
        for t in range(len(s)-2):
            a,b,cc=s[t],s[t+1],s[t+2]
            if not (a and b and cc): continue
            c[step(a,b)][step(b,cc)]+=1
    print(name)
    for k in ('stay','up','down'):
        n=sum(c[k].values())
        print('  after', k, 'n=%d' % n, {j: round(100*c[k][j]/n,1) for j in ('stay','up','down')})
analyze('Moerel AUS', load_moerel(sys.argv[1]))
analyze('Brockbank US', load_brock(sys.argv[2]))
