"""2v2 all-simultaneous RPS under Cho's rule II: team strategies 'same' (both members same hand) vs 'diff' (two different hands),
labels uniformly random; subgames with a single member on a side: that member uniform; a side with 2 members keeps its strategy.
Compute P(A wins) matrix for A in {same, diff, indep} x B in {same, diff, indep}.
"""
from itertools import product
from fractions import Fraction as F
from functools import lru_cache

def beats(a, b):
    return (a - b) % 3 == 1

def profiles(m, strat):
    out = {}
    if m == 1 or strat == 'indep':
        for p in product(range(3), repeat=m):
            out[p] = out.get(p, 0) + F(1, 3**m)
    elif strat == 'same':
        for h in range(3):
            out[(h,)*m] = out.get((h,)*m, 0) + F(1, 3)
    elif strat == 'diff':
        pairs = [(x, y) for x in range(3) for y in range(3) if x != y]
        for (x, y) in pairs:
            prof = tuple(x if i % 2 == 0 else y for i in range(m))
            out[prof] = out.get(prof, 0) + F(1, len(pairs))
    return out

def make(sa, sb):
    @lru_cache(None)
    def P(m, n):
        res = {}
        for pa, qa in profiles(m, sa).items():
            for pb, qb in profiles(n, sb).items():
                p = qa * qb
                s = set(pa) | set(pb)
                if len(s) != 2:
                    key = ('tie',)
                else:
                    x, y = tuple(s)
                    w = x if beats(x, y) else y
                    key = ('dec', sum(h == w for h in pa), sum(h == w for h in pb))
                res[key] = res.get(key, 0) + p
        tie = res.get(('tie',), F(0))
        acc = F(0)
        for k, p in res.items():
            if k[0] != 'dec':
                continue
            _, wa, wb = k
            if wa > 0 and wb == 0:
                acc += p
            elif wa > 0 and wb > 0:
                acc += p * P(wa, wb)
        return acc / (1 - tie)
    return P

strats = ['same', 'diff', 'indep']
print("P(A wins), 2v2, rule II")
print("A\\B   " + "  ".join(f"{s:>7s}" for s in strats))
for sa in strats:
    print(f"{sa:6s}" + "  ".join(f"{float(make(sa, sb)(2, 2)):7.4f}" for sb in strats))
