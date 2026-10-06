"""Verified parameters only (source IDs from the verified-data JSON)."""

# ---------- Item 1: unconditional / first-throw distributions ----------
# Each entry: name, source id, kind, (R, P, S) as counts or fractions, n (throws) or None,
# m = throws per cluster (player/triad) for design-effect adjustment (None = ~independent)
FIRST = [
    # --- first throws ---
    dict(name="Batzilis 2019 first throws, full (online 2007)", src="baserates:C01 / foundations:C06",
         kind="first", rps=(0.3399, 0.3482, 0.3120), n=5012128, m=15),
    dict(name="Batzilis 2019 first throws, experienced (>=100 matches)", src="baserates:C01",
         kind="first", rps=(0.3260, 0.3456, 0.3284), n=1472319, m=190),
    dict(name="Eyler 2009 first throws (US, vs computer)", src="baserates:C02",
         kind="first", counts=(66, 39, 14), m=None),
    dict(name="Brockbank & Vul round 1 (US dyads)", src="baserates:MF04",
         kind="first", counts=(40, 53, 27), m=None),
    dict(name="Moerel 2025 game 1 (AU pairs)", src="baserates:MF04",
         kind="first", counts=(14, 12, 23), m=None),
    dict(name="Toint 2023 STATED opener, all (JP survey)", src="baserates:C14",
         kind="stated", counts=(374, 206, 420), m=None),
    dict(name="Toint 2023 STATED opener, men", src="baserates:C14",
         kind="stated", counts=(143, 85, 109), m=None),
    dict(name="Toint 2023 STATED opener, women", src="baserates:C14",
         kind="stated", counts=(231, 121, 311), m=None),
    # --- all throws ---
    dict(name="Batzilis 2019 all-throws proxy (avg of opp. histories)", src="baserates:C01",
         kind="all", rps=(0.3545, 0.3401, 0.3054), n=None, m=None),
    dict(name="Xu 2013 Zhejiang lab (a=2, 72 x 300)", src="baserates:C04",
         kind="all", counts=(7702, 6937, 6961), m=300),
    dict(name="Wang L 2020 Zhejiang vs AI (41 x 300)", src="baserates:C04",
         kind="all", counts=(4371, 3948, 3981), m=300),
    dict(name="Dyson 2016 Canada vs computer (31 x 225)", src="sequential:B1 / foundations:C06",
         kind="all", rps=(0.3560, 0.3224, 0.3216), n=31 * 225, m=225),
    dict(name="Forder & Dyson 2016 UK vs computer (36 x 450)", src="baserates:C18 (P by subtraction)",
         kind="all", rps=(0.3516, 1 - 0.3516 - 0.3235, 0.3235), n=36 * 450, m=450),
    dict(name="Dyson 2022 Canada vs computer (avg of 3 conditions)", src="baserates:MF03",
         kind="all", rps=((0.370 + 0.356 + 0.348) / 3, (0.323 + 0.327 + 0.335) / 3,
                          (0.307 + 0.316 + 0.318) / 3), n=40 * 360, m=360),
    dict(name="Moerel 2025 AU fixed pairs (29,511 throws)", src="baserates:C12 / MF03",
         kind="all", rps=(0.3534, 0.3254, 0.3212), n=29511, m=476,
         boot_paper=(3.2, 1.4, 5.2)),
    dict(name="Brockbank & Vul 2020 US dyads (all games)", src="baserates:MF03",
         kind="all", counts=(11457, 12068, 12444), m=298,
         boot_paper=(-2.7, -4.8, -0.7)),
    dict(name="Cook 2012 UK live hands", src="baserates:C11",
         kind="all", rps=(0.324, 0.333, 0.344), n=14 * 9 * 20 * 2, m=360),
    dict(name="Yoshizawa JP live hands (725 people)", src="baserates:C05",
         kind="all", counts=(4054, 3849, 3664), m=16),
    dict(name="Sazae-san TV sequence (anecdotal)", src="baserates:C16",
         kind="all", counts=(436, 444, 467), m=None),
]
# Wang 2014 (354 players): mean individual frequencies and between-player SDs
WANG2014 = dict(name="Wang 2014 Zhejiang lab (354 players, all a)", src="sequential:A4 / baserates:C04",
                mean=(0.36, 0.33, 0.32), sd=(0.08, 0.07, 0.06), players=354)
