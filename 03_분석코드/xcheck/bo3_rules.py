"""Exact Bo3 (first to 2 decisive wins, ties replayed) win probability for reply rules vs conditional tables.
State = opponent's last outcome (W/T/L, opponent view) after throw 1; throw 1 is uniform for both sides.
Rule: dict state->reply in {'X','X+','X-','rand'} relative to the opponent's last hand."""
from functools import lru_cache

T = {
    "ZJ a=2":  {"W": (.528, .226, .247), "T": (.432, .334, .234), "L": (.360, .276, .365)},
    "Dyson16": {"W": (.357, .307, .336), "T": (.275, .401, .324), "L": (.223, .372, .405)},
    "Forder":  {"W": (.4245, .2932, .2823), "T": (.2928, .3732, .3340), "L": (.2146, .3913, .3941)},
    "US pairs": {"W": (.322, .358, .320), "T": (.294, .352, .354), "L": (.237, .377, .386)},
    "AU pairs": {"W": (.262, .365, .372), "T": (.281, .337, .382), "L": (.285, .340, .374)},
    "JP 500":  {"W": (.305, .352, .342), "T": (.277, .361, .362), "L": (.265, .336, .399)},
}

def shrink(tab, f):
    return {o: tuple(1/3 + f*(x - 1/3) for x in p) for o, p in tab.items()}

def step(p, reply):
    """returns (P we win, P tie, P we lose) given opp next-dist p=(s,u,d) relative to X and our reply."""
    s, u, d = p
    if reply == "rand":
        return (1/3, 1/3, 1/3)
    if reply == "X":   # beats X- (d), ties X (s), loses to X+ (u)
        return (d, s, u)
    if reply == "X+":  # beats X (s), ties X+ (u), loses to X- (d)
        return (s, u, d)
    return (u, d, s)    # X-: beats X+ (u), ties X- (d), loses to X (s)

def bo3(tab, rule):
    # opponent outcome after a throw: we win -> opp 'L'; tie -> 'T'; we lose -> 'W'
    @lru_cache(None)
    def V(state, w, l):
        if w == 2: return 1.0
        if l == 2: return 0.0
        pw, pt, pl = step(tab[state], rule[state])
        # tie loops on state 'T'
        return pw*V("L", w+1, l) + pt*V_tie(w, l) + pl*V("W", w, l+1)
    @lru_cache(None)
    def V_tie(w, l):
        pw, pt, pl = step(tab["T"], rule["T"])
        return (pw*V("L", w+1, l) + pl*V("W", w, l+1)) / (1 - pt)
    # throw 1 uniform: win/tie/lose 1/3 each
    return (V("L", 1, 0) + V_tie(0, 0) + V("W", 0, 1)) / 3

rules = {
    "R3 always X- (base rule)": {"W": "X-", "T": "X-", "L": "X-"},
    "R9 X- after tie/our win, random after our loss": {"W": "rand", "T": "X-", "L": "X-"},
    "R4 X+ after our loss, X- otherwise": {"W": "X+", "T": "X-", "L": "X-"},
    "random": {"W": "rand", "T": "rand", "L": "rand"},
}
for f in (1.0, 0.5):
    print(f"\n== opponent biases x{f} (Bo3 P(win)) ==")
    print(f"{'rule':50s}" + "".join(f"{k:>10s}" for k in T))
    for name, r in rules.items():
        print(f"{name:50s}" + "".join(f"{bo3(shrink(T[k], f), r):10.3f}" for k in T))
