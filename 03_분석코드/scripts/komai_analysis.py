import os, sys, math, collections
base = sys.argv[1]
H = os.path.join(base, 'Human_hand_data'); A = os.path.join(base, 'AI_hand_data')
# coding per Komai et al. 2022 Appendix: rock, scissors, paper = 0, 1, 2  -> h beats (h+1)%3
NAME = {0:'R',1:'S',2:'P'}
def beats(a,b): return (a+1)%3==b          # a beats b
def up(h): return (h-1)%3                  # hand that beats h  (R0 -> P2, S1 -> R0, P2 -> S1)
def down(h): return (h+1)%3                # hand that h beats  (R0 -> S1, S1 -> P2, P2 -> R0)
def outcome(me, op):
    if me==op: return 'tie'
    return 'win' if beats(me,op) else 'loss'
players=[]
for fn in sorted(os.listdir(H), key=lambda s: int(s.split('.')[0])):
    def parse(p):
        toks=[t.strip() for t in open(p).read().replace('\r','').replace('\n',',').split(',')]
        return [int(t) for t in toks if t!='']
    h=parse(os.path.join(H,fn)); a=parse(os.path.join(A,fn))
    L=min(len(h),len(a))
    if len(h)!=len(a): print('note: unequal lengths in', fn, len(h), len(a), '-> truncated to', L)
    players.append((fn,h[:L],a[:L]))
print('players', len(players), 'lengths', collections.Counter(len(p[1]) for p in players))
# 1 marginals
allh=collections.Counter(); first=collections.Counter(); ai=collections.Counter()
res=collections.Counter()
for fn,h,a in players:
    allh.update(h); first[h[0]]+=1; ai.update(a)
    for x,y in zip(h,a): res[outcome(x,y)]+=1
N=sum(allh.values())
print('human marginals', {NAME[k]: round(v/N,4) for k,v in sorted(allh.items())}, 'N', N)
print('human first throw', {NAME[k]: (v, round(v/len(players),4)) for k,v in sorted(first.items())})
print('AI marginals', {NAME[k]: round(v/sum(ai.values()),4) for k,v in sorted(ai.items())})
T=sum(res.values()); print('human outcome vs AI: win %.4f loss %.4f tie %.4f' % (res['win']/T, res['loss']/T, res['tie']/T))
# chi-square first throw vs uniform
n=len(players); exp=n/3; chi=sum((first[k]-exp)**2/exp for k in range(3)); print('first-throw chi2(df2)=%.2f' % chi)
# 2 repeat rates
rep=0; tot=0; per=[]
for fn,h,a in players:
    r=sum(1 for i in range(1,len(h)) if h[i]==h[i-1]); per.append(r/(len(h)-1)); rep+=r; tot+=len(h)-1
print('overall repeat %.4f; players below 1/3: %d of %d; mean of per-player %.4f' % (rep/tot, sum(1 for x in per if x<1/3), len(per), sum(per)/len(per)))
# 3 outcome-conditioned transitions, pooled and per-player means
def trans_table(rng):
    pooled=collections.defaultdict(collections.Counter); perp=collections.defaultdict(list)
    for fn,h,a in players:
        loc=collections.defaultdict(collections.Counter)
        for i in rng(len(h)):
            o=outcome(h[i-1],a[i-1]); x0=h[i-1]; x1=h[i]
            t='stay' if x1==x0 else ('up' if x1==up(x0) else 'down')
            pooled[o][t]+=1; loc[o][t]+=1
        for o in loc:
            m=sum(loc[o].values())
            if m>0: perp[o].append({k: loc[o][k]/m for k in ['stay','up','down']})
    return pooled, perp
for label, rng in [('all transitions (rounds 2-50)', lambda L: range(1,L)), ('rounds 2-20', lambda L: range(1,min(20,L))), ('rounds 21-50', lambda L: range(20,L))]:
    pooled, perp = trans_table(rng)
    print('\n==', label)
    for o in ['win','tie','loss']:
        m=sum(pooled[o].values())
        pp=perp[o]; 
        means={k: sum(d[k] for d in pp)/len(pp) for k in ['stay','up','down']}
        ses={k: math.sqrt(sum((d[k]-means[k])**2 for d in pp)/(len(pp)-1))/math.sqrt(len(pp)) for k in ['stay','up','down']}
        print(f"  after {o:4s} (n={m}, players={len(pp)}): pooled stay {pooled[o]['stay']/m:.3f} up {pooled[o]['up']/m:.3f} down {pooled[o]['down']/m:.3f} | per-player mean stay {means['stay']:.3f} ({ses['stay']:.3f}) up {means['up']:.3f} ({ses['up']:.3f}) down {means['down']:.3f} ({ses['down']:.3f})")
# 4 after tie by tied hand (next human hand distribution)
tied=collections.defaultdict(collections.Counter)
for fn,h,a in players:
    for i in range(1,len(h)):
        if h[i-1]==a[i-1]: tied[h[i-1]][h[i]]+=1
print('\nafter tie by tied hand (next R/P/S %):')
for k in [0,2,1]:
    m=sum(tied[k].values()); print('  tie on', NAME[k], 'n=',m, ' '.join(f"{NAME[j]} {tied[k][j]/m:.3f}" for j in [0,2,1]))
# 5 counterfactual rule edges vs human's actual next throw (relative to human's own previous hand, i.e., what an opponent facing this human would do)
def edge(rule, rng=lambda L: range(1,L)):
    w=l=0; t=0; per=[]
    for fn,h,a in players:
        pw=pl=pn=0
        for i in rng(len(h)):
            mine=rule(h[i-1], a[i-1])
            o=outcome(mine,h[i])
            if o=='win': w+=1; pw+=1
            elif o=='loss': l+=1; pl+=1
            t+=1; pn+=1
        if pn: per.append((pw-pl)/pn)
    m=sum(per)/len(per); se=math.sqrt(sum((x-m)**2 for x in per)/(len(per)-1))/math.sqrt(len(per))
    return (w-l)/t, m, se
rules = {
 "beat their last hand (X+)": lambda hx, ax: up(hx),
 "throw the hand their last hand beats (X-)": lambda hx, ax: down(hx),
 "copy their last hand (X)": lambda hx, ax: hx,
}
print('\ncounterfactual rules (opponent = these humans), pooled net and per-player mean (SE):')
for name, r in rules.items():
    for lab, rng in [('all', lambda L: range(1,L)), ('rounds 2-20', lambda L: range(1,min(20,L)))]:
        p,m,se = edge(r, rng); print(f'  {name:45s} {lab:12s} pooled {p:+.3f}  per-player {m:+.3f} ({se:.3f})')
# 6 second-order
so=collections.defaultdict(collections.Counter)
for fn,h,a in players:
    for i in range(2,len(h)):
        t1='stay' if h[i-1]==h[i-2] else ('up' if h[i-1]==up(h[i-2]) else 'down')
        t2='stay' if h[i]==h[i-1] else ('up' if h[i]==up(h[i-1]) else 'down')
        so[t1][t2]+=1
print('\nsecond-order:')
for t1 in ['stay','up','down']:
    m=sum(so[t1].values()); print('  after', t1, 'n=',m, ' '.join(f"{t2} {so[t1][t2]/m:.3f}" for t2 in ['stay','up','down']))