# Aczel 2012 live Hungary: only Scissors share reported
ACZEL = dict(name="Aczel 2012 HU live hands (Scissors share only)", src="baserates:C11 / MF3",
             S=(0.3676, 0.3664))

# ---------- Item 2/3: conditional tables ----------
# Rows are the OPPONENT's own previous outcome; values = P(next = stay X, up X+, down X-),
# where X = opponent's previous hand, X+ = hand that beats X, X- = hand X beats.
COND = {
    "ZJ a=2 (Wang 2014)": dict(src="sequential:A1", group="Zhejiang",
        W=(0.528, 0.226, 0.247), T=(0.432, 0.334, 0.234), L=(0.360, 0.276, 0.365)),
    "Dyson 2016 (CA vs PC)": dict(src="sequential:B1", group="Western",
        W=(0.357, 0.307, 0.336), T=(0.275, 0.401, 0.324), L=(0.223, 0.372, 0.405)),
    "Forder&Dyson 2016 (UK vs PC)": dict(src="sequential:B2", group="Western",
        W=(0.4245, 0.2932, 0.2823), T=(0.2928, 0.3732, 0.3340), L=(0.2146, 0.3913, 0.3941)),
    "Dyson 2021 E1 (CA vs PC)": dict(src="sequential:MF5 (Exp1 no-credit column)", group="Western",
        W=(0.376, 0.329, 0.295), T=(0.294, 0.380, 0.327), L=(0.234, 0.385, 0.382)),
    "ZJ vs AI (Wang L 2020)": dict(src="sequential:C2", group="Zhejiang",
        W=(0.469, 0.284, 0.248), T=(0.394, 0.303, 0.303), L=(0.375, 0.320, 0.305)),
    "US dyads (Brockbank)": dict(src="sequential:C1", group="Western",
        W=(0.322, 0.358, 0.320), T=(0.294, 0.352, 0.354), L=(0.237, 0.377, 0.386)),
    "AU pairs (Moerel)": dict(src="sequential:C1", group="Western",
        W=(0.262, 0.365, 0.372), T=(0.281, 0.337, 0.382), L=(0.285, 0.340, 0.374)),
}
# Early-round (rounds 1-20) pooled tables with cell n (sequential:MF2)
EARLY = {
    "US dyads r1-20": dict(src="sequential:MF2", W=(0.279, 0.381, 0.340), nW=746,
                           T=(0.331, 0.328, 0.341), nT=686, L=(0.296, 0.352, 0.352), nL=744),
    "AU pairs r1-20": dict(src="sequential:MF2", W=(0.261, 0.404, 0.335), nW=364,
                           T=(0.285, 0.312, 0.403), nT=372, L=(0.275, 0.367, 0.358), nL=360),
    "ZJ vs AI r1-20": dict(src="sequential:MF2", W=(0.375, 0.314, 0.311), nW=309,
                           T=(0.329, 0.365, 0.306), nT=310, L=(0.336, 0.331, 0.333), nL=369),
}
LATE = {
    "US dyads r51-300": dict(W=(0.324, 0.359, 0.317), T=(0.286, 0.357, 0.357), L=(0.223, 0.380, 0.397)),
    "ZJ vs AI r51-300": dict(W=(0.469, 0.288, 0.243), T=(0.394, 0.299, 0.308), L=(0.402, 0.309, 0.289)),
}
# Per-player SEMs (sequential:C1 US; sequential:A1 ZJ a=2 group SEMs, 12 groups)
SEM = {
    "US dyads (Brockbank)": dict(nclus=116,
        W=(0.016, 0.012, 0.013), T=(0.012, 0.008, 0.010), L=(0.012, 0.010, 0.010)),
    "AU pairs (Moerel)": dict(nclus=62, W=(0.014, 0.013, 0.016)),
    "Dyson 2016 (CA vs PC)": dict(nclus=31, L=(0.026, 0.018, 0.028)),
    "ZJ a=2 (Wang 2014)": dict(nclus=12, W=(0.040, None, 0.024)),
}

