"""Exact verification of Cho (2010, 2019) expected numbers of RPS games between two teams.
Rule II (Cho 2019): all m+n play; if decisive and winners only on one team -> that team wins;
 if winners on both teams -> only winners continue; ties (all same or all three hands) -> replay.
Rule I (Cho 2010): team with more winners wins; equal winners -> winners continue.
"""
from itertools import product
from fractions import Fraction as F
from functools import lru_cache

def beats(a, b):  # 0=R,1=P,2=S ; a beats b?
    return (a - b) % 3 == 1

def outcomes(m, n):
    """Yield (prob, winnersA, winnersB, decisive) for one simultaneous round."""
    tot = 3 ** (m + n)
    res = {}
    for combo in product(range(3), repeat=m + n):
        s = set(combo)
        if len(s) != 2:
            key = ('tie',)
        else:
            a, b = tuple(s)
            win = a if beats(a, b) else b
            wa = sum(1 for x in combo[:m] if x == win)
            wb = sum(1 for x in combo[m:] if x == win)
            key = ('dec', wa, wb)
        res[key] = res.get(key, 0) + 1
    return {k: F(v, tot) for k, v in res.items()}

@lru_cache(None)
def E_rule2(m, n):
    o = outcomes(m, n)
    p_tie = o.get(('tie',), F(0))
    acc = F(1)
    for k, p in o.items():
        if k[0] == 'dec':
            _, wa, wb = k
            if wa > 0 and wb > 0:
                acc += p * E_rule2(wa, wb)
    return acc / (1 - p_tie)

@lru_cache(None)
def E_rule1(m, n):
    o = outcomes(m, n)
    p_tie = o.get(('tie',), F(0))
    acc = F(1)
    for k, p in o.items():
        if k[0] == 'dec':
            _, wa, wb = k
            if wa == wb:
                acc += p * E_rule1(wa, wb)
    return acc / (1 - p_tie)

for (m, n) in [(1,1),(2,1),(2,2),(3,1),(3,2),(3,3)]:
    e = E_rule2(m, n)
    print('Rule II', (m, n), e, float(e))
for N in [1, 2, 3]:
    e = E_rule1(N, N)
    print('Rule I', (N, N), e, float(e))
