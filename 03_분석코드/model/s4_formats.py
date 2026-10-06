"""Item 4: format amplification of a per-decisive-throw win probability q."""
from math import comb
from functools import lru_cache

def atleast(n, k, p):
    return sum(comb(n, i) * p**i * (1-p)**(n-i) for i in range(k, n+1))
def bo(q, n):  # best-of-n (first to (n+1)/2), ties replayed
    return atleast(n, (n+1)//2, q)
def relay(q, n):
    @lru_cache(None)
    def P(i, j):  # i of ours left, j of theirs left; each bout we win w.p. q; loser eliminated, winner stays
        if j == 0: return 1.0
        if i == 0: return 0.0
        return q * P(i, j-1) + (1-q) * P(i-1, j)
    return P(n, n)

Q = [0.50, 0.52, 0.55, 0.60]
print("| q (P win a decisive throw) | 1 decisive throw | Bo3 | Bo5 | relay n=3 | relay n=5 | relay n=7 | 5-member points, 1-throw bouts | 5-member points, Bo3 bouts | 5-member points, Bo5 bouts |")
for q in Q:
    r = [relay(q, n) for n in (3, 5, 7)]
    chk = [atleast(2*n-1, n, q) for n in (3, 5, 7)]
    assert all(abs(a-b) < 1e-12 for a, b in zip(r, chk))
    print(f"| {q:.2f} | {q:.3f} | {bo(q,3):.3f} | {bo(q,5):.3f} | {r[0]:.3f} | {r[1]:.3f} | {r[2]:.3f} | "
          f"{atleast(5,3,q):.3f} | {atleast(5,3,bo(q,3)):.3f} | {atleast(5,3,bo(q,5)):.3f} |")
print("(relay DP == P(Bin(2n-1,q) >= n) verified to 1e-12)")
print("\nExtra: 3-member points with Bo3 bouts (PBR Indy format, team:C3):",
      ", ".join(f"q={q:.2f}: {atleast(3,2,bo(q,3)):.3f}" for q in Q))

# Bridge: per-throw edge e (win-loss over all throws) with tie rate t -> q
def q_from(e, t): return 0.5 + e / (2 * (1 - t))
print("\nBridge from per-throw edge to q (q = 1/2 + e/(2(1-t))):")
for label, e, t in [("Batzilis experienced players, realised first throws (34.66/32.17/33.17)", 0.0149, 0.3217),
                    ("Batzilis best response to predicted play (41.66/30.97/27.37)", 0.1429, 0.3097),
                    ("Persistent Rock bias, always Paper vs Moerel all-throws (35.3/32.5/32.1)", 0.3534-0.3212, 0.3254),
                    ("Persistent bias, always Paper vs Xu 2013 (35.7/32.1/32.2)", (7702-6961)/21600, 6937/21600)]:
    q = q_from(e, t)
    print(f"  {label}: e={e*100:+.2f}pp, t={t*100:.1f}% -> q={q:.4f}; Bo3 {bo(q,3):.3f}; Bo5 {bo(q,5):.3f}; relay5 {relay(q,5):.3f}; points5(Bo3) {atleast(5,3,bo(q,3)):.3f}")

# First-throw-only edge (later throws fair)
print("\nFirst-throw-only edge e1 (all later throws fair): Bo3 = 0.5 + 0.25*e1 ; Bo5 = 0.5 + 0.1875*e1 (derived)")
for label, e1 in [("Paper vs Batzilis full first throws", 0.3399-0.3120), ("Scissors vs Batzilis experienced", 0.3456-0.3260),
                  ("Paper vs Eyler novices (n=119)", (66-14)/119)]:
    # verify by exact DP: first throw W1/T1/L1 arbitrary split; P = W1*0.75 + T1*0.5 + L1*0.25
    print(f"  {label}: e1={e1*100:+.1f}pp -> Bo3 {0.5+0.25*e1:.3f}, Bo5 {0.5+0.1875*e1:.3f}")
# check Bo5 coefficients exactly
p10 = atleast(4, 2, 0.5); p01 = atleast(4, 3, 0.5)
print(f"  check: P(win Bo5 | 1-0)={p10:.4f}, P(win Bo5 | 0-1)={p01:.4f} -> coefficient {(p10-p01)/2:.4f}")