# ---------- Item 3: after-tie tables (stay, up=X+, down=X-) ----------
TIE = [
    ("Wang&Xu a=1 (tie pays = win)", "baserates:C08/MF02", (0.800, 0.138, 0.060)),
    ("Wang 2014 a=1.1", "baserates:C08", (0.604, 0.253, 0.143)),
    ("Wang 2014 a=2", "sequential:A1", (0.432, 0.334, 0.234)),
    ("Wang 2014 a=4", "baserates:C08", (0.388, 0.382, 0.230)),
    ("Wang 2014 a=9", "baserates:C08", (0.358, 0.349, 0.291)),
    ("Wang 2014 a=100", "baserates:C08", (0.364, 0.368, 0.269)),
    ("Wang&Xu a=inf (tie pays 0)", "baserates:C08/MF02", (0.338, 0.377, 0.283)),
    ("Wang L 2020 ZJ vs AI", "sequential:C2", (0.394, 0.303, 0.303)),
    ("Dyson 2016 CA (unweighted)", "sequential:B1", (0.275, 0.401, 0.324)),
    ("Dyson 2016 CA (hand-weighted)", "baserates:C07", (0.287, 0.396, 0.317)),
    ("Forder&Dyson 2016 UK", "sequential:B2", (0.2928, 0.3732, 0.3340)),
    ("Dyson 2021 Exp1 (avg credit)", "sequential:MF5", (0.297, 0.366, 0.338)),
    ("Dyson 2021 Exp2 (avg credit)", "sequential:MF5", (0.263, 0.357, 0.380)),
    ("Dyson 2021 Exp3 (avg credit)", "sequential:MF5", (0.339, 0.351, 0.309)),
    ("US dyads (per-player means)", "sequential:C1", (0.294, 0.352, 0.354)),
    ("US dyads (pooled, 11,656 ties)", "baserates:MF01", (0.291, 0.352, 0.356)),
    ("AU pairs (per-player means)", "sequential:C1", (0.281, 0.337, 0.382)),
    ("AU pairs (pooled, 9,661 ties)", "baserates:MF01", (0.283, 0.337, 0.380)),
    ("US dyads rounds 1-20", "sequential:MF2", (0.331, 0.328, 0.341)),
    ("AU pairs rounds 1-20", "sequential:MF2", (0.285, 0.312, 0.403)),
    ("ZJ vs AI rounds 1-20", "sequential:MF2", (0.329, 0.365, 0.306)),
    ("Toint 2023 JP STATED", "baserates:MF07", (0.193, 0.369, 0.438)),
]
TIE_BOOT = {  # cluster-bootstrap CIs (pp) reported in baserates:MF01 / C18
    "US dyads (pooled, 11,656 ties)": dict(Xm=(5.8, 2.4, 9.1), Xp=(-6.3, -10.6, -1.7)),
    "AU pairs (pooled, 9,661 ties)": dict(Xm=(5.4, 1.2, 9.7), Xp=(-9.8, -14.0, -5.3)),
}
TIE_N = {"US dyads rounds 1-20": 686, "AU pairs rounds 1-20": 372, "ZJ vs AI rounds 1-20": 310}
# Per tied hand: next R/P/S shares (%)
TIE_HAND = {
    "AU pairs (Moerel)": dict(src="baserates:MF01", R=(30.4, 31.4, 38.2), P=(40.1, 27.8, 32.2), S=(38.0, 35.8, 26.2)),
    "US dyads (Brockbank)": dict(src="baserates:MF01", R=(30.7, 34.7, 34.6), P=(35.4, 26.1, 38.5), S=(32.5, 36.7, 30.8)),
    "Dyson 2016 CA": dict(src="baserates:C07", R=(32.1, 37.2, 30.7), P=(34.3, 24.8, 40.8), S=(42.3, 32.1, 25.5)),
}
YOSHIZAWA_REPEAT = 2465 / 10833  # baserates:C06 (all consecutive pairs, not tie-specific)

# ---------- Item 6 calibration: human exploitation of 90%-pattern bots ----------
# baserates/sequential:D4 + MF1 (Brockbank & Vul 2024 Exp1 raw data): human win/loss % vs bot
BOTS90 = [
    ("prev_move_positive (bot plays what beats its own last)", "simple self-transition", 66.5, 16.6),
    ("opponent_prev_move_nil (bot copies human's last)", "simple opp-transition", 65.0, 17.7),
    ("prev_move_negative (bot plays what its own last beats = MF1 cycle)", "simple self-transition", 62.2, 17.6),
    ("opponent_prev_move_positive (bot beats human's last)", "simple opp-transition", 58.5, 12.7),
    ("win_nil_lose_positive (stay/upgrade/downgrade after W/L/T)", "outcome-conditioned", 41.3, 24.8),
    ("win_positive_lose_negative", "outcome-conditioned", 39.7, 26.7),
    ("outcome_transition_dual_dependency", "outcome x transition", 34.1, 32.0),
]
