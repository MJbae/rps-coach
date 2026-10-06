"""Sensitivity: host with Yoshizawa live marginals (R/P/S = 4054/3849/3664 of 11567); ordered splits."""
from fractions import Fraction as Fr
from functools import lru_cache
host = (Fr(4054, 11567), Fr(3849, 11567), Fr(3664, 11567))  # slots: 0=R, 1=P (beats R), 2=S (beats P)
def comps(m):
    for a in range(m + 1):
        for b in range(m + 1 - a):
            yield (a, b, m - a - b)
def evens(m):
    base, r = divmod(m, 3)
    out = set()
    for c in comps(m):
        if max(c) - min(c) <= 1: out.add(c)
    return out
for rule in ("A", "B"):
    @lru_cache(None)
    def Vopt(k, m):
        if m == 0: return Fr(0)
        if k == 0: return Fr(1)
        return max(val(k, m, a, Vopt) for a in comps(m))
    @lru_cache(None)
    def Vev(k, m):  # best-labelled even split each round
        if m == 0: return Fr(0)
        if k == 0: return Fr(1)
        return max(val(k, m, a, Vev) for a in evens(m))
    def val(k, m, a, V):
        tot = Fr(0)
        for i in range(3):
            beat = a[(i + 1) % 3]; lose = a[(i + 2) % 3]
            surv = beat if rule == "A" else m - lose
            tot += host[i] * V(k - 1, surv)
        return tot
    print(f"Rule {rule}:", "; ".join(f"n={n},k={k}: even {float(Vev(k,n)):.4f} / best {float(Vopt(k,n)):.4f}"
                                     for n, k in ((3, 2), (5, 2), (5, 3), (10, 3), (20, 3), (10, 5))))
