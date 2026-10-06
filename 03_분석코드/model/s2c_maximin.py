"""Brute force all 64 per-state rules (X+, X, X-, random for each opp state) -> maximin / mean across tables."""
import itertools, numpy as np
from data import COND, EARLY
from markov import stationary, match, NAME
opts = [1, 0, 2, "r"]
full = list(COND.keys()); early = list(EARLY.keys())
west = [k for k, v in COND.items() if v["group"] == "Western"]; zj = [k for k, v in COND.items() if v["group"] == "Zhejiang"]
res = []
for w, t, l in itertools.product(opts, repeat=3):
    rule = {"W": w, "T": t, "L": l}
    ef = {k: stationary(COND[k], rule)[1] for k in full}
    ee = {k: stationary(EARLY[k], rule)[1] for k in early}
    res.append((rule, min(ef.values()), np.mean(list(ef.values())), min(ee.values()), np.mean(list(ee.values())),
                min(list(ef.values()) + list(ee.values())), np.mean([ef[k] for k in west]), np.mean([ef[k] for k in zj])))
def nm(r): return "/".join(NAME[r[s]] for s in ("W", "T", "L"))
print("Top 8 by worst case over all 10 tables (7 full + 3 early):")
for r in sorted(res, key=lambda x: -x[5])[:8]:
    print(f"  {nm(r[0])}: min10 {r[5]*100:+.2f} | min full {r[1]*100:+.2f} mean full {r[2]*100:+.2f} | min early {r[3]*100:+.2f} mean early {r[4]*100:+.2f} | West {r[6]*100:+.2f} ZJ {r[7]*100:+.2f}")
print("Top 5 by mean over 7 full tables:")
for r in sorted(res, key=lambda x: -x[2])[:5]:
    print(f"  {nm(r[0])}: mean full {r[2]*100:+.2f} min full {r[1]*100:+.2f} min early {r[3]*100:+.2f}")
print("Count of the 63 non-random rules with min over 7 full tables > 0:",
      sum(1 for r in res if r[1] > 1e-9))
