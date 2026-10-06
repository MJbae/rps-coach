"""Everyone-vs-host elimination: P(at least one team member survives k rounds).
Host throws uniformly at random each round (independent of the team).
Rule A: only members who BEAT the host survive (ties and losses eliminated).
Rule B: members who beat OR tie the host survive (only losers eliminated).
Strategies:
  indep   : each surviving member throws uniformly at random, independently.
  even    : survivors split as evenly as possible across R/P/S every round.
  optimal : allocation (a,b,c) chosen each round by dynamic programming to maximise P(>=1 survivor after k rounds).
Also: same-hand (everyone throws the same hand) for contrast.
"""
from fractions import Fraction as F
from functools import lru_cache

def splits(m):
    for a in range(m + 1):
        for b in range(m - a + 1):
            yield (a, b, m - a - b)

def even_split(m):
    q, r = divmod(m, 3)
    return tuple(q + (1 if i < r else 0) for i in range(3))

@lru_cache(None)
def V(rule, strat, m, k):
    if m == 0:
        return F(0)
    if k == 0:
        return F(1)
    def val(alloc):
        a = alloc
        if rule == 'A':
            # host hand h; survivors = members on the hand that beats h -> each of the three groups survives w.p. 1/3
            return sum(V(rule, strat, a[i], k - 1) for i in range(3)) / 3
        else:
            # survivors = m - (members on the hand that loses to h) -> each group eliminated w.p. 1/3
            return sum(V(rule, strat, m - a[i], k - 1) for i in range(3)) / 3
    if strat == 'even':
        return val(even_split(m))
    if strat == 'same':
        return val((m, 0, 0))
    if strat == 'optimal':
        return max(val(s) for s in splits(m))
    raise ValueError

def indep(rule, m, k):
    s = F(1, 3) if rule == 'A' else F(2, 3)
    return 1 - (1 - s**k) ** m

for rule in ['A', 'B']:
    print(f"\n=== Rule {rule} ({'only winners survive' if rule=='A' else 'winners and ties survive'}) ===")
    print("n  k | indep   even    optimal  same-hand")
    for n in [3, 5, 10, 20]:
        for k in [1, 2, 3, 4, 5]:
            pi = float(indep(rule, n, k))
            pe = float(V(rule, 'even', n, k))
            po = float(V(rule, 'optimal', n, k))
            ps = float(V(rule, 'same', n, k))
            print(f"{n:2d} {k} | {pi:.4f}  {pe:.4f}  {po:.4f}   {ps:.4f}")
