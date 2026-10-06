"""All-simultaneous team-vs-team RPS (Cho 2019 rule II and Cho 2010 rule I).
Team A uses a strategy type each round; team B members throw independently uniformly.
Compute P(A wins) exactly by recursion over remaining team sizes (ties replay).
Strategy types for A: 'indep' (independent uniform), 'same' (all members same hand, hand uniform),
'split2' (members spread over as many hands as possible, at most 2 distinct hands, random labels).
"""
from itertools import product, permutations
from fractions import Fraction as F
from functools import lru_cache

def beats(a, b):
    return (a - b) % 3 == 1

def a_profiles(m, strat):
    """Return dict profile(tuple)->prob for team A of size m."""
    out = {}
    if strat == 'indep':
        for p in product(range(3), repeat=m):
            out[p] = out.get(p, 0) + F(1, 3**m)
    elif strat == 'same':
        for h in range(3):
            out[(h,)*m] = out.get((h,)*m, 0) + F(1, 3)
    elif strat == 'split2':
        # use two distinct hands (ordered pair uniformly), members alternate between them
        pairs = [(x, y) for x in range(3) for y in range(3) if x != y]
        for (x, y) in pairs:
            prof = tuple(x if i % 2 == 0 else y for i in range(m)) if m > 1 else (x,)
            out[prof] = out.get(prof, 0) + F(1, len(pairs))
    return out

def round_dist(m, n, strat):
    res = {}
    for pa, wa_p in a_profiles(m, strat).items():
        for pb in product(range(3), repeat=n):
            p = wa_p * F(1, 3**n)
            s = set(pa) | set(pb)
            if len(s) != 2:
                key = ('tie',)
            else:
                x, y = tuple(s)
                w = x if beats(x, y) else y
                key = ('dec', sum(1 for h in pa if h == w), sum(1 for h in pb if h == w))
            res[key] = res.get(key, 0) + p
    return res

def solve(rule, strat):
    @lru_cache(None)
    def P(m, n):
        d = round_dist(m, n, strat)
        tie = d.get(('tie',), F(0))
        if tie == 1:
            return None  # never resolves
        acc = F(0)
        for k, p in d.items():
            if k[0] != 'dec':
                continue
            _, wa, wb = k
            if rule == 'II':
                if wa > 0 and wb == 0:
                    acc += p
                elif wa > 0 and wb > 0:
                    sub = P(wa, wb)
                    if sub is None:
                        return None
                    acc += p * sub
            else:  # rule I: more winners wins; equal -> winners continue
                if wa > wb:
                    acc += p
                elif wa == wb:
                    sub = P(wa, wb)
                    if sub is None:
                        return None
                    acc += p * sub
        return acc / (1 - tie)
    return P

for rule in ['II', 'I']:
    for strat in ['indep', 'same', 'split2']:
        P = solve(rule, strat)
        vals = []
        for (m, n) in [(2, 2), (3, 3)]:
            v = P(m, n)
            vals.append(f"{m}v{n}: {('never resolves' if v is None else round(float(v), 4))}")
        print(f"rule {rule:2s} A={strat:6s} vs B=indep -> " + " | ".join(vals))
