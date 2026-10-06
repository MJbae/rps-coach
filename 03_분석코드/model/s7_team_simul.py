"""Supplement: simultaneous team-vs-team (all members throw at once), Cho rules I and II (team:C6/MF1 cross-check)."""
import itertools
from fractions import Fraction as F
from functools import lru_cache

def comp_dist(a, strat):
    """Distribution over our multiset of hands (tuple of counts per hand 0,1,2), hand h+1 beats h."""
    out = {}
    def add(c, p):
        out[c] = out.get(c, 0) + p
    if a == 0:
        add((0, 0, 0), F(1)); return out
    if strat == "IND" or a == 1:
        for prof in itertools.product(range(3), repeat=a):
            c = [0, 0, 0]
            for h in prof: c[h] += 1
            add(tuple(c), F(1, 3**a))
        return out
    for X in range(3):
        c = [0, 0, 0]
        if strat == "HERD":
            c[X] = a
        else:
            c[X] = a - 1
            if strat == "BEAT":    # one on X- (the hand X beats)
                c[(X + 2) % 3] += 1
            elif strat == "LOSE":  # one on X+ (the hand that beats X)
                c[(X + 1) % 3] += 1
            elif strat == "SPLITR":  # one on a random other hand
                for o in (1, 2):
                    cc = list(c); cc[(X + o) % 3] += 1
                    add(tuple(cc), F(1, 6))
                continue
        add(tuple(c), F(1, 3))
    return out

def solve(strat, opp, rule, A, B):
    @lru_cache(None)
    def P(a, b):
        ours = comp_dist(a, strat); theirs = comp_dist(b, opp)
        win = F(0); self_p = F(0); rest = F(0)
        for co, po in ours.items():
            for ct, pt in theirs.items():
                p = po * pt
                shown = [h for h in range(3) if co[h] + ct[h] > 0]
                if len(shown) != 2:
                    self_p += p; continue
                h1, h2 = shown
                w = h2 if (h2 - h1) % 3 == 1 else h1  # winning hand
                wa, wb = co[w], ct[w]
                if rule == "I":
                    if wa > wb: win += p
                    elif wa == wb:
                        if (wa, wb) == (a, b): self_p += p
                        else: rest += p * P(wa, wb)
                else:  # rule II
                    if wb == 0: win += p
                    elif wa == 0: pass
                    else:
                        if (wa, wb) == (a, b): self_p += p
                        else: rest += p * P(wa, wb)
        return (win + rest) / (1 - self_p)
    return P(A, B)

for rule in ("I", "II"):
    for n in (2, 3, 4):
        row = []
        for s in ("BEAT", "LOSE", "SPLITR", "HERD", "IND"):
            v = solve(s, "IND", rule, n, n)
            row.append(f"{s} {float(v):.4f}" + (f" ({v})" if n == 3 and s == "BEAT" else ""))
        print(f"Rule {rule}, {n}v{n} vs independent-random team: " + ", ".join(row))
    v = solve("BEAT", "HERD", rule, 3, 3)
    print(f"Rule {rule}, 3v3 BEAT vs HERD team: {float(v):.4f}")
