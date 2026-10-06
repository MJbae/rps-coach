"""Verify n-player RPS decisive-round probability and expected rounds.
Hands: 0=Rock,1=Paper,2=Scissors; h beats (h-1)%3, i.e., Paper(1) beats Rock(0), Scissors(2) beats Paper(1), Rock(0) beats Scissors(2).
"""
from itertools import product
from fractions import Fraction as F
from math import comb

def decisive_bruteforce(n):
    cnt = 0
    for combo in product(range(3), repeat=n):
        if len(set(combo)) == 2:
            cnt += 1
    return F(cnt, 3**n)

def decisive_formula(n):
    return F(3*(2**n - 2), 3**n)

print("n | P(decisive) brute | formula | float | E[rounds until decisive]=1/q")
for n in range(2, 9):
    b = decisive_bruteforce(n)
    f = decisive_formula(n)
    assert b == f
    print(n, b, f, float(f), float(1/f))
for n in [10, 12, 15, 20]:
    f = decisive_formula(n)
    print(n, "formula only", float(f), "E rounds to first decisive:", round(float(1/f), 2))

# Expected total rounds W_n until a single winner remains (losers retire each decisive round)
# P(I_n=j) = 3*C(n,j)/3^n for 1<=j<=n-1 ; tie prob = 1 - 3(2^n-2)/3^n
EW = {1: F(0)}
for n in range(2, 31):
    tie = 1 - decisive_formula(n)
    s = sum(F(3*comb(n, j), 3**n) * EW[j] for j in range(1, n))
    EW[n] = (1 + s) / (1 - tie)
print("\nn | E[W_n] exact | (1/3)(3/2)^n asymptotic")
for n in [2, 3, 4, 5, 6, 7, 8, 10, 12, 15, 20, 25, 30]:
    print(n, round(float(EW[n]), 3), round((1/3)*(1.5**n), 3))
