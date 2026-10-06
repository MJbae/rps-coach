"""Markov machinery for outcome-conditioned RPS play.

Opponent state o in {W,T,L} = the opponent's own previous outcome.
Opponent next move relative to its previous hand X: index 0 = stay (X), 1 = up (X+), 2 = down (X-).
Our move relative to X: 1 = X+ (beats X), 0 = X, 2 = X- (hand X beats); 'r' = uniform random.
We win iff (our_d - opp_d) % 3 == 1, tie iff == 0, lose iff == 2.
"""
import numpy as np

STATES = ("W", "T", "L")
NAME = {1: "X+", 0: "X", 2: "X-", "r": "rand"}


def norm(q):
    q = np.array(q, dtype=float)
    return q / q.sum()


def outcome_probs(our_d, q):
    """Return (our_win, tie, our_loss) when we play relative hand our_d and opp plays q=(stay,up,down)."""
    q = norm(q)
    if our_d == "r":
        return np.array([1 / 3, 1 / 3, 1 / 3])
    w = t = l = 0.0
    for opp_d, pr in zip((0, 1, 2), q):
        diff = (our_d - opp_d) % 3
        if diff == 1:
            w += pr
        elif diff == 0:
            t += pr
        else:
            l += pr
    return np.array([w, t, l])


def edges(q):
    """Edge (win-loss) of each relative response vs opp distribution q."""
    return {d: (lambda o: o[0] - o[2])(outcome_probs(d, q)) for d in (1, 0, 2)}


def best_response(table):
    br = {}
    for s in STATES:
        e = edges(table[s])
        d = max(e, key=e.get)
        br[s] = (d, e[d])
    return br


def step_probs(table, rule, s, p=1.0, knowing=False):
    """Probabilities of OPPONENT outcome (W,T,L) next, from opp state s.
    rule[s] = our relative hand or 'r'; with prob p we follow rule, else uniform.
    knowing=True: opponent knows the rule and best-responds (beats the rule hand)."""
    if knowing:
        if rule[s] == "r":
            return np.array([1 / 3, 1 / 3, 1 / 3])
        hit = p + (1 - p) / 3
        return np.array([hit, (1 - p) / 3, (1 - p) / 3])  # opp W, T, L
    o = outcome_probs(rule[s], table[s])  # our (w,t,l)
    ours = p * o + (1 - p) * np.array([1 / 3, 1 / 3, 1 / 3])
    return np.array([ours[2], ours[1], ours[0]])  # convert to opp outcome (W,T,L)


def stationary(table, rule, p=1.0, knowing=False):
    M = np.array([step_probs(table, rule, s, p, knowing) for s in STATES])
    # solve pi M = pi
    A = np.vstack([M.T - np.eye(3), np.ones(3)])
    b = np.array([0, 0, 0, 1.0])
    pi = np.linalg.lstsq(A, b, rcond=None)[0]
    # per-throw our edge = sum pi_s * (P(opp L) - P(opp W))
    e = sum(pi[i] * (M[i][2] - M[i][0]) for i in range(3))
    tie = sum(pi[i] * M[i][1] for i in range(3))
    return pi, e, tie


def match(table, rule, N, p=1.0, knowing=False, first=(1 / 3, 1 / 3, 1 / 3)):
    """First to N decisive wins, ties replayed. First throw: our (win,tie,loss)=first.
    Returns P(we win), E[throws], E[our wins - our losses], per-throw edge."""
    # transient states: (a, b, s) with a,b < N, s in {S0, W, T, L}
    idx = {}
    for a in range(N):
        for b in range(N):
            for s in ("S0",) + STATES:
                idx[(a, b, s)] = len(idx)
    n = len(idx)
    Q = np.zeros((n, n))
    Rwin = np.zeros(n)
    r_throw = np.ones(n)
    r_net = np.zeros(n)
    for (a, b, s), i in idx.items():
        if s == "S0":
            ow, ot, ol = first  # our outcome probs
        else:
            pr = step_probs(table, rule, s, p, knowing)  # opp W,T,L
            ow, ot, ol = pr[2], pr[1], pr[0]
        r_net[i] = ow - ol
        # our win -> opp state L
        if a + 1 >= N:
            Rwin[i] += ow
        else:
            Q[i, idx[(a + 1, b, "L")]] += ow
        Q[i, idx[(a, b, "T")]] += ot
        if b + 1 < N:
            Q[i, idx[(a, b + 1, "W")]] += ol
    I = np.eye(n)
    F = np.linalg.solve(I - Q, np.eye(n))
    s0 = idx[(0, 0, "S0")]
    pwin = (F @ Rwin)[s0]
    ethrows = (F @ r_throw)[s0]
    enet = (F @ r_net)[s0]
    return pwin, ethrows, enet, enet / ethrows


def shrink(table, f=0.5):
    out = {}
    for s in STATES:
        q = norm(table[s])
        out[s] = tuple(1 / 3 + f * (x - 1 / 3) for x in q)
    return out


def only_loss(table):
    return {"W": (1 / 3, 1 / 3, 1 / 3), "T": (1 / 3, 1 / 3, 1 / 3), "L": tuple(table["L"])}
