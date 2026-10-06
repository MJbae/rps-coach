"""Monte Carlo check of the Markov solver with explicit absolute hands."""
import random
from data import COND
from markov import stationary, match, norm
random.seed(7)
def beats(a, b):  # True if hand a beats hand b ; hand h+1 beats h
    return (a - b) % 3 == 1
def sim(table, rule, nmatch=200000, N=2, p=1.0):
    q = {s: norm(table[s]) for s in "WTL"}
    wins = thr = net = 0
    for _ in range(nmatch):
        a = b = 0; state = None; opp_last = None
        while a < N and b < N:
            if state is None:
                me = random.randrange(3); op = random.randrange(3)
            else:
                r = random.random(); qs = q[state]
                rel = 0 if r < qs[0] else (1 if r < qs[0] + qs[1] else 2)
                op = (opp_last + rel) % 3       # stay / up(X+1 beats X) / down (X-1)
                d = rule[state]
                if d == "r" or random.random() > p: me = random.randrange(3)
                else: me = (opp_last + d) % 3
            thr += 1
            if beats(me, op): a += 1; net += 1; state = "L"
            elif beats(op, me): b += 1; net -= 1; state = "W"
            else: state = "T"
            opp_last = op
        wins += a >= N
    return wins / nmatch, net / thr, thr / nmatch
for name, rule in (("ZJ a=2 (Wang 2014)", {"W": 1, "T": 1, "L": 0}), ("US dyads (Brockbank)", {"W": 2, "T": 2, "L": 2}),
                   ("AU pairs (Moerel)", {"W": 1, "T": 2, "L": 2})):
    t = COND[name]
    mc = sim(t, rule)
    ex = match(t, rule, 2)
    print(f"{name} rule {rule}: MC Bo3 P(win) {mc[0]:.4f} vs exact {ex[0]:.4f}; edge/throw {mc[1]*100:+.2f} vs {ex[3]*100:+.2f}; throws {mc[2]:.3f} vs {ex[1]:.3f}")
# long-run stationary check
t = COND["ZJ a=2 (Wang 2014)"]; rule = {"W": 1, "T": 1, "L": 0}
mc = sim(t, rule, nmatch=1, N=400000)
print(f"ZJ long run edge {mc[1]*100:+.2f} vs stationary {stationary(t, rule)[1]*100:+.2f}")
