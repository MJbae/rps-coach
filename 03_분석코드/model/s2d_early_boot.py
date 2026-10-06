"""Parametric bootstrap (multinomial resampling of each rounds-1-20 cell, n from sequential:MF2) of stationary edges."""
import numpy as np
from data import EARLY
from markov import stationary, norm
rng = np.random.default_rng(11)
RULES = {"R3 always X-": {"W": 2, "T": 2, "L": 2}, "R2 always X+": {"W": 1, "T": 1, "L": 1},
         "R4 X+/X-/X-": {"W": 1, "T": 2, "L": 2}, "R6 MF1 cycle X+/X-/X": {"W": 1, "T": 2, "L": 0},
         "R10 tie-only X-": {"W": "r", "T": 2, "L": "r"}, "R11 loss-only X-": {"W": "r", "T": "r", "L": 2}}
B = 4000
for name, t in EARLY.items():
    draws = {s: rng.multinomial(t["n" + s], norm(t[s]), size=B) / t["n" + s] for s in "WTL"}
    out = []
    for rn, rule in RULES.items():
        est = stationary(t, rule)[1]
        bs = np.array([stationary({s: draws[s][i] for s in "WTL"}, rule)[1] for i in range(B)])
        lo, hi = np.percentile(bs, [2.5, 97.5])
        out.append(f"{rn} {est*100:+.1f} [{lo*100:+.1f},{hi*100:+.1f}]")
    print(f"{name}: " + "; ".join(out))
