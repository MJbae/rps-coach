from fractions import Fraction as F
import itertools
H=['R','P','S']
BEATS={('R','S'),('P','R'),('S','P')}
def u(a,b):  # payoff to a
    if a==b: return 0
    return 1 if (a,b) in BEATS else -1
def solve2x2(A):
    # zero-sum, row maximizer, A 2x2; return value, p(row0), q(col0) (check saddle first)
    # pure saddle
    for i in range(2):
        for j in range(2):
            if A[i][j]==min(A[i]) and A[i][j]==max(A[k][j] for k in range(2)):
                return F(A[i][j]), (F(1) if i==0 else F(0)), (F(1) if j==0 else F(0)), 'pure'
    a,b,c,d=A[0][0],A[0][1],A[1][0],A[1][1]
    den=a-b-c+d
    p=F(d-c,den); q=F(d-b,den); v=F(a*d-b*c,den)
    return v,p,q,'mixed'
pairs=[('R','P'),('R','S'),('P','S')]
print('RPS minus one: stage-2 subgames (row pair vs column pair)')
V={}
for X in pairs:
    for Y in pairs:
        A=[[u(x,y) for y in Y] for x in X]
        v,p,q,kind=solve2x2(A)
        V[(X,Y)]=v
        # outcome probs
        win=sum((p if i==0 else 1-p)*(q if j==0 else 1-q) for i in range(2) for j in range(2) if A[i][j]==1)
        tie=sum((p if i==0 else 1-p)*(q if j==0 else 1-q) for i in range(2) for j in range(2) if A[i][j]==0)
        print(f'  {X} vs {Y}: value {v} ({kind}); row keeps {X[0]} w.p. {p}, col keeps {Y[0]} w.p. {q}; row win {win}, tie {tie}, loss {1-win-tie}')
print('stage-1 value matrix (rows/cols = pairs):')
for X in pairs: print('  ', X, [str(V[(X,Y)]) for Y in pairs])
# check uniform stage-1 is equilibrium: each pure pair vs uniform gives 0
for X in pairs: print('  pair', X, 'vs uniform opponent:', sum(V[(X,Y)] for Y in pairs)/3)
# doubles
print('doubles: {R,R} vs pairs:', [str(min(u('R',y) for y in Y)) for Y in pairs], '(opponent best response)')
# Mukjjippa: attacker wins if same hand; otherwise winner of throw becomes attacker.
# attacker value V solves V = val(M) with M[a][d] = 1 if a==d else (V if attacker wins throw else 1-V)
import math
Vm=F(1,2)
for it in range(200):
    M=[[1 if a==d else (Vm if u(a,d)==1 else 1-Vm) for d in H] for a in H]
    # circulant -> uniform equilibrium value = average row
    rowvals=[sum(F(x) for x in row)/3 for row in M]
    Vm=rowvals[0]
print('Mukjjippa attacker equilibrium value (uniform play):', Vm, '; row values vs uniform defender:', [str(x) for x in rowvals])
# check: each defender pure response vs uniform attacker
cols=[sum(F(M[a][d]) for a in range(3))/3 for d in range(3)]
print('defender pure responses vs uniform attacker give attacker:', [str(c) for c in cols])
