import os, sys, collections
base = sys.argv[1]
H = os.path.join(base, 'Human_hand_data'); A = os.path.join(base, 'AI_hand_data')
def up(h): return (h-1)%3
def down(h): return (h+1)%3
def parse(p):
    toks=[t.strip() for t in open(p).read().replace('\r','').replace('\n',',').split(',')]
    return [int(t) for t in toks if t!='']
c1=collections.Counter(); c2=collections.Counter(); c2same=collections.Counter()
for fn in os.listdir(H):
    h=parse(os.path.join(H,fn)); a=parse(os.path.join(A,fn)); L=min(len(h),len(a)); h=h[:L]; a=a[:L]
    for i in range(2,L):
        if h[i-1]==a[i-1] and h[i-2]==a[i-2]:
            t='stay' if h[i]==h[i-1] else ('up' if h[i]==up(h[i-1]) else 'down'); c2[t]+=1
            if h[i-1]==h[i-2]: c2same[t]+=1
for name,c in [('after two consecutive ties (any hands)',c2),('after two consecutive ties on the same hand',c2same)]:
    n=sum(c.values()); print(name, 'n=',n, ' '.join(f'{k} {c[k]/n:.3f}' for k in ['stay','up','down']))
