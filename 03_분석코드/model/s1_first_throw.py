"""Item 1: W/T/L and net edge of throwing R, P, S against each verified marginal distribution."""
import math
from data import FIRST, WANG2014, ACZEL

Z = 1.959964


def shares(d):
    if "counts" in d:
        c = d["counts"]
        n = sum(c)
        return tuple(x / n for x in c), n
    r = d["rps"]
    s = sum(r)
    return tuple(x / s for x in r), d.get("n")


def wtl(p):
    R, P, S = p
    # throwing Rock: win vs S, tie vs R, lose vs P ; Paper: win vs R, tie P, lose S ; Scissors: win P, tie S, lose R
    return {"R": (S, R, P), "P": (R, P, S), "S": (P, S, R)}


def se_diff(pa, pb, n):
    # multinomial: Var(pa_hat - pb_hat) = (pa + pb - (pa - pb)^2) / n
    return math.sqrt((pa + pb - (pa - pb) ** 2) / n)


# ---- calibrate intra-cluster correlation from the two cluster-bootstrap CIs ----
rho = {}
for d in FIRST:
    if "boot_paper" in d:
        p, n = shares(d)
        se_naive = se_diff(p[0], p[2], n)
        est, lo, hi = d["boot_paper"]
        se_boot = (hi - lo) / 100 / (2 * Z)
        deff = (se_boot / se_naive) ** 2
        rho[d["name"]] = ((deff - 1) / (d["m"] - 1), deff, se_naive, se_boot)
print("Calibration of clustering (Paper edge, naive vs reported cluster bootstrap):")
for k, (r, deff, sn, sb) in rho.items():
    print(f"  {k}: naive SE {sn*100:.2f}pp, bootstrap SE {sb*100:.2f}pp, deff {deff:.2f}, implied ICC {r:.4f}")
# Wang 2014 implied ICC for Rock share: between-player var / p(1-p)
mR, sdR = WANG2014["mean"][0], WANG2014["sd"][0]
binom_var = mR * (1 - mR) / 300
icc_w = (sdR ** 2 - binom_var) / (mR * (1 - mR))
print(f"  Wang 2014 implied ICC for Rock share (SD .08, 300 rounds): {icc_w:.4f}")
RHO = max(r[0] for r in rho.values())  # conservative of the two raw-data calibrations
print(f"  -> ICC used for adjusted CIs: {RHO:.4f} (larger of the two raw-data values)\n")

print("| Dataset | kind | n | R/P/S % | edge R | edge P | edge S | best | naive 95% CI best | adj. 95% CI best |")
rows = []
for d in FIRST:
    p, n = shares(d)
    e = {h: (w - l) for h, (w, t, l) in wtl(p).items()}
    best = max(e, key=e.get)
    pair = {"R": (p[2], p[1]), "P": (p[0], p[2]), "S": (p[1], p[0])}[best]
    ci = adj = "n/a"
    if n:
        se = se_diff(pair[0], pair[1], n)
        ci = f"[{(e[best]-Z*se)*100:+.1f}, {(e[best]+Z*se)*100:+.1f}]"
        if d.get("m"):
            f = math.sqrt(1 + (d["m"] - 1) * RHO)
            adj = f"[{(e[best]-Z*se*f)*100:+.1f}, {(e[best]+Z*se*f)*100:+.1f}] (x{f:.1f})"
        if "boot_paper" in d and best == "P":
            adj = f"[{d['boot_paper'][1]:+.1f}, {d['boot_paper'][2]:+.1f}] (reported bootstrap)"
    if "boot_paper" in d and best != "P":
        adj = f"Paper edge bootstrap [{d['boot_paper'][1]:+.1f}, {d['boot_paper'][2]:+.1f}]"
    print(f"| {d['name']} | {d['kind']} | {n if n else 'n/a'} | {p[0]*100:.1f}/{p[1]*100:.1f}/{p[2]*100:.1f} | "
          f"{e['R']*100:+.1f} | {e['P']*100:+.1f} | {e['S']*100:+.1f} | {best} | {ci} | {adj} |")
    rows.append((d['name'], p, e, n))

# Also CIs for every hand's edge (naive) for the record
print("\nAll-hand naive 95% CIs (pp):")
for d in FIRST:
    p, n = shares(d)
    if not n:
        continue
    out = []
    for h, (a, b) in {"R": (p[2], p[1]), "P": (p[0], p[2]), "S": (p[1], p[0])}.items():
        se = se_diff(a, b, n)
        out.append(f"{h} {(a-b)*100:+.1f} [{(a-b-Z*se)*100:+.1f},{(a-b+Z*se)*100:+.1f}]")
    print(f"  {d['name']}: " + "; ".join(out))

# Explicit W/T/L table
print("\nExplicit W/T/L (%) when throwing each hand:")
for d in FIRST:
    p, n = shares(d)
    w = wtl(p)
    print(f"  {d['name']}: Rock {w['R'][0]*100:.1f}/{w['R'][1]*100:.1f}/{w['R'][2]*100:.1f} | "
          f"Paper {w['P'][0]*100:.1f}/{w['P'][1]*100:.1f}/{w['P'][2]*100:.1f} | "
          f"Scissors {w['S'][0]*100:.1f}/{w['S'][1]*100:.1f}/{w['S'][2]*100:.1f}")

# Wang 2014: player-level SE with correlation bounds
m = WANG2014["mean"]; sd = WANG2014["sd"]; N = WANG2014["players"]
eP = m[0] - m[2]
for corr in (0.0, -0.5, -1.0):
    se = math.sqrt(sd[0] ** 2 + sd[2] ** 2 - 2 * corr * sd[0] * sd[2]) / math.sqrt(N)
    print(f"\nWang 2014 Paper edge {eP*100:+.1f}pp; corr(R,S) across players={corr}: 95% CI "
          f"[{(eP-Z*se)*100:+.1f}, {(eP+Z*se)*100:+.1f}]")
eR = m[2] - m[1]; eS = m[1] - m[0]
print(f"Wang 2014 edges: R {eR*100:+.1f}, P {eP*100:+.1f}, S {eS*100:+.1f}")

# Aczel: Rock edge = S - P ; P unknown; assume R=P split of the remainder
for s in ACZEL["S"]:
    rest = (1 - s) / 2
    print(f"Aczel S={s*100:.2f}%: if R=P={rest*100:.2f}% then Rock edge {(s-rest)*100:+.1f}pp, "
          f"Paper edge {(rest-s)*100:+.1f}pp, Scissors 0")
