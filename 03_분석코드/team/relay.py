"""Winner-stays relay (승자 연전 / kachinuki): two teams of n; each bout eliminates the loser,
the winner stays; team wins when the other team runs out of players.
If each bout is won by our side with constant probability p (ties replayed), our team wins iff
we win n bouts before losing n bouts  ==  P(Binomial(2n-1, p) >= n)  (same as a best-of-(2n-1) series).
Also: per-bout p from per-throw win/lose rates with ties replayed: p = w/(w+l).
Also: points format (each pair plays once, n odd): P(Binomial(n,p) > n/2) -- identical formula for n odd? no: Bin(n,p)>=ceil(n/2).
Also: Monte Carlo check of the relay formula and an ordering check with heterogeneous strengths.
"""
from math import comb
import random

def relay_exact(n, p):
    N = 2 * n - 1
    return sum(comb(N, j) * p**j * (1 - p)**(N - j) for j in range(n, N + 1))

def points_exact(n, p):
    need = n // 2 + 1
    return sum(comb(n, j) * p**j * (1 - p)**(n - j) for j in range(need, n + 1))

def relay_mc(n, p, trials=200000, seed=1):
    rng = random.Random(seed)
    wins = 0
    for _ in range(trials):
        a = b = n
        while a and b:
            if rng.random() < p:
                b -= 1
            else:
                a -= 1
        wins += (b == 0)
    return wins / trials

print("Winner-stays relay: P(team wins) by team size n and per-bout win prob p")
print("n  | p=0.50  0.52    0.55    0.60")
for n in [1, 3, 5, 7]:
    row = [relay_exact(n, p) for p in [0.50, 0.52, 0.55, 0.60]]
    print(f"{n:2d} | " + "  ".join(f"{x:.4f}" for x in row))
print("MC check n=5,p=0.55:", relay_mc(5, 0.55), "exact", round(relay_exact(5, 0.55), 4))

print("\nPoints format (each pair plays once; majority of n bouts):")
for n in [3, 5, 7]:
    row = [points_exact(n, p) for p in [0.50, 0.52, 0.55, 0.60]]
    print(f"{n:2d} | " + "  ".join(f"{x:.4f}" for x in row))

print("\nBest-of-3 single representative (first to 2 decisive wins): p^2(3-2p)")
for p in [0.50, 0.511, 0.52, 0.55, 0.60, 0.6035]:
    print(p, round(p*p*(3-2*p), 4))

# per-throw rates from Batzilis et al. (2019) Table 5 (first throws): experienced 34.66/32.17/33.17 ; best response 41.66/30.97/27.37
for label, w, l in [("experienced", 34.66, 33.17), ("best-response-to-predicted", 41.66, 27.37)]:
    p = w / (w + l)
    print(label, "per decisive bout p =", round(p, 4), "| relay n=5:", round(relay_exact(5, p), 4), "| best-of-3:", round(p*p*(3-2*p), 4))

# Heterogeneous strengths: does order matter in winner-stays relay?
from functools import lru_cache
def relay_het(order_A, order_B, pmat):
    @lru_cache(None)
    def f(i, j):  # i: index of current A player, j: index of current B player
        if i == len(order_A):
            return 0.0
        if j == len(order_B):
            return 1.0
        p = pmat[(order_A[i], order_B[j])]
        return p * f(i, j + 1) + (1 - p) * f(i + 1, j)
    return f(0, 0)
import itertools
# example: A has one strong player 'S' (p=0.6 vs anyone) and two average 'a1','a2' (p=0.5); B all average
pm = {}
for x in ['S', 'a1', 'a2']:
    for y in ['b1', 'b2', 'b3']:
        pm[(x, y)] = 0.6 if x == 'S' else 0.5
for order in itertools.permutations(['S', 'a1', 'a2']):
    print("order", order, round(relay_het(order, ('b1', 'b2', 'b3'), pm), 4))
