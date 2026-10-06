import itertools, random
from functools import lru_cache
def relay_het(order_A, order_B, pmat):
    @lru_cache(None)
    def f(i, j):
        if i == len(order_A):
            return 0.0
        if j == len(order_B):
            return 1.0
        p = pmat[(order_A[i], order_B[j])]
        return p * f(i, j + 1) + (1 - p) * f(i + 1, j)
    return f(0, 0)

A = ['x1', 'x2', 'x3']; B = ['y1', 'y2', 'y3']
# Case 1: matchup-specific edge: x1 has scouted y1 (p=0.65 vs y1), all else 0.5
pm = {(a, b): 0.5 for a in A for b in B}
pm[('x1', 'y1')] = 0.65
print("Case1 (x1 edge only vs y1; B order fixed y1,y2,y3):")
for o in itertools.permutations(A):
    print(' ', o, round(relay_het(o, tuple(B), pm), 4))
print("  If B order unknown (avg over B permutations):")
for o in itertools.permutations(A):
    vals = [relay_het(o, ob, pm) for ob in itertools.permutations(B)]
    print(' ', o, round(sum(vals) / len(vals), 4))
# Case 2: random Bradley-Terry strengths -> check order invariance
rng = random.Random(3)
sa = {a: rng.uniform(0.5, 2) for a in A}; sb = {b: rng.uniform(0.5, 2) for b in B}
pmbt = {(a, b): sa[a] / (sa[a] + sb[b]) for a in A for b in B}
print("Case2 Bradley-Terry strengths:")
for o in itertools.permutations(A):
    print(' ', o, round(relay_het(o, tuple(B), pmbt), 6))
# Case 3: arbitrary matrix
pmr = {(a, b): rng.uniform(0.3, 0.7) for a in A for b in B}
print("Case3 arbitrary matchup matrix:")
for o in itertools.permutations(A):
    print(' ', o, round(relay_het(o, tuple(B), pmr), 4))
