"""Item 2: best responses to outcome-conditioned opponents; stationary and short-match edges; robustness."""
import math
import numpy as np
from data import COND, EARLY, SEM
from markov import (STATES, NAME, edges, best_response, stationary, match, shrink, only_loss, norm)

Z = 1.959964
ALL = dict(COND)
ALL.update({k: v for k, v in EARLY.items()})


def fmt_rule(rule):
    return "/".join(NAME[rule[s]] for s in STATES)


print("=== Per-state edges (pp) of responses X+ / X / X- relative to OPP's last hand; BR marked ===")
BR = {}
for name, t in ALL.items():
    br = best_response(t)
    BR[name] = br
    parts = []
    for s in STATES:
        e = edges(t[s])
        parts.append(f"{s}: X+ {e[1]*100:+.1f}, X {e[0]*100:+.1f}, X- {e[2]*100:+.1f} -> {NAME[br[s][0]]} {br[s][1]*100:+.1f}")
    print(f"{name}: " + " | ".join(parts))

print("\n=== Approximate CIs on BR state edges ===")
# early-round pooled cells: multinomial
for name, t in EARLY.items():
    out = []
    for s in STATES:
        q = norm(t[s]); n = t["n" + s]
        d, e = BR[name][s]
        # edge components: X+ = stay-down, X = down-up, X- = up-stay
        a, b = {1: (q[0], q[2]), 0: (q[2], q[1]), 2: (q[1], q[0])}[d]
        se = math.sqrt((a + b - (a - b) ** 2) / n)
        out.append(f"{s}({n}) {NAME[d]} {e*100:+.1f} [{(e-Z*se)*100:+.1f},{(e+Z*se)*100:+.1f}]")
    print(f"{name}: " + "; ".join(out))
# per-player SEM-based (covariance unknown: lower bound uses cov=0, upper uses cov=-SEa*SEb)
for name, sem in SEM.items():
    t = COND[name]
    nclus = sem["nclus"]
    tcrit = {116: 1.981, 62: 2.000, 31: 2.042, 12: 2.201}[nclus]
    for s in STATES:
        if s not in sem:
            continue
        q = norm(t[s]); se3 = sem[s]
        for d, (ia, ib) in {1: (0, 2), 0: (2, 1), 2: (1, 0)}.items():
            if se3[ia] is None or se3[ib] is None:
                continue
            e = q[ia] - q[ib]
            lo_se = math.sqrt(se3[ia] ** 2 + se3[ib] ** 2)
            hi_se = se3[ia] + se3[ib]
            print(f"  {name} after opp {s}, {NAME[d]}: {e*100:+.1f}pp; 95% CI between "
                  f"[{(e-tcrit*lo_se)*100:+.1f},{(e+tcrit*lo_se)*100:+.1f}] and "
                  f"[{(e-tcrit*hi_se)*100:+.1f},{(e+tcrit*hi_se)*100:+.1f}]")

print("\n=== Own-BR exploitation: stationary per-throw edge and match outcomes (first throw random) ===")
print("| Opponent table | BR rule (after opp W/T/L) | unweighted mean state edge | stationary pi(W,T,L) | stationary edge/throw | tie rate | q=w/(w+l) | P(win 1 decisive) | P(win Bo3) | edge/throw in Bo3 | E[throws Bo3] | P(win Bo5) |")
RES = {}
for name, t in ALL.items():
    br = BR[name]
    rule = {s: br[s][0] for s in STATES}
    mean_state = np.mean([br[s][1] for s in STATES])
    pi, e, tie = stationary(t, rule)
    w = (1 - tie + e) / 2; l = (1 - tie - e) / 2
    q = w / (w + l)
    p1 = match(t, rule, 1)
    p3 = match(t, rule, 2)
    p5 = match(t, rule, 3)
    RES[name] = (rule, e, q, p3[0], p5[0])
    print(f"| {name} | {fmt_rule(rule)} | {mean_state*100:+.1f} | {pi[0]:.2f}/{pi[1]:.2f}/{pi[2]:.2f} | {e*100:+.1f} | "
          f"{tie*100:.1f} | {q:.3f} | {p1[0]:.3f} | {p3[0]:.3f} | {p3[3]*100:+.1f} | {p3[1]:.2f} | {p5[0]:.3f} |")

print("\n=== Robustness: same BR rule vs opponent with biases halved; vs opponent with ONLY its after-loss bias ===")
print("| Opponent table | full: edge/throw, Bo3 | biases x0.5: edge/throw, Bo3 | only lose-shift: BR after opp loss, edge/throw, Bo3 |")
for name, t in ALL.items():
    rule = RES[name][0]
    _, e_full, _ = stationary(t, rule)
    b3_full = match(t, rule, 2)[0]
    th = shrink(t, 0.5)
    _, e_half, _ = stationary(th, rule)
    b3_half = match(th, rule, 2)[0]
    tl = only_loss(t)
    brl = best_response(tl)
    rule_l = {"W": "r", "T": "r", "L": brl["L"][0]}
    _, e_l, _ = stationary(tl, rule_l)
    b3_l = match(tl, rule_l, 2)[0]
    print(f"| {name} | {e_full*100:+.2f}, {b3_full:.3f} | {e_half*100:+.2f}, {b3_half:.3f} | "
          f"{NAME[brl['L'][0]]} ({brl['L'][1]*100:+.1f} on post-loss throws), {e_l*100:+.2f}, {b3_l:.3f} |")

# Generic symmetric lose-shift (B3 range of lose-stay 17.7%..26.1%, shifts split evenly) -- assumption
print("\nGeneric lose-shift opponent (repeat-after-loss r, shifts split evenly; W,T uniform):")
for r in (0.177, 0.2146, 0.223, 0.261, 0.30):
    t = {"W": (1/3, 1/3, 1/3), "T": (1/3, 1/3, 1/3), "L": (r, (1 - r) / 2, (1 - r) / 2)}
    rule = {"W": "r", "T": "r", "L": 2}
    _, e, _ = stationary(t, rule)
    b3 = match(t, rule, 2)[0]
    print(f"  r={r:.3f}: post-loss X- edge {(1-3*r)/2*100:+.1f}pp; stationary {e*100:+.2f}pp/throw; Bo3 {b3:.3f}")

print("\n=== Late-session comparison (rounds 51-300) BR ===")
from data import LATE
for name, t in LATE.items():
    br = best_response(t)
    rule = {s: br[s][0] for s in STATES}
    _, e, _ = stationary(t, rule)
    print(f"{name}: BR {fmt_rule(rule)} state edges " +
          ", ".join(f"{s} {br[s][1]*100:+.1f}" for s in STATES) + f"; stationary {e*100:+.1f}pp")
