"""Item 3: best response after a tie on X (edges of X+, X, X- relative to the tied hand)."""
import math
from data import TIE, TIE_BOOT, TIE_N, TIE_HAND, YOSHIZAWA_REPEAT
from markov import edges, norm, NAME
Z = 1.959964
print("| After-tie data | src | stay/up/down % | X+ (beat tied hand) | X (repeat tied hand) | X- (hand tied hand beats) | BR | CI |")
for name, src, q in TIE:
    e = edges(q); d = max(e, key=e.get)
    ci = ""
    if name in TIE_BOOT:
        b = TIE_BOOT[name]
        ci = f"X- {b['Xm'][0]:+.1f} [{b['Xm'][1]:+.1f},{b['Xm'][2]:+.1f}]; X+ {b['Xp'][0]:+.1f} [{b['Xp'][1]:+.1f},{b['Xp'][2]:+.1f}] (cluster bootstrap)"
    if name in TIE_N:
        n = TIE_N[name]; qq = norm(q)
        parts = []
        for dd, (a, bb) in {1: (qq[0], qq[2]), 2: (qq[1], qq[0])}.items():
            se = math.sqrt((a + bb - (a - bb) ** 2) / n); ed = a - bb
            parts.append(f"{NAME[dd]} {ed*100:+.1f} [{(ed-Z*se)*100:+.1f},{(ed+Z*se)*100:+.1f}]")
        ci = f"n={n}: " + "; ".join(parts)
    qq = norm(q)
    print(f"| {name} | {src} | {qq[0]*100:.1f}/{qq[1]*100:.1f}/{qq[2]*100:.1f} | {e[1]*100:+.1f} | {e[0]*100:+.1f} | {e[2]*100:+.1f} | {NAME[d]} {e[d]*100:+.1f} | {ci} |")
# Yoshizawa: overall repeat 22.75%, assume after-tie repeat equals it and shifts split evenly (ASSUMPTION)
r = YOSHIZAWA_REPEAT
print(f"\nYoshizawa overall repeat {r*100:.2f}% (all pairs). If after-tie repeat = {r*100:.2f}% and shifts split evenly: "
      f"X- edge {(1-3*r)/2*100:+.1f}pp, X+ edge {(3*r-1)/2*100:+.1f}pp (equal by symmetry: both switches beat a repeat-avoider's switch half the time).")
# per tied hand
HAND = ["R", "P", "S"]
print("\nPer tied hand (next R/P/S %), edges of X- (hand tied hand beats) and X+ (hand that beats tied hand):")
for ds, d in TIE_HAND.items():
    out = []
    for i, h in enumerate(HAND):
        nxt = d[h]  # next R,P,S given tie on hand h
        stay = nxt[i]; up = nxt[(i + 1) % 3]; down = nxt[(i + 2) % 3]  # index: R=0,P=1,S=2; P beats R, S beats P, R beats S
        out.append(f"{h}-tie: X-({HAND[(i+2)%3]}) {up-stay:+.1f}, X+({HAND[(i+1)%3]}) {stay-down:+.1f}, X({h}) {down-up:+.1f}")
    print(f"  {ds} [{d['src']}]: " + " | ".join(out))
