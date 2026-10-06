"""Check the direction of each recommended rule against verified conditional tables.
Tables are from the OPPONENT's perspective: after the opponent's outcome o in {W,T,L},
P(stay on X), P(up = hand that beats X), P(down = hand X beats), X = opponent's last hand.
Our reply edges: reply X -> d-u ; reply X+ -> s-d ; reply X- -> u-s.
"""
T = {  # (s, u, d)
    "ZJ a=2 (Wang14, re-matched lab)": {"W": (.528, .226, .247), "T": (.432, .334, .234), "L": (.360, .276, .365)},
    "Dyson16 (CA, vs computer)":      {"W": (.357, .307, .336), "T": (.275, .401, .324), "L": (.223, .372, .405)},
    "Forder&Dyson16 (UK, vs comp)":   {"W": (.4245, .2932, .2823), "T": (.2928, .3732, .3340), "L": (.2146, .3913, .3941)},
    "US fixed human dyads":           {"W": (.322, .358, .320), "T": (.294, .352, .354), "L": (.237, .377, .386)},
    "AU fixed human pairs":           {"W": (.262, .365, .372), "T": (.281, .337, .382), "L": (.285, .340, .374)},
    "JP 500 players (Komai)":         {"W": (.305, .352, .342), "T": (.277, .361, .362), "L": (.265, .336, .399)},
}
edge = {"X": lambda s, u, d: d - u, "X+": lambda s, u, d: s - d, "X-": lambda s, u, d: u - s}
# Rules phrased from MY perspective (my last hand Y). Map to opponent-relative reply.
# I won  -> opp lost (L), X = Y-  : repeat Y = X+, Y- = X, Y+ = X-
# I lost -> opp won  (W), X = Y+  : repeat Y = X-, Y- = X+, Y+ = X
# tie    -> (T), X = Y            : repeat = X,  Y- = X-, Y+ = X+
rules = [
    ("I WON: repeat my winning hand",                 "L", "X+"),
    ("I WON: throw the hand my winning hand beats",   "L", "X"),
    ("I WON: throw the hand that beats my winning hand", "L", "X-"),
    ("I LOST: repeat my losing hand",                 "W", "X-"),
    ("I LOST: beat the winner's hand",                "W", "X+"),
    ("I LOST: copy the winner's hand",                "W", "X"),
    ("TIE: repeat tied hand",                         "T", "X"),
    ("TIE: throw the hand the tied hand beats",       "T", "X-"),
    ("TIE: beat the tied hand",                       "T", "X+"),
]
names = list(T)
print(f"{'rule':52s}" + "".join(f"{n.split(' ')[0][:9]:>10s}" for n in names))
for label, state, reply in rules:
    vals = [edge[reply](*T[n][state]) for n in names]
    print(f"{label:52s}" + "".join(f"{v:+10.3f}" for v in vals))
print("\nConcrete example check (Rock=R, Paper=P, Scissors=S):")
beats = {"R": "S", "P": "R", "S": "P"}          # key beats value
beaten_by = {v: k for k, v in beats.items()}     # hand that beats key
print(" tie on R -> hand R beats =", beats["R"], "| tie on P ->", beats["P"], "| tie on S ->", beats["S"])
print(" opp last R -> hand R beats (X-) =", beats["R"], "; opp last S ->", beats["S"], "; opp last P ->", beats["P"])
print(" I won with P over R -> 'hand that beats my winning hand' =", beaten_by["P"], "(== X- of their R:", beats["R"], ")")
print(" I lost with R to P -> 'repeat my losing hand' = R (== X- of their P:", beats["P"], ")")
