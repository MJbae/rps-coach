import csv, sys, os, collections, math, random
base = sys.argv[1]
parts = {r['participant_id']: r for r in csv.DictReader(open(os.path.join(base,'participants.tsv')), delimiter='\t')}
NAME={1:'R',2:'P',3:'S'}
players=[]  # (gender, age, hands list (valid only, in order), first valid)
for pid, r in parts.items():
    rows=list(csv.DictReader(open(os.path.join(base,'events',f'{pid}_task-RPS_events.tsv')), delimiter='\t'))
    for k in ['player1','player2']:
        hands=[int(x[f'{k}_resp']) for x in rows]
        players.append((r[f'{k}_gender'], r[f'{k}_age'], pid+k, hands))
print('players', len(players), collections.Counter(p[0] for p in players))
def shares(hs):
    c=collections.Counter(h for h in hs if h in (1,2,3)); n=sum(c.values()); return {NAME[k]: c[k]/n for k in (1,2,3)}, n
by=collections.defaultdict(list)
for g,age,pid,hands in players:
    s,n=shares(hands); by[g].append((s,n,hands))
for g in sorted(by):
    xs=by[g]
    mean={h: sum(x[0][h] for x in xs)/len(xs) for h in 'RPS'}
    se={h: math.sqrt(sum((x[0][h]-mean[h])**2 for x in xs)/(len(xs)-1))/math.sqrt(len(xs)) if len(xs)>1 else float('nan') for h in 'RPS'}
    pooled=collections.Counter(); 
    for x in xs: pooled.update(h for h in x[2] if h in (1,2,3))
    N=sum(pooled.values())
    most=collections.Counter(max('RPS', key=lambda h: x[0][h]) for x in xs)
    first=collections.Counter(NAME[next(h for h in x[2] if h in (1,2,3))] for x in xs)
    print(f"{g}: n={len(xs)} per-player mean R {mean['R']:.3f} ({se['R']:.3f}) P {mean['P']:.3f} ({se['P']:.3f}) S {mean['S']:.3f} ({se['S']:.3f}); pooled R {pooled[1]/N:.3f} P {pooled[2]/N:.3f} S {pooled[3]/N:.3f}; most-played {dict(most)}; first valid throw {dict(first)}")
# difference M - F in Rock share with bootstrap over players
M=[x[0]['R'] for x in by['M']]; F=[x[0]['R'] for x in by['F']]
d=sum(M)/len(M)-sum(F)/len(F)
random.seed(2)
bs=sorted((sum(random.choices(M,k=len(M)))/len(M) - sum(random.choices(F,k=len(F)))/len(F)) for _ in range(5000))
print('Rock share M-F: %+.3f, 95%% bootstrap CI %+.3f to %+.3f' % (d, bs[125], bs[4874]))
for h in 'PS':
    M=[x[0][h] for x in by['M']]; F=[x[0][h] for x in by['F']]
    d=sum(M)/len(M)-sum(F)/len(F)
    bs=sorted((sum(random.choices(M,k=len(M)))/len(M) - sum(random.choices(F,k=len(F)))/len(F)) for _ in range(5000))
    print('%s share M-F: %+.3f, 95%% bootstrap CI %+.3f to %+.3f' % (h, d, bs[125], bs[4874]))
