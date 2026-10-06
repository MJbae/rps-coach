import os, sys, math, collections
base = sys.argv[1]
H = os.path.join(base, 'Human_hand_data'); A = os.path.join(base, 'AI_hand_data')
NAME = {0:'R',1:'S',2:'P'}
def beats(a,b): return (a+1)%3==b
def up(h): return (h-1)%3
def down(h): return (h+1)%3
def outcome(me, op):
    if me==op: return 'tie'
    return 'win' if beats(me,op) else 'loss'
def parse(p):
    toks=[t.strip() for t in open(p).read().replace('\r','').replace('\n',',').split(',')]
    return [int(t) for t in toks if t!='']
players=[]
for fn in os.listdir(H):
    h=parse(os.path.join(H,fn)); a=parse(os.path.join(A,fn)); L=min(len(h),len(a)); players.append((h[:L],a[:L]))
# AI net per player
nets=[]
for h,a in players:
    w=sum(1 for x,y in zip(a,h) if outcome(x,y)=='win'); l=sum(1 for x,y in zip(a,h) if outcome(x,y)=='loss'); nets.append((w-l)/len(h))
m=sum(nets)/len(nets); se=math.sqrt(sum((x-m)**2 for x in nets)/(len(nets)-1))/math.sqrt(len(nets))
print('AI net per throw vs humans: %+.4f (SE %.4f), AI ahead in %d of %d sessions, behind in %d' % (m,se,sum(1 for x in nets if x>0),len(nets),sum(1 for x in nets if x<0)))
# throws 1..5 marginals
for t in range(5):
    c=collections.Counter(h[t] for h,a in players); n=sum(c.values())
    print('throw', t+1, ' '.join(f'{NAME[k]} {c[k]/n:.3f}' for k in [0,2,1]), 'n', n)
# per-hand after win / loss: next hand
for o in ['win','loss']:
    tab=collections.defaultdict(collections.Counter)
    for h,a in players:
        for i in range(1,len(h)):
            if outcome(h[i-1],a[i-1])==o: tab[h[i-1]][h[i]]+=1
    print('after', o, 'by own hand (next R/P/S):')
    for k in [0,2,1]:
        n=sum(tab[k].values()); print('   with', NAME[k], 'n=',n, ' '.join(f'{NAME[j]} {tab[k][j]/n:.3f}' for j in [0,2,1]))
# opening EV per hand vs first-throw distribution
c=collections.Counter(h[0] for h,a in players); n=sum(c.values()); p={k:c[k]/n for k in range(3)}
for k in range(3):
    ev = p[down(k)] - p[up(k)]  # wins vs the hand k beats, loses vs the hand that beats k
    print('open with', NAME[k], 'EV vs first-throw mix %+.3f' % ev)
# bootstrap CI for first-throw paper share
import random
random.seed(1)
firsts=[h[0] for h,a in players]
bs=sorted(sum(1 for x in random.choices(firsts,k=len(firsts)) if x==2)/len(firsts) for _ in range(4000))
print('first-throw Paper share 95%% CI %.3f-%.3f' % (bs[100], bs[3899]))
# rounds 2-10 rule edge (short-bout horizon)
def edge(rule, lo, hi):
    per=[]
    for h,a in players:
        w=l=n=0
        for i in range(lo, min(hi,len(h))):
            o=outcome(rule(h[i-1]), h[i]); n+=1
            w+= o=='win'; l+= o=='loss'
        per.append((w-l)/n)
    m=sum(per)/len(per); se=math.sqrt(sum((x-m)**2 for x in per)/(len(per)-1))/math.sqrt(len(per)); return m,se
print('rounds 2-10: X- rule %+.3f (SE %.3f); X+ rule %+.3f (SE %.3f)' % (*edge(down,1,10), *edge(up,1,10)))
