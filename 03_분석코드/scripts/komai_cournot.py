import os, sys, math, collections
base = sys.argv[1]
H = os.path.join(base, 'Human_hand_data'); A = os.path.join(base, 'AI_hand_data')
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
c=collections.Counter(); per=[]
for h,a in players:
    loc=collections.Counter()
    for i in range(1,len(h)):
        rel='copy' if h[i]==a[i-1] else ('beat' if h[i]==up(a[i-1]) else 'lose')
        c[rel]+=1; loc[rel]+=1
    n=sum(loc.values()); per.append({k:loc[k]/n for k in ['copy','beat','lose']})
n=sum(c.values())
print('human next hand relative to AI previous hand: copy %.3f beat (Cournot) %.3f lose %.3f (n=%d)' % (c['copy']/n, c['beat']/n, c['lose']/n, n))
# counterfactual: an opponent who throws the hand its OWN previous hand beats (self-downgrade), where 'own previous' = AI's previous hand
W=L=N=0; pp=[]
for h,a in players:
    w=l=k=0
    for i in range(1,len(h)):
        mine=down(a[i-1]); r=outcome(mine,h[i]); k+=1; w+=r=='win'; l+=r=='loss'
    pp.append((w-l)/k); W+=w; L+=l; N+=k
m=sum(pp)/len(pp); se=math.sqrt(sum((x-m)**2 for x in pp)/(len(pp)-1))/math.sqrt(len(pp))
print('self-downgrade rule (throw what your own last hand beats) vs these humans: pooled %+.3f per-player %+.3f (SE %.3f)' % ((W-L)/N, m, se))
