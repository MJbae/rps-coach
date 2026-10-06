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
rules={'X+ (beat their last hand)': up, 'X (copy their last hand)': lambda x:x, 'X- (hand their last hand beats)': down}
for lo,hi,lab in [(1,50,'rounds 2-50'),(1,10,'rounds 2-10')]:
    print('==',lab)
    for o in ['win','tie','loss']:
        for rn, r in rules.items():
            W=L=N=0; per=[]
            for h,a in players:
                w=l=n=0
                for i in range(lo, min(hi,len(h))):
                    if outcome(h[i-1],a[i-1])!=o: continue
                    res=outcome(r(h[i-1]), h[i]); n+=1; w+=res=='win'; l+=res=='loss'
                if n: per.append((w-l)/n); W+=w; L+=l; N+=n
            m=sum(per)/len(per); se=math.sqrt(sum((x-m)**2 for x in per)/(len(per)-1))/math.sqrt(len(per))
            print(f'  opponent {o:4s} -> {rn:32s} pooled {(W-L)/N:+.3f} per-player {m:+.3f} (SE {se:.3f}) n={N}')
