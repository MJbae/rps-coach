"""Exploiting an opponent with outcome-conditioned responses (stay / up / down).

Hands are relative to the opponent's previous hand h:
  stay = h, up = the hand that beats h, down = the hand that h beats.
Opponent's next-throw distribution after outcome o in {W,T,L} (opponent's view): (s_o, u_o, d_o).
Our reply Y in {h, up, down}:  win vs prev(Y), lose vs next(Y).
  Y=h    -> we beat 'down', lose to 'up'       edge = d - u
  Y=up   -> we beat 'stay', lose to 'down'     edge = s - d
  Y=down -> we beat 'up',   lose to 'stay'     edge = u - s
"""
import sys
import json
import numpy as np

REPLY = ("h", "up", "down")


def reply_outcomes(p, reply):
    s, u, d = p
    if reply == "h":
        return {"opp_win": u, "tie": s, "opp_loss": d}
    if reply == "up":
        return {"opp_win": d, "tie": u, "opp_loss": s}
    return {"opp_win": s, "tie": d, "opp_loss": u}


def best_reply(p):
    edges = {r: reply_outcomes(p, r)["opp_loss"] - reply_outcomes(p, r)["opp_win"] for r in REPLY}
    r = max(edges, key=edges.get)
    return r, edges[r]


def long_run(params, policy=None):
    """params: {'W':(s,u,d),'T':(...),'L':(...)} (opponent's view). policy: {'W':reply,...} or None=best reply."""
    order = ("W", "T", "L")
    pol = policy or {o: best_reply(params[o])[0] for o in order}
    T = np.zeros((3, 3))
    for i, o in enumerate(order):
        r = reply_outcomes(params[o], pol[o])
        T[i] = [r["opp_win"], r["tie"], r["opp_loss"]]
    w, v = np.linalg.eig(T.T)
    pi = np.real(v[:, np.argmin(np.abs(w - 1))])
    pi = pi / pi.sum()
    edge = sum(pi[i] * (T[i][2] - T[i][0]) for i in range(3))
    win = sum(pi[i] * T[i][2] for i in range(3))
    loss = sum(pi[i] * T[i][0] for i in range(3))
    return {"policy": pol, "stationary_prev_outcome(opp W,T,L)": pi.round(4).tolist(),
            "our_win": round(win, 4), "our_loss": round(loss, 4), "edge": round(edge, 4),
            "q_decisive": round(win / (win + loss), 4)}


def shrink(params, f):
    return {o: tuple(1 / 3 + f * (x - 1 / 3) for x in p) for o, p in params.items()}


if __name__ == "__main__":
    params = {k: tuple(v) for k, v in json.loads(sys.argv[1]).items()}
    for o, p in params.items():
        assert abs(sum(p) - 1) < 1e-6, (o, p)
        print(o, "best reply:", best_reply(p))
    for f in (1.0, 0.5):
        print(f"bias x{f}:", long_run(shrink(params, f)))
