# hands: 0=R,1=P,2=S ; payoff A[i][j] for me playing i vs opp j
A=[[0,-1,1],[1,0,-1],[-1,1,0]]
q=(0.36,0.32,0.32)
def ev(x,q): return sum(x[i]*q[j]*A[i][j] for i in range(3) for j in range(3))
def expl(x): return max(-sum(x[i]*A[i][j] for i in range(3)) for j in range(3))
N=600
best={}
for a in range(N+1):
    for b in range(N+1-a):
        x=(a/N,b/N,(N-a-b)/N)
        e=round(expl(x),3); v=ev(x,q)
        for eps in (0.05,0.1,0.25,1/3,0.5,1.0):
            if expl(x)<=eps+1e-9:
                if v>best.get(eps,(-9,None))[0]: best[eps]=(v,x)
for eps,(v,x) in sorted(best.items()):
    print(f"eps={eps:.3f} maxEV={v*100:.2f}pp at x(R,P,S)={tuple(round(t,3) for t in x)}")
for x in ((0,1,0),(0.25,0.5,0.25),(0.3,0.4,0.3),(1/3,0.5,1/6),(1/3,0.4,4/15)):
    print(x, 'EV pp', round(ev(x,q)*100,2), 'expl pp', round(expl(x)*100,2))
