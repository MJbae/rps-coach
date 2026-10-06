"""Item 5: team vs host elimination; and P(decisive simultaneous round)."""
import itertools
from fractions import Fraction as F
from functools import lru_cache

# ---- decisive-round probability ----
print("| n players | P(decisive) closed form 3(2^n-2)/3^n | enumeration | expected throws to first decisive round |")
for n in range(2, 11):
    cf = F(3 * (2**n - 2), 3**n)
    cnt = sum(1 for prof in itertools.product(range(3), repeat=n) if len(set(prof)) == 2)
    en = F(cnt, 3**n)
    assert cf == en
    print(f"| {n} | {float(cf):.4f} ({cf}) | {float(en):.4f} | {float(1/cf):.2f} |")

# ---- host game ----
def splits(m):
    for a in range(m + 1):
        for b in range(a, m + 1 - a):
            c = m - a - b
            if c >= b:
                yield (a, b, c)

def even(m):
    base, r = divmod(m, 3)
    return tuple(sorted([base + (1 if i < r else 0) for i in range(3)]))

def make(rule, host=(F(1,3),)*3):
    # host = probabilities that the host's hand is beaten by our slot 0,1,2 (rule A survivors) -- for uniform host any labeling
    @lru_cache(None)
    def V_even(k, m):
        if m == 0: return F(0)
        if k == 0: return F(1)
        a = even(m)
        return val(k, m, a, V_even)
    @lru_cache(None)
    def V_opt(k, m):
        if m == 0: return F(0)
        if k == 0: return F(1)
        best = max(val(k, m, a, V_opt) for a in splits(m))
        return best
    def val(k, m, a, V):
        # slots: counts on hands h0,h1,h2 where h_{i+1} beats h_i (cyclic). Host plays hand H with prob host[...]
        # Rule A: survivors = those on the hand that beats H. Rule B: survivors = m - those on the hand that H beats.
        tot = F(0)
        for i in range(3):  # host's hand index i
            ph = host[i]
            beat = a[(i + 1) % 3]     # our members on the hand that beats host hand i
            lose = a[(i + 2) % 3]     # our members on the hand host hand i beats  (i beats i-1 == i+2)
            surv = beat if rule == "A" else m - lose
            tot += ph * V(k - 1, surv)
        return tot
    return V_even, V_opt

for rule in ("A", "B"):
    V_even, V_opt = make(rule)
    print(f"\nRule {rule} ({'only winners survive' if rule=='A' else 'winners and ties survive'}): P(at least one member survives k rounds) vs uniform random host")
    print("| team n | k | independent random | coordinated even split | optimal (DP over all splits) | herding (all same hand) | gain even-indep (pp) | expected survivors (any strategy) |")
    for n in (3, 5, 10, 20):
        for k in range(1, 6):
            s = F(1, 3) if rule == "A" else F(2, 3)
            ind = 1 - (1 - s**k)**n
            ev = V_even(k, n); op = V_opt(k, n); hd = s**k
            assert ev == op, (rule, n, k, ev, op)
            print(f"| {n} | {k} | {float(ind):.3f} | {float(ev):.3f} | {float(op):.3f} | {float(hd):.3f} | {float(ev-ind)*100:+.1f} | {float(n*s**k):.3f} |")
print("\n(even split == DP optimum in every cell: asserted)")

# Sensitivity: biased host (Yoshizawa live marginals R .3505 / P .3328 / S .3168), rule A
from fractions import Fraction
host_rps = (Fraction(4054, 11567), Fraction(3849, 11567), Fraction(3664, 11567))  # R, P, S
# order slots so that h_{i+1} beats h_i : R(0) -> P(1) beats R -> S(2) beats P -> R beats S  OK
for rule in ("A", "B"):
    V_even_b, V_opt_b = make(rule, host=host_rps)
    # for a biased host, even split labeling matters: try all labelings of the even split
    print(f"\nBiased host (Yoshizawa R/P/S 35.0/33.3/31.7), rule {rule}:")
    for n, k in ((5, 2), (10, 2), (10, 3), (20, 3)):
        print(f"  n={n}, k={k}: even split {float(V_even_b(k, n)):.4f} vs best split {float(V_opt_b(k, n)):.4f} "
              f"(uniform host even split {float(make(rule)[0](k, n)):.4f})")
