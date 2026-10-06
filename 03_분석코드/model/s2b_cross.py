"""Item 2 (robustness across populations): candidate fixed rules vs every verified opponent table."""
import numpy as np
from data import COND, EARLY
from markov import STATES, stationary, match, shrink

RULES = {
    "R1 ZJ-BR: X+/X+/X": {"W": 1, "T": 1, "L": 0},
    "R2 always X+ (beat their last)": {"W": 1, "T": 1, "L": 1},
    "R3 always X- (play what their last beats)": {"W": 2, "T": 2, "L": 2},
    "R4 West-lab BR: X+/X-/X-": {"W": 1, "T": 2, "L": 2},
    "R5 Dyson16-BR: X/X-/X-": {"W": 0, "T": 2, "L": 2},
    "R6 MF1 cycle (self-downgrade): X+/X-/X": {"W": 1, "T": 2, "L": 0},
    "R7 C2 rules, tie random: X+/rand/X": {"W": 1, "T": "r", "L": 0},
    "R8 example 'beat last winning hand': X+/rand/X-": {"W": 1, "T": "r", "L": 2},
    "R9 core West: rand/X-/X-": {"W": "r", "T": 2, "L": 2},
    "R10 tie-only X-: rand/X-/rand": {"W": "r", "T": 2, "L": "r"},
    "R11 loss-only X-: rand/rand/X-": {"W": "r", "T": "r", "L": 2},
    "R0 uniform random": {"W": "r", "T": "r", "L": "r"},
}
OPP = dict(COND)
OPP.update(EARLY)
west = [k for k, v in COND.items() if v["group"] == "Western"]
zj = [k for k, v in COND.items() if v["group"] == "Zhejiang"]
early = list(EARLY.keys())

short = {"ZJ a=2 (Wang 2014)": "ZJa2", "Dyson 2016 (CA vs PC)": "DY16", "Forder&Dyson 2016 (UK vs PC)": "FD16",
         "Dyson 2021 E1 (CA vs PC)": "DY21", "ZJ vs AI (Wang L 2020)": "ZJAI", "US dyads (Brockbank)": "US",
         "AU pairs (Moerel)": "AU", "US dyads r1-20": "US1-20", "AU pairs r1-20": "AU1-20", "ZJ vs AI r1-20": "ZJAI1-20"}

print("Stationary per-throw edge (pp, win-loss) of each fixed rule (after opp W/T/L) vs each opponent table")
hdr = "| Rule | " + " | ".join(short[k] for k in OPP) + " | min full(7) | mean West(5) | mean ZJ(2) | min early(3) | Bo3 P(win) at full-min |"
print(hdr)
summary = {}
for rn, rule in RULES.items():
    vals = {}
    for k, t in OPP.items():
        _, e, _ = stationary(t, rule)
        vals[k] = e
    full = {k: vals[k] for k in COND}
    kmin = min(full, key=full.get)
    b3 = match(COND[kmin], rule, 2)[0]
    mw = np.mean([vals[k] for k in west]); mz = np.mean([vals[k] for k in zj])
    me = min(vals[k] for k in early)
    summary[rn] = (min(full.values()), mw, mz, me)
    print(f"| {rn} | " + " | ".join(f"{vals[k]*100:+.1f}" for k in OPP) +
          f" | {min(full.values())*100:+.1f} ({short[kmin]}) | {mw*100:+.1f} | {mz*100:+.1f} | {me*100:+.1f} | {b3:.3f} |")

print("\nSame, opponents' biases halved (x0.5 toward 1/3):")
print("| Rule | min full(7) | mean West(5) | mean ZJ(2) | min early(3) |")
for rn, rule in RULES.items():
    vals = {}
    for k, t in OPP.items():
        _, e, _ = stationary(shrink(t, 0.5), rule)
        vals[k] = e
    print(f"| {rn} | {min(vals[k] for k in COND)*100:+.1f} | {np.mean([vals[k] for k in west])*100:+.1f} | "
          f"{np.mean([vals[k] for k in zj])*100:+.1f} | {min(vals[k] for k in early)*100:+.1f} |")

print("\nBo3 match-win probability (first throw random) for selected rules vs each opponent:")
for rn in ["R1 ZJ-BR: X+/X+/X", "R3 always X- (play what their last beats)", "R6 MF1 cycle (self-downgrade): X+/X-/X",
           "R8 example 'beat last winning hand': X+/rand/X-", "R9 core West: rand/X-/X-", "R10 tie-only X-: rand/X-/rand",
           "R11 loss-only X-: rand/rand/X-"]:
    rule = RULES[rn]
    print(f"  {rn}: " + ", ".join(f"{short[k]} {match(t, rule, 2)[0]:.3f}" for k, t in OPP.items()))
